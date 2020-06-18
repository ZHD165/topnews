# from flask import Flask, Blueprint
#
# from app.resources.user import SMSCodeResource, user_api
# from utils.constats import BASE_URL_PRIFIX
#
#
# def regieter_bp(app:Flask):
#     from app.resources.user import  user_blu #建议局部导入
#
#     app.register_blueprint(user_blu)
#
#     user_api.add_resource(SMSCodeResource, '/sms/codes/<mobile>')
#
#     user_bp = Blueprint('user', __name__, url_prefix=BASE_URL_PRIFIX)
