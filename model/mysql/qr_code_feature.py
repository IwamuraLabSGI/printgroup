from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, Float
from model.mysql.qr_code import QRCode

Base = declarative_base()


class QRCodeFeature(Base):
    __tablename__ = "qr_code_features"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    qr_code_id = Column(Integer, ForeignKey(QRCode.id), nullable=False)
    feature = Column(Float, nullable=False)
