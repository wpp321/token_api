import redis
from peewee import *
import config
import copy
import datetime

redis_conn = redis.StrictRedis(**config.redis_conf)
database = MySQLDatabase(**config.mysql)


class User(Model):
    first_name = CharField(null=True)
    id = CharField(primary_key=True)
    last_name = CharField(null=True)
    mobile = CharField(null=True)

    class Meta:
        table_name = 'user'
        database = database

    def to_dict(self):
        dic = copy.deepcopy(self.__data__)
        for k in dic:
            if isinstance(dic[k], datetime.datetime):
                dic[k] = dic[k].strftime('%Y-%m-%d %H:%M:%S')
        return dic
