import sys
from os.path import *

# 将common路径加入模块查询路径
from flask import Flask

from app.settings.config import config_dict
from utils.constats import EXTIA_ENV_CONFIG

BASE_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, BASE_DIR + '/common')

from flask_sqlalchemy import SQLAlchemy



# sqlalchemy组件对象
db = SQLAlchemy()

from flask_migrate import Migrate
# redis数据库操作对象
redis_client = None  # type: StrictRedis
from redis import StrictRedis
def register_extensions(app):
    """组件初始化"""

    # SQLAlchemy组件初始化
    from app import db
    db.init_app(app)
    # 数据迁移组件初始化
    Migrate(app, db)

    # 导入模型类
    from models import user
    # redis组件初始化
    global redis_client
    redis_client = StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)

    # 添加请求钩子
    from utils.middlewares import get_userinfo
    app.before_request(get_userinfo)

def create_app(type):
    """创建应用 和 组件初始化"""

    # 创建flask应用
    app = create_flask_app(type)

    # 组件初始化
    register_extensions(app)


    return app

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




