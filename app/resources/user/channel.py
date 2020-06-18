from flask import request, g
from app import db
from utils.decorators import login_required
from flask import g
from flask_restful import Resource
from sqlalchemy.orm import load_only
from models.article import Channel, UserChannel


class UserChannelResource(Resource):
    """用户频道"""
    method_decorators = {'put': [login_required]}
    def get(self):
        # 获取用户信息
        userid = g.userid
        if userid:  # 判断用户是否登录
            # 如果登录，查询用户频道(根据用户id 进行查询，要求正在使用，根据序号排序)
            # channels = Channel.query.options\
            #         (load_only(Channel.id,Channel.name)).\
            #         filter(UserChannel.user_id==userid,
            #                 UserChannel.is_deleted ==False).\
            #         order_by(UserChannel.sequence).all()

            channels = Channel.query.options \
                (load_only(Channel.id, Channel.name)) \
                .join(UserChannel, Channel.id == UserChannel.channel_id). \
                filter(UserChannel.user_id == userid, UserChannel.
                       is_deleted == False). \
                order_by(UserChannel.sequence).all()
            if len(channels) == 0:  # 用户未选择频道，则查询默认频道
                channels = Channel.query.options(
                    load_only(Channel.id, Channel.name)). \
                    filter(Channel.is_default == True).all()
        else:  # 未登录，查询默认频道
            channels = Channel.query.options(
                load_only(Channel.id, Channel.name)). \
                filter(Channel.is_default == True).all()
        # 序列化
        channel_list = [channel.to_dict() for channel in channels]

        # 手动添加‘推荐频道’，数据库中没有保存该频道的数据，该频道数据有推荐系统来返回
        channel_list.insert(0, {'id': 0, 'name': '推荐'})

        # 返回数据
        return {'channels': channel_list}



    def put(self):
        """修改用户频道  重置式更新"""
        # 获取参数
        userid = g.userid
        # request.json 取出来的而是字典格式
        channels = request.json.get('channels')
        # 下面的方法取出来的数据是 字符串，不好调整！
        # parser = RequestParser()
        # parser.add_argument('channels',location = 'json')
        # 将该用户原有的频道列表逻辑删除
        UserChannel.query.filter \
            (UserChannel.user_id == userid,
             UserChannel.is_deleted == False) \
            .update({'is_deleted': True})

        # 遍历新的频道列表
        for channel in channels:  # channel : {'id':1 ,'seq':2}
            # 查询是否关注过该列表
            user_channel = UserChannel.query.options \
                (load_only(UserChannel.id)) \
                .filter(UserChannel.user_id == userid,
                        UserChannel.channel_id == channel['id']).first()
            if user_channel:
                user_channel.sequence = channel['seq']
                user_channel.is_deleted = False
            else:
                user_channel = UserChannel \
                    (user_id=userid,
                     channel_id=channel['id'],
                     sequence=channel['seq'])
                db.session.add(user_channel)
        db.session.commit()
        # 有，更新数据（序号，逻辑删除）
        # 无，新增数据
        return {'channel': channels}
