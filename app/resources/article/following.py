from datetime import datetime

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from models.user import Relation, User
from utils.decorators import login_required


class FollowingUserResource(Resource):
    mehod_decortors = {'post': [login_required]}

    def post(self):
        """关注用户"""
        # 获取参数
        userid = g.userid
        # 1. 创建RequestParser实例
        parser = RequestParser()
        # 2. 添加验证参数
        # 第一个参数： 传递的参数的名称
        # 第二个参数（location）： 传递参数的方式
        # 第三个参数（type）： 验证参数的函数(可以自定义验证函数)
        parser.add_argument('target', required=True, location='args', type=int)

        # args是一个字典
        args = parser.parse_args()
        # 4. 获取验证后的数据

        target = args.target

        # 查询该用户合作者是否有关系
        rel_obj = Relation.query.options(load_only(Relation.id)) \
            .filter(Relation.user_id == userid,
                    Relation.author_id == target).first()
        if rel_obj:  # 如果有关系，更新记录
            rel_obj.relation = Relation.RELATION.FOLLOW
            rel_obj.update_time = datetime.now()
        else:  # 如果无关系，添加记录
            Relation(user_id=userid, author_id=target,
                     relation=Relation.RELATION.FOLLOW)
            db.session.add(rel_obj)
        # 让作者的粉丝数量+1
        User.query.filter(User.id == target).update({'fans_count': User.fans_count + 1})
        # 让用户的关注数量+1
        User.query.filter(User.id == userid).update({'following_count': User.following_count + 1})
        db.session.commit()
        # 返回结果
        return {'target': target}
