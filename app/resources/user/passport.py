from datetime import datetime,timedelta
import random
from flask import current_app
from flask_restful.inputs import regex
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only
from flask_restful import Resource
from app import redis_client, db
from models.user import User
from utils.constats import SMS_CODE_EXPIRE
from utils.jwt_util import generate_jwt
from utils.parser import mobile as mobile_type


class SMSCodeResource(Resource):
    """获取短信验证码"""

    def get(self, mobile):
        # 1生成短信验证码
        # rand_num = '%06d' % random.randint(0, 999999)
        rand_num = 123456

        # 2.保存验证码(redis)  app:(:相当于下划线)code：18838118792  123456
        key = 'app:code:{}'.format(mobile)
        redis_client.set(key, rand_num, ex=SMS_CODE_EXPIRE)

        # 3.发送短信 第三方短信平台 celery
        # print('短信验证码："mobile":{},"code":{}'.format(mobile, rand_num))
        print(f'短信验证码："mobile":{mobile},"code":{rand_num}')
        # 3.返回json给前段
        return {'mobile': mobile}


class LoginResource(Resource):
    """注册登录"""

    def post(self):
        # 获取参数
        parser = RequestParser()
        parser.add_argument('mobile', required=True, location='json', type=mobile_type)
        parser.add_argument('code', required=True, location='json', type=regex(r'\d{6}$'))
        args = parser.parse_args()
        mobile = args.mobile
        code = args.code
        # 效验短信验证码
        key = 'app:code:{}'.format(mobile)
        real_code = redis_client.get(key)
        if not real_code or real_code != code:
            return {'message': 'Invaild Code', 'data': None},400
        # 删除验证码
        # redis_client.delete(key)
        # 查询数据库
        user = User.query.options(load_only(User.id)).filter(User.mobile == mobile).first()
        if user:  # 有,更新最后登录时间
            user.last_login = datetime.now()
        else:  # 无,添加用户数据
            user = User(mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
        db.session.commit()

        # 生成令牌
        token = generate_jwt({'userid': user.id},
                             datetime.utcnow() + timedelta(days=current_app.config['JWT_EXPIRE_DAYS']))

        return {'id':user.id,
                'toekn': token}, 201
