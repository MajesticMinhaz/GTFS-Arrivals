from redis import Redis
from .config import Config


# Create a Redis client instance with the specified configuration options
my_redis = None

if not Config.CACHE_REDIS_SOCK:
    my_redis = Redis(
        host=Config.CACHE_REDIS_HOST,
        port=Config.CACHE_REDIS_PORT,
        db=0
    )
else:
    my_redis = Redis(
        unix_socket_path=Config.CACHE_REDIS_SOCK
    )
