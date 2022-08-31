from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, PrimaryKeyConstraint
from sqlalchemy.types import JSON, Float

Base = declarative_base()


class QRCodeFeatureHashCache(Base):
    __tablename__ = "qr_code_feature_hash_caches"
    __table_args__ = (
        PrimaryKeyConstraint('hash'),
    )
    hash = Column(Float, nullable=False, unique=True)
    qr_code_ids = Column(JSON, nullable=False)
