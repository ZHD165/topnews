class DefaultConfig:
    """默认配置"""
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.150.130:3306/hm_topnews'  # 连接地址
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 是否追踪数据变化
    SQLALCHEMY_ECHO = False  # 是否打印底层执行的SQL
    SQLALCHEMY_BINDS = {  # 主从数据库的URI
        "master": 'mysql://root:mysql@192.168.150.130:3306/hm_topnews',
        "slave1": 'mysql://root:mysql@192.168.150.130:3306/hm_topnews',
        "slave2": 'mysql://root:mysql@192.168.150.130:8306/hm_topnews'
    }
    # # redis配置
    # REDIS_HOST = '192.168.150.130'  # ip
    # REDIS_PORT = 6381  # 端口

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


    SERVICE_NAME = 'mymaster'  # 哨兵配置的主数据库别名
    # 设置哨兵的ip和端口
    SENTINEL_LIST = [
        ('192.168.150.130', 26380),
        ('192.168.150.130', 26381),
        ('192.168.150.130', 26382),
    ]
    # redis集群配置
    CLUSTER_NODES = [  # 集群中主数据库的ip和端口号
            {'host': '192.168.150.130', 'port': 7000},
            {'host': '192.168.150.130', 'port': 7001},
            {'host': '192.168.150.130', 'port': 7002},
    ]
config_dict = {
    'dev': DefaultConfig
}
