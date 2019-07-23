# -*- coding: utf-8 -*-
import redis

redis = redis.Redis(host='localhost', port=6379)

redis.zadd("end_game_world_rank", "21", "1003856")

redis.zadd("end_game_world_rank", "19", "1003853")
redis.zadd("end_game_world_rank", "11", "1003857")
redis.zadd("end_game_world_rank", "25", "1003859")
redis.zadd("end_game_world_rank", "28", "1003860")


ret_data = redis.zrevrange("end_game_world_rank", 0, -1, withscores=True)

print ret_data

