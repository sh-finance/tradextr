from redis import Redis

from config import Redis as RedisConfig

redis = Redis(
    host=RedisConfig.host,
    port=RedisConfig.port,
    password=RedisConfig.password,
)
