class DefaultConfig:
    """默认配置"""
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.150.129:3306/hm_topnews'  # 连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的SQL
    SQLALCHEMY_BINDS = {  # 主从数据库的URI
        "master": 'mysql://root:mysql@192.168.150.129:3306/hm_topnews',
        "slave1": 'mysql://root:mysql@192.168.150.129:3306/hm_topnews',
        "slave2": 'mysql://root:mysql@192.168.150.129:8306/hm_topnews'
    }
    # redis配置
    REDIS_HOST = '192.168.150.129'  # ip
    REDIS_PORT = 6381  # 端口

    # JWT
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'  # 秘钥
    JWT_EXPIRE_DAYS = 14  # JWT过期时间

    # 七牛云
    QINIU_ACCESS_KEY = 'Z3n7VHTzWjjTxiSQc1cLlvtjdBjdG6yIsRYXim54'
    QINIU_SECRET_KEY = 'OuU8PaON7VxJYiO7ER_uS_MIsx-PkmkgckiEDBeN'
    QINIU_BUCKET_NAME = 'zhdsh35'
    QINIU_DOMAIN = 'http://qc3o3ps8s.bkt.clouddn.com/'

    CORS = ['http://127.0.0.1:5000']
    # CORS = ['http://0.0.0.0:8000']


config_dict = {
    'dev': DefaultConfig
}
