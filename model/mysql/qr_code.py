from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean
from dataclasses import dataclass

Base = declarative_base()


class QRCode(Base):
    __tablename__ = "qr_codes"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    s3_uri = Column(String(255), nullable=False)
    file_name = Column(String(255))
    feature_hash_cache_created = Column(Boolean, nullable=False, default=False)

@dataclass
class QRCodeCount:
    id: int
    count: int
