from flask import Blueprint
from flask_restful import Api

from app.resources.user.profile import CurrentUserResource
from utils.constats import BASE_URL_PRIFIX
from .passport import SMSCodeResource, LoginResource
from utils.output import output_json

# 1.创建蓝图对象
user_bp = Blueprint('user', __name__,url_prefix=BASE_URL_PRIFIX)

# 2. 根据Api对象
user_api = Api(user_bp)

# 设置json包装格式
user_api.representation('application/json')(output_json)
# 组件添加类视图
user_api.add_resource(SMSCodeResource, '/sms/codes/<mob:mobile>')
user_api.add_resource(LoginResource, '/authorizations')
user_api.add_resource(CurrentUserResource, '/users')
