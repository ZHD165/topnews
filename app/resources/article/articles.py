from datetime import datetime

from flask import g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from models.article import Article, ArticleContent, Collection, Attitude
from models.user import User, Relation
from utils.constats import HOME_PRE_PAGE


class ArticleListResource(Resource):

    def get(self):
        # 获取参数
        # 1. 创建RequestParser实例
        parser = RequestParser()
        # 2. 添加验证参数
        # 第一个参数： 传递的参数的名称
        # 第二个参数（location）： 传递参数的方式
        # 第三个参数（type）： 验证参数的函数(可以自定义验证函数)
        parser.add_argument('channel_id', required=True, location='args', type=int)
        parser.add_argument('timestamp', required=True, location='args', type=int)
        # 3. 验证数据
        # args是一个字典
        args = parser.parse_args()
        # 4. 获取验证后的数据
        channel_id = args.channel_id
        timestamp = args.timestamp

        # 如果“推荐”频道，先返回空数据

        if channel_id == 0:
            return {'results': [], 'pre_timestamp': 0}

        # 将timestamp 转为datetime(日期时间格式)类型
        date = datetime.fromtimestamp(timestamp * 0.001)
        # 查询频道中对应的数据 链接查询 要求： 频道对应 & 审核通过 &发布时间 《timestamp
        data = db.session.query(Article.id,
                                Article.title,
                                Article.user_id,
                                Article.ctime,
                                User.name,
                                Article.comment_count,
                                Article.cover) \
            .join(User, Article.user_id == User.id) \
            .filter(Article.channel_id == channel_id,
                    Article.status == Article.STATUS.APPROVED,
                    Article.ctime < date) \
            .order_by(Article.ctime.desc()) \
            .limit(HOME_PRE_PAGE).all()
        print(data)
        # ctime 为日期时间对象
        # 序列化
        articles = [{
            'art_id': item.id,
            'title': item.title,
            'aut_id': item.user_id,
            'pubdate': item.ctime.isoformat(),
            'aut_name': item.name,
            'comm_count': item.comment_count,
            'cover': item.cover
        }
            for item in data]
        # 设置该组数据最后一条的发布时间为 pre_timestamp
        # 构建相应数据（需要设置改组数据最后一条发布的时间为对应的时间戳，转化为毫秒为单位）
        # 日期对象 转为时间戳 日期对象.tiemstamp()

        pre_timestamp = int(data[-1].ctime.timestamp() * 1000) if data else 0

        # 返回数据

        return {'results': articles, 'pre_timestamp': pre_timestamp}


class ArticleDetailResource(Resource):

    def get(self, article_id):

        data = db.session.query(
            Article.id, Article.title, Article.ctime,
            Article.user_id, User.name, User.profile_photo,
            ArticleContent.content) \
            .join(User, Article.user_id == User.id) \
            .join(ArticleContent,

                   Article.id==ArticleContent.article_id ) .filter(Article.id == article_id).first()
        article_data = {
            'art_id': data.id,
            'title': data.title,
            'pubdate': data.ctime.isoformat(),
            'aut_id': data.user_id,
            'aut_name': data.name,
            'aut_photo': data.profile_photo,
            'content': data.content,
            'is_followed': False,
            'attitude': -1,
            'is_collected': False}



        """查询关系数据"""
        # 获取参数
        userid = g.userid

        # 判断用户是否已登录

        if userid:
            # 查询用户关系  用户 -> 作者
            relation_obj = Relation.query.options(
                load_only(Relation.id)) \
                .filter(Relation.user_id == userid,
                        Relation.author_id == data.user_id,
                        Relation.relation == Relation.RELATION.FOLLOW).first()

            article_data['is_followed'] = True if relation_obj else False

            # 查询用户对文章的态度  用户 -> 文章
            collect = Collection.query.options(load_only(Collection.id)) \
                .filter(Collection.user_id == userid,
                        Collection.article_id == article_id,
                        Collection.is_deleted == False).first()

            atti_obj = article_data['is_collected'] = True if collect else False

            # 查询收藏关系  用户 -> 文章
            Attitude.query.options(load_only(Attitude.attitude)) \
                .filter(Attitude.user_id == userid,
                        Attitude.article_id == article_id).first()

            if not atti_obj:
                attitude = -1
            else:
                attitude = atti_obj.attitude

            article_data['attitude'] = attitude


        # return {'data':article_data}
        return article_data
