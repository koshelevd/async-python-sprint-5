from dotenv import load_dotenv
from pydantic import BaseSettings as Base

load_dotenv()


class BaseSettings(Base):
    pass
