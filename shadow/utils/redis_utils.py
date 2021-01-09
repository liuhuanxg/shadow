# -*- coding: utf-8 -*-
"""

"""
import redis
import time


class RedisConnect:
    def __init__(self):
        self.redisC = redis.Redis(host='localhost', port=6379, db=3, password=None, )

    def add_sset_data(self, name, mapping, nx=False, xx=False, ch=False, incr=False):
        self.redisC.zadd(name, mapping, nx, ch, incr)

    def get_zrangebyscore_date(self, name, min, max):
        return self.redisC.zrangebyscore(name, min, max)

    def zremrangebyscore(self, name, min, max):
        self.redisC.zremrangebyscore(name, min, max)

    def get_zrange_withsocre(self, name, start, end, desc=False, withscores=False, score_cast_func=float):
        return self.redisC.zrange(name, start, end, desc, withscores)


def func(report, username):
    connect = RedisConnect()

    now_time = int(str(time.time()).split(("."))[0])
    activity_leavel = 120
    connect.add_sset_data(report, {username: now_time + activity_leavel})
    connect.zremrangebyscore(report, 0, now_time)
    result = connect.get_zrangebyscore_date(report, 0, now_time + activity_leavel)
    print(result)
    result = connect.get_zrange_withsocre(report, 0, -1, withscores=True)
    print(result)