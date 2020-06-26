from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from sqlalchemy.orm import load_only

from app import db
from cache.user import UserCache
from models.user import User
from utils.decorators import login_required
from utils.parser import image_file

"""
class CurrentUserResource(Resource):
    method_decorators = {'get':[login_required]}

    def get(self):
        # 获取用户信息
        # 获取用户id

        userid= g.userid
        #根据id 从数据库中查询用户信息
        
        user=User.query.options(load_only(User.id,
                                    User.name,
                                    User.profile_photo,
                                    User.introduction,
                                    User.article_count,
                                    User.following_count,
                                    User.fans_count)).filter(User.id==userid).first()
        # 返回
        return user.to_dict()
"""


class CurrentUserResource(Resource):
    method_decorators = {'get': [login_required]}

    def get(self):
        # 获取用户信息
        # 获取用户id

        userid = g.userid
        user_cache = UserCache(userid).get()
        if user_cache:
            return user_cache
        else:
            return {'message': 'Invalid User', 'date': None}, 400


from utils.img_storage import upload_file


class UserPhotoResource(Resource):
    method_decorators = [login_required]

    def patch(self):
        """修改头像"""

        # 获取头像
        userid = g.userid

        parser = RequestParser()

        parser.add_argument('photo', required=True,
                            location='files', type=image_file)
        args = parser.parse_args()

        photo_file = args.photo
        # 读取二进制数据

        file_bytes = photo_file.read()

        # 上传到七牛晕
        try:
            file_url = upload_file(file_bytes)
        except BaseException as e:

            return {'message': "Thired Error: %s" % e}, 500
        # 将数据库中头像url进行更新
        User.query.filter(User.id == userid).update({'profile_photo': file_url})
        db.session.commit()
        # 用户信息更新后，删除用户基础数据-缓存
        UserCache(userid).clear()
        # 返回url
        return {'photo_url': file_url}
        #
