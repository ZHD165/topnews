from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only

from models.user import User
from utils.decorators import login_required


class CurrentUserResource(Resource):
    method_decorators = {'get',[login_required]}

    def get(self):
        # 获取用户信息
        # 获取用户id

        userid= g.userid
        #根据id 从数据库中查询用户信息
        user=User.query.opions(load_only(User.id,User.name,
                                    User.profile_photo
                                    ,User.introduction,
                                    User.article_count,
                                    User.following_count,
                                    User.fans_count)).filter(User.id==userid).first()
        # 返回
        return user.to_dict()