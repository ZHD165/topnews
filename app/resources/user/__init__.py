from flask import Blueprint
from flask_restful import Api

from app.resources.user.profile import CurrentUserResource
from .passport import SMSCodeResource, LoginResource

# 1.创建蓝图对象
user_blu = Blueprint('user', __name__)
# 2. 根据蓝图创建组件对象
user_api = Api(user_blu)
# 设置json包装格式
from utils.output import output_json

user_api.representation('application/json')(output_json)
# 组件添加类视图
user_api.add_resource(SMSCodeResource, '/sms/code/<mob:mobile>')
user_api.add_resource(LoginResource, '/authorizations')
user_api.add_resource(CurrentUserResource, '/users')