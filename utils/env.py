import os
from dotenv import load_dotenv

load_dotenv()


def env(key: str) -> str:
    return os.environ.get(key)
