import random


# 方案 一  ：使用常量封装过期时间
# 缺点： 要求常量必须局部导入


# 用户数据过期时间
# 为了表面缓存雪崩，给过期时间设置随机值
# UserCacheTTl = 60*60*2+ random.randint(0,600)


# 方案2  使用函数封装过期时间.

# UserCacheTTL = 60*60*2
# UserCacheMaxDelta = 60*10
# def get_val(ttl,max_delta):
#
#     return ttl+ random.randint(0,max_delta)


# 方案三 : 使用类分装过期时间

class BaseCacheTTl:
    TTl = 60 * 60 * 2  # 过期时间
    MAX_DELTA = 60 * 10  # 随机最大值

    @classmethod
    def get_val(cls):
        return cls.TTl + random.randint(0, cls.MAX_DELTA)


class UserCacheTTL(BaseCacheTTl):
    """用户缓存-过期时间类"""
    pass


class UserNotExistTTL(BaseCacheTTl):
    TTL = 60 * 10
    MAX_DELTA = 60


class ArticleCacheTTL(BaseCacheTTl):
    TTL = 60 * 60 * 5
