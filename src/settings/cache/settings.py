from aiocache import caches

from settings.base import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    def make_cache_conf(self):
        return caches.set_config(
            {
                "default": {
                    "cache": "aiocache.SimpleMemoryCache",
                    "serializer": {
                        "class": "aiocache.serializers.PickleSerializer"
                    },
                },
                "redis_alt": {
                    "cache": "aiocache.RedisCache",
                    "endpoint": self.REDIS_HOST,
                    "port": self.REDIS_PORT,
                    "password": self.REDIS_PASSWORD,
                    "timeout": 1,
                    "serializer": {
                        "class": "aiocache.serializers.PickleSerializer"
                    },
                    "plugins": [
                        {"class": "aiocache.plugins.HitMissRatioPlugin"},
                        {"class": "aiocache.plugins.TimingPlugin"},
                    ],
                },
            }
        )
