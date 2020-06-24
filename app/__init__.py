import sys
from os.path import *
from flask import Flask
from flask_cors import CORS
from redis.sentinel import Sentinel
from app.settings.config import config_dict

BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR + '/common')
from utils.constats import EXTIA_ENV_CONFIG
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# sqlalchemy组件对象
# db = SQLAlchemy()
from models.routing_db.routing_sqlalchemy import RoutingSQLAlchemy

# mysql数据库操作对象
db = RoutingSQLAlchemy()
# redis数据库操作对象
redis_client = None  # type: StrictRedis
from redis import StrictRedis

# redis主从数据库
redis_master = None  # type: StrictRedis
redis_slave = None  # type: StrictRedis


def create_flask_app(type):
    """创建flask应用"""

    app = Flask(__name__)
    # 根据类型加载配置子类

    config_class = config_dict[type]
    # 先加载默认配置
    app.config.from_object(config_class)

    # 在加载额外配置
    app.config.from_envvar(EXTIA_ENV_CONFIG, silent=True)

    # 返回应用
    return app


def register_extensions(app: Flask):
    """组件初始化"""

    # SQLAlchemy组件初始化
    from app import db

    db.init_app(app)

    # redis组件初始化
    # 哨兵客户端
    global redis_master, redis_slave
    sentinel = Sentinel(app.config['SENTINEL_LIST'])
    redis_master = sentinel.master_for(app.config['SERVICE_NAME'], decode_responses=True)
    redis_slave = sentinel.slave_for(app.config['SERVICE_NAME'], decode_responses=True)
    # 添加转换器
    from utils.converters import register_converters
    register_converters(app)

    # 数据迁移组件初始化
    Migrate(app, db)

    # 添加请求钩子
    from utils.middlewares import get_userinfo
    app.before_request(get_userinfo)

    #
    CORS(app, supports_credentials=True)

    # 导入模型类
    from models import user, article


def register_bp(app: Flask):
    """注册蓝图"""

    # 局部导入
    from app.resources.user import user_bp
    app.register_blueprint(user_bp)

    from app.resources.article import article_bp
    app.register_blueprint(article_bp)


def create_app(type):
    """创建应用 和 组件初始化"""

    # 创建flask应用
    app = create_flask_app(type)

    # 组件初始化
    register_extensions(app)

    # 注册蓝图
    register_bp(app)

    return app
