from flask_restful import Resource
from sqlalchemy.orm import load_only
from models.article import Channel


class AllChannelResource(Resource):
    def get(self):
        channels = Channel.query.options \
            (load_only(Channel.id, Channel.name)) \
            .all()

        channel_list = [channel.to_dict() for channel in channels]

        return {'channels': channel_list}
