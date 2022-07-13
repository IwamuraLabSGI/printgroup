from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Float

Base = declarative_base()


class QRCodeFeature(Base):
    __tablename__ = "qr_code_features"
    id = Column(Integer, primary_key=True)
    qr_code_id = Column(ForeignKey('qr_codes.id'), nullable=False)
    feature = Column(Float, nullable=False)