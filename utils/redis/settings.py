import redis


def connect_redis():
    red = redis.Redis()
    return red
