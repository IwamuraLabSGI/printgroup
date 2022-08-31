from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

@dataclass
class MySQLConfig:
    host: str = ''
    port: int = 0
    user: str = ''
    password: str = ''
    database: str = ''


class MySQL:
    _config: MySQLConfig
    _engine: Engine
    _session: Session

    def __init__(self, config: MySQLConfig):
        self._config = config

    def connect(self):
        config = self._config
        self._engine = create_engine(
            f'mysql+pymysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?charset=utf8mb4'
        )
        SessionClass = sessionmaker(self._engine)
        self._session = SessionClass()

    def get_session(self):
        return self._session
