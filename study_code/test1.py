# -*- coding: utf-8 -*-
import redis

r = redis.Redis(host='localhost', port=6379)

r.zadd("end_game_world_rank", 21, 1003856)

r.zadd("end_game_world_rank", level=19, uin=1003853)
r.zadd("end_game_world_rank", level=11, uin=1003857)
r.zadd("end_game_world_rank", level=25, uin=1003859)
r.zadd("end_game_world_rank", level=28, uin=1003860)


ret_data = r.zrevrange("end_game_world_rank", 0, -1, withscores=True)

print ret_data

