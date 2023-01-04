from aiocache import cached  # noqa
from dotenv import load_dotenv

from settings.cache.settings import Settings

load_dotenv()

cache_settings = Settings()
cache_settings.make_cache_conf()
