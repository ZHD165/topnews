class DefaultConfig:
    """默认配置"""
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.150.129:3306/hm_topnews'  # 连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的SQL

    # redis配置
    REDIS_HOST = '192.168.150.129'  # ip
    REDIS_PORT = 6381  # 端口

    # JWT
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'  # 秘钥
    JWT_EXPIRE_DAYS = 14  # JWT过期时间


config_dict = {
    'dev': DefaultConfig
}
