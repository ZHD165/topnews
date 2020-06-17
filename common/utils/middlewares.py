from flask import request, g

from utils.jwt_util import verify_jwt


def get_userinfo():
    #获取请求投头中的token

    token = request.headers.get('Authorization')
    g.userid = None
    #验证token

    if token:

        data = verify_jwt(token)

        if data:
            #去除用户id ，使用g变量记录
            g.userid =data.get('userid')