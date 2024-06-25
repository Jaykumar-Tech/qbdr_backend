from sqlalchemy import Column, Integer, String, Boolean, MetaData, Date, DateTime, Float, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class QBSettings(Base):
    __tablename__ = "qb_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    client_id = Column(String(255))
    client_secret = Column(String(255))
    refresh_token = Column(String(255))
    access_token = Column(Text())
    realm_id = Column(String(255))
    is_sandbox = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, server_default=text("now()"))