from flask import Flask, request, jsonify
from db import redis_conn, User
import jwt
import datetime
import config

app = Flask(__name__)


@app.route('/token', methods=['POST'])
def get_token():
    mobile = request.get_json().get("mobile")
    opt = request.get_json().get("opt")
    if not all([mobile, opt]):
        return jsonify(code=0, msg="参数不全")
    mobile_code = redis_conn.get("MOBILE_CODE_" + mobile)
    if mobile_code is None:
        return jsonify(code=0, msg="未获取手机验证码")
    if mobile_code.decode() != opt:
        return jsonify(code=0, msg="验证码不匹配")
    try:
        user = User.get(mobile=mobile)
    except:
        return jsonify(code=0, msg="用户未注册")
    access_token = jwt.encode(
        payload={'id': user.id,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config.ACCESS_TOKEN_EXPIRE)},
        key=config.ACCESS_SECRET).decode()
    refresh_token = jwt.encode(
        payload={'id': user.id,
                 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=config.REFRESH_TOKEN_EXPIRE)},
        key=config.REFRESH_SECRET).decode()
    return jsonify(access_token=access_token, refresh_token=refresh_token, expiry=config.ACCESS_TOKEN_EXPIRE)


def check_token(func):
    def wrapper():
        authorization = request.headers.get("Authorization")
        if authorization is None:
            return jsonify(code=0, msg="无效请求")
        try:
            payload = jwt.decode(jwt=authorization, key=config.ACCESS_SECRET)
        except:
            return jsonify(code=0, msg="无效令牌")
        try:
            user = User.get(id=payload["id"])
            request.current_user = user.to_dict()
        except:
            return jsonify(code=0, msg="无效用户")
        return func()

    return wrapper


@app.route('/profile', methods=['POST'])
@check_token
def get_profile():
    request.current_user.pop("mobile")
    return jsonify(**request.current_user)
