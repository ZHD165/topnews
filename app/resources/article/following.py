from datetime import datetime
from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only
from app import db
from models.user import Relation, User
from utils.decorators import login_required


class FollowingUserResource(Resource):
    method_decorators = {'post': [login_required],'get':[login_required]}

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
        parser.add_argument('target', required=True, location='json', type=int)

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
            relation = Relation(user_id=userid, author_id=target,
                     relation=Relation.RELATION.FOLLOW)
            db.session.add(relation)
        # 让作者的粉丝数量+1
        User.query.filter(User.id == target).update({'fans_count': User.fans_count + 1})
        # 让用户的关注数量+1
        User.query.filter(User.id == userid).update({'following_count': User.following_count + 1})
        db.session.commit()
        # 返回结果
        return {'target': target}

    def get(self):
        # 获取关注列表
        #获取参数
        userid = g.userid
        parser = RequestParser()
        parser.add_argument('page',default=1,location='json',type = int)
        parser.add_argument('per_page',default=2,location='json',type = int)
        args = parser.parse_args()
        page = args.page
        per_page = args.per_page

        #查询数据
        #error_out 默认为True，如果分页越界则抛出404，设置为False则不胡报错，返回空数据
        pn = User.query.options(load_only(User.id,
                                          User.name,
                                          User.profile_photo))\
        .join(Relation,User.id == Relation.author_id)\
        .filter(Relation.user_id == userid,
                Relation.relation ==Relation.RELATION.FOLLOW)\
        .order_by(Relation.update_time.desc())\
        .paginate(page,per_page,error_out=False)

        """相互关注"""
        #查询当前的粉丝列表
        fans_list = Relation.query.options(load_only(Relation.user_id))\
        .filter(Relation.author_id == userid ,
                Relation.relation ==Relation.RELATION.FOLLOW).all()

        #序列化
        author_list=[]
        for item in pn.items:
            au_list = {
            'id':item.id,
            'name':item.name,
            'photo':item.profile_photo,
            'fans_count':item.fans_count,
            'mutual_follow':False
            }
            #判断去除的作者是否在当前用户的粉丝列表中（如果在，则为相互关注）
            for fans in fans_list:
                if fans.user_id ==item.id:
                    au_list['mutual_follow']=True
                    break
            author_list.append(au_list)



        #返回数据
        return {'results':author_list , 'per_page':per_page ,
                'page': pn.page ,'total_count':pn.total}


class UnFollowingUserResource(Resource):
    method_decorators = {'delete': [login_required]}

    def delete(self, target):
        """取消关注"""

        # 获取参数
        userid = g.userid

        # 删除关系 （逻辑删除，将relation字段更新）
        Relation.query.filter(Relation.user_id == userid,
                              Relation.author_id == target,
                              Relation.relation == Relation.RELATION.FOLLOW) \
            .update({'relation': 0, 'update_time': datetime.now()})

        # 让作者的粉丝数量-1
        User.query.filter(User.id == target).update({'fans_count': User.fans_count - 1})
        # 让用户的关注数量-1
        User.query.filter(User.id == userid).update({'following_count': User.following_count - 1})
        db.session.commit()
        # 返回结果
        return {'message': 'ok'}

