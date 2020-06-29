from sqlalchemy.orm import load_only
from app import redis_cluster
from cache.constant import UserCacheTTL, UserNotExistTTL, UserFollowCacheTTL
from models.user import User, Relation


# user:<用户id>:basic   hash   {'name': xx, 'mobile': xx}

# 用户数据缓存类
# 属性
#    userid   用户id
# 方法
#    get()    获取缓存数据
#    clear()  删除缓存数据


class UserCache:
    """用户基础数据-缓存类"""

    def __init__(self, userid):
        self.userid = userid
        self.key = 'user:{}:basic'.format(self.userid)

    def get(self):
        """
        获取缓存
        :return: 包含用户数据的字典/None
        """
        # 从缓存中读取数据
        data = redis_cluster.hgetall(self.key)  # 键不存在会返回空字典

        if data:  # 缓存中如果有，返回缓存数据
            # 判断是否为默认值
            if data.get('null'):
                # 是默认值，返回None
                return None
            else:
                # 不是默认值，直接返回数据
                print('从缓存中获取数据')
                return data

        else:  # 缓存中没有，进行数据库查询
            user = User.query.options(load_only(User.id,
                                                User.name,
                                                User.profile_photo,
                                                User.introduction,
                                                User.article_count,
                                                User.fans_count,
                                                User.following_count)).filter(User.id == self.userid).first()
            if user:  # 数据库中如果有，进行数据回填，返回数据
                # 模型转字典
                user_dict = user.to_dict()
                # 数据回填到redis中
                # todo
                redis_cluster.hmset(self.key, user_dict)
                # 方案一
                # from cache.constant import UserCacheTTl
                # redis_cluster.expire(self.key, 60 * 60 * 2,UserCacheTTl)
                # 方案二
                # redis_cluster.expire(self.key, get_val(UserCacheTTL,UserCacheMaxDelta))3
                # 方案三
                redis_cluster.expire(self.key, UserCacheTTL.get_val())

                print('查询数据库')
                return user_dict
            else:  # 数据库中没有，设置默认值（防止缓存穿透）
                redis_cluster.hmset(self.key, {'null': 1})
                redis_cluster.expire(self.key, UserNotExistTTL.get_val())
                return None

    def clear(self):

        """清除缓存"""

        redis_cluster.delete(self.key)


"""
user:<用户id>:followings   zset   [{value: 用户id, score: 关注时间}, {}...]

用户关注缓存类  UserFollowingCache
  属性
     userid  用户id
     key    redis的键

  方法
    get()   获取缓存
    update()  更新缓存
"""


class BaseFollowingCache:

    def __init__(self, userid):
        self.userid = userid  # 用户id

    def get(self, page, per_page):
        """
        获取关注列表-缓存
        :param page: 页码
        :param per_page: 每页条数
        :return: 关注列表
        """
        # 先从缓存中读取数据
        is_exist_key = redis_cluster.exists(self.key)

        # 构建开始/结束索引
        start_index = (page - 1) * per_page  # 开始索引 = (页码 - 1) * 每页条数
        end_index = start_index + per_page - 1  # 结束索引 = 开始索引 + 每页条数 - 1

        if is_exist_key:  # 如果有, 则直接取出
            print('从缓存中读取数据')
            # 逆序取值, 取出的一定是列表  [作者id, ..]
            return redis_cluster.zrevrange(self.key, start_index, end_index)


        else:  # 如果没有, 进入数据库查询逻辑

            # 如果该用户关注过人(有关注数量), 进行数据库查询
            user = UserCache(self.userid).get()
            if user and user[self.count_key]:

                # 进行数据库查询
                data = self.db_query()

                following_list = []
                # 将数据回填到redis中
                for item in data:
                    # 获取属性  getattr(对象, 字符串形式的属性名)
                    data_id = getattr(item, self.attr_key)

                    redis_cluster.zadd(self.key, data_id, item.update_time.timestamp())
                    following_list.append(item)

                print('从数据查询并回填数据')
                # 设置过期时间
                redis_cluster.expire(self.key, UserFollowCacheTTL.get_val())

                # 返回分页数据
                if start_index <= len(following_list) - 1:  # 判断开始索引是否越界   开始索引 <= 集合的最大索引
                    try:
                        return following_list[start_index:end_index + 1]  # 先尝试正常取值
                    except BaseException:
                        return following_list[start_index:]  # 如果出现异常, 说明结束索引越界, 则直接取出剩余所有数据

                else:
                    return []

            else:  # 如果该用户没有关注过人, 直接返回空列表(防止缓存穿透)
                return []


class UserFollowingCache(BaseFollowingCache):
    count_key = 'follow_count'  # 获取关注数量的键
    attr_key = 'author_id'

    def __init__(self, userid):
        super().__init__(userid)
        self.key = 'user:{}:followings'.format(self.userid)  # redis的键

    def db_query(self):
        # 查询该用户的关注列表(取 作者id, 关注时间, 根据时间倒序排列)
        return Relation.query.options(load_only(Relation.author_id, Relation.update_time)). \
            filter(Relation.user_id == self.userid, Relation.relation == Relation.RELATION.FOLLOW). \
            order_by(Relation.update_time.desc()).all()

    def update(self, author_id, timestamp=None, is_follow=True):
        """
        更新关注列表-缓存  关注/取消关注
        :param author_id: 作者id
        :param timestamp: 关注时间
        :param is_follow: True 关注 / False 取消关注
        """

        # 判断该用户的关注列表是否进行了缓存
        is_key_exist = redis_cluster.exists(self.key)

        if not is_key_exist:  # 如果没有缓存, 则不需要更新, 直接返回
            return

        # 如果有缓存, 则更新缓存
        if is_follow:  # 关注, 添加数据
            redis_cluster.zadd(self.key, author_id, timestamp)
        else:  # 取消关注, 删除数据
            redis_cluster.zrem(self.key, author_id)


class UserFansCache(BaseFollowingCache):
    count_key = 'fans_count'  # 获取粉丝数量的键
    attr_key = 'user_id'

    def __init__(self, userid):
        super().__init__(userid)
        self.key = 'user:{}:fans'.format(self.userid)  # redis的键

    def db_query(self):
        # 查询该用户的粉丝列表
        return Relation.query.options(load_only(Relation.user_id, Relation.update_time)). \
            filter(Relation.author_id == self.userid, Relation.relation == Relation.RELATION.FOLLOW). \
            order_by(Relation.update_time.desc()).all()

    def has_fans(self, fans_id):
        """判断传入的id 是否为当前用户的粉丝"""

        # 判断粉丝列表是否进行了缓存
        is_exist_key = redis_cluster.exists(self.key)

        if not is_exist_key:  # 如果没有缓存, 生成缓存
            items = self.get(1, 1)  # 生成缓存
            if len(items) == 0:  # 该用户没有粉丝
                return False

        # 如果有缓存, 则使用zscore判断是否有指定id对应的分数 (有分数说明有该粉丝, 没有分数说明无该粉丝)
        score = redis_cluster.zscore(self.key, fans_id)
        return True if score else False
