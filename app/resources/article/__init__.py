from flask import Blueprint
from flask_restful import Api

from app.resources.article.articles import ArticleListResource
from app.resources.article.channel import AllChannelResource
from utils.constats import BASE_URL_PRIFIX

# 1.创建蓝图对象
article_bp = Blueprint('article', __name__, url_prefix=BASE_URL_PRIFIX)
# 2.根据蓝图对象创建组建对象

article_api = Api(article_bp)
# 2.创建API对象
from utils.output import output_json

article_api.representation('application/json')(output_json)

article_api.add_resource(AllChannelResource, '/channels')

article_api.add_resource(ArticleListResource, '/articles')
<<<<<<< Updated upstream
=======

article_api.add_resource(ArticleDetailResource, '/articles/<int:article_id>')

article_api.add_resource(FollowingUserResource, '/user/followings')

article_api.add_resource(UnFollowingUserResource, '/user/followings/<int:target>')

article_api.add_resource(CommentsResource,'/comments')
>>>>>>> Stashed changes
