import os
import redis

def RedisBloomFilter(host: str, port: int, db: int, key: str, error_rate :int = 0.01, capacity: int = 1000000):
    redis_client = redis.Redis(host=host, port=port, db=db)
    if not redis_client.exists(key):
        redis_client.execute_command('BF.RESERVE', key, error_rate, capacity)
    return redis_client

def connect_redis():
    return redis.Redis(
        host = os.environ.get('REDIS_HOST'),
        port = int(os.environ.get('REDIS_PORT')),
        db = int(os.environ.get('REDIS_DB'))
    )