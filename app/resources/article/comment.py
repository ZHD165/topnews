from flask import g
from flask_restful import Resource
from flask_restful.inputs import regex
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from app import db
from models.article import Comment, Article
from models.user import User
from utils.decorators import login_required


class CommentsResource(Resource):
    method_decorators = {'post': [login_required]}

    def post(self):
        """发布评论"""
        # 获取参数

        userid = g.userid
        parser = RequestParser()
        parser.add_argument('target', required=True, location='json', type=int)
        # 正则表达式：.代表任何内容，+ 至少一位
        parser.add_argument('content', required=True, location='json', type=regex(r'.+'))
        parser.add_argument('parent_id', location='json', type=int)
        args = parser.parse_args()
        target = args.target  # 文章id
        content = args.content  # 评论内容
        parent_id = args.parent_id  # 父评论id （如果发布子评论，则需要设置）
        print(target,parent_id,content)
        # 判断发布评论\子评论
        if parent_id:  # 发布子评论
            # 新增子评论数据
            sub_comment = Comment(user_id=userid,
                                  article_id=target,
                                  content=content,
                                  parent_id=parent_id)

            db.session.add(sub_comment)
            print(sub_comment)
            # 让父评论回复数量+1
            Comment.query.filter(Comment.id == parent_id).update({
                'reply_count': Comment.reply_count + 1
            })
            db.session.commit()

            return {'com_id': sub_comment.id, 'target': target, 'parent_id': parent_id}
        else:
            # 新增评论数据
            comment = Comment(user_id=userid, article_id=target,
                              content=content, parent_id=0)
            db.session.add(comment)
            # 让文章评论数量加1#
            Article.query.filter(Article.id == target).update({'comment_count': Article.comment_count + 1})
            db.session.commit()

            #
            return {'com_id': comment.id, 'target': target}

    def get(self):
        """获取评论列表"""
        # 获取参数
        parser = RequestParser()
        parser.add_argument('source', required=True, location='args', type=int)  # a 文章id 、c 夫评论id
        #评论id
        parser.add_argument('offset', default=0, location='args', type=int)
        # 基于该字段进行分页查询
        parser.add_argument('limit', default=10, location='args', type=int)
        parser.add_argument('type', required=True, location='args', type=regex(r'[ac]'))
        args = parser.parse_args()
        source = args.source
        offset = args.offset
        limit = args.limit
        type = args.type
        # 判断获取 评论列表 回复列表
        if type == 'a':
            data = db.session.query(Comment.id,
                                    Comment.user_id,
                                    User.name,
                                    User.profile_photo,
                                    Comment.ctime,
                                    Comment.content,
                                    Comment.reply_count,
                                    Comment.like_count) \
                .join(User, Comment.user_id == User.id) \
                .filter(Comment.article_id == source, Comment.id > offset, Comment.parent_id == 0) \
                .limit(limit).all()

            # 查看评论总数
            count = Comment.query.filter(Comment.article_id == source, Comment.parent_id == 0).count()
            # 所有列表中最后一条回复的记录
            # end_comment = Comment.query.options(load_only(Comment.id)) .filter(Comment.article_id == source) .order_by(Comment.id.desc()).first()
            end_comment =Comment.query.options(load_only(Comment.id)).filter(Comment.article_id == source, Comment.parent_id == 0) .order_by(Comment.id.desc()).first()
        else:  # 回复列表
            # 某条评论的的回复列表
            data = db.session.query(Comment.id,
                                    Comment.user_id,
                                    User.name,
                                    User.profile_photo,
                                    Comment.ctime,
                                    Comment.content,
                                    Comment.reply_count,
                                    Comment.like_count) \
                .join(User, Comment.user_id == User.id) \
                .filter(Comment.parent_id == source, Comment.id > offset) \
                .limit(limit).all()
            # 某条评论的的回复总数
            count = Comment.query.filter(Comment.parent_id == source).count()
            # 某条评论的的回复列表中最后一条回复的记录
            end_comment = Comment.query.options(load_only(Comment.id)).filter(Comment.parent_id == source) \
                .order_by(Comment.id.desc()).first()
            """
            common_list = []
            for item in data:
                common_dict = {
                    'com_di': item.id,
                    'aut_id': item.user_id,
                    'aut_name': item.name,
                    'aut_photo': item.profile_photo,
                    'pubdate': item.ctime.isoformat(),
                    'content': item.content,
                    'reply_count': item.reply_count,
                    'like_count': item.like_count
                }
                common_list.append(common_dict)
            # 使其按照评论列表点赞数从大到小排列
            common_list.sort(key=lambda obj: obj['like_count'], reverse=True)
            """
        common_list = []
        for item in data:
            common_dict = {
                'com_di': item.id,
                'aut_id': item.user_id,
                'aut_name': item.name,
                'aut_photo': item.profile_photo,
                'pubdate': item.ctime.isoformat(),
                'content': item.content,
                'reply_count': item.reply_count,
                'like_count': item.like_count
            }
            common_list.append(common_dict)
        # 使其按照评论列表点赞数从大到小排列
        common_list.sort(key=lambda obj: obj['like_count'], reverse=True)

        end_id = end_comment.id if end_comment else None
        # 本次请求中的最后一条id
        last_id = data[-1].id if data else None
        return {'results': common_list, 'total_count': count,
                'end_id': end_id, 'last_id': last_id}
