from sqlalchemy.orm import load_only
from app import redis_cluster
# from cache.constant import get_val, UserCacheTTL, UserCacheMaxDelta
from cache.constant import UserCacheTTL, UserNotExistTTL
from models.user import User


class UserCache:
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
                return data

        else:  # 缓存中没有，进行数据库查询
            user = User.query.options(load_only(User.id,
                                                User.name,
                                                User.profile_photo,
                                                User.introduction,
                                                User.article_count,
                                                User.fans_count,
                                                User.following_count)) \
                .filter(User.id == self.userid).first()
            if user:  # 数据库中如果有，进行数据回填，返回数据
                # 模型转字典
                user_dict = user.to_dict()
                # 数据回填到redis中
                redis_cluster.hmset(self.key, user_dict)
                #方案一
                # from cache.constant import UserCacheTTl
                # redis_cluster.expire(self.key, 60 * 60 * 2,UserCacheTTl)
                # 方案二
                # redis_cluster.expire(self.key, get_val(UserCacheTTL,UserCacheMaxDelta))
                redis_cluster.expire(self.key, UserCacheTTL.get_val())

                print('查询数据库')
                return user_dict
            else:  # 数据库中没有，设置默认值（防止缓存穿透）
                redis_cluster.hmset(self.key, {'null': 1})
                redis_cluster.expire(self.key, UserNotExistTTL.get_val())
                return None
