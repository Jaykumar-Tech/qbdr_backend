from sqlalchemy import Column, String, DateTime, Integer, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

class EmailVerify(Base):
    __tablename__ = "emailverify"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), index=True)
    verify_code = Column(String(6))
    created_at = Column(DateTime)