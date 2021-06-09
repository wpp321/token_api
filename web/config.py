# mysql配置
mysql = {
    "host": "mysql",
    "user": "root",
    "password": "1234",
    "database": "auth"
}
# redis配置
redis_conf = {
    "host": "redis", "db": 0
}
# access_token 加密密码
ACCESS_SECRET = "ttyGDr8W"
# refresh_token 加密密码
REFRESH_SECRET = "27T1maHX"
# access_token 有效时间
ACCESS_TOKEN_EXPIRE = 7200
# access_token 有效时间
REFRESH_TOKEN_EXPIRE = 3600 * 24 * 7
