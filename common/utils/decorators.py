from functools import wraps

from flask import g


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if g.userid:  # 有用户id ，正常访问
            return f(*args, **kwargs)
        else:  # 如果没有，返回错误信息
            return {'message': 'Invalid Token', 'data': None}, 401

    return wrapper
