from sqlalchemy import Column, Integer, String, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(80), nullable=False, unique=True, index=True)
    full_name = Column(String(80), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    google_id = Column(String(80))
    updated_at = Column(String(80))
    created_at = Column(String(80))
    email_verified = Column(Boolean)
    role = Column(Integer)
    avatar_url = Column(String(255))
    forgot_password_token = Column(String(255))
    activated = Column(Boolean)
    
    def __repr__(self):
        return 'UserModel(email=%s, full_name=%s, password=%s, google_id=%s, updated_at=%s, created_at=%s, email_verified=%s, role=%s)' % (self.email, self.full_name, self.password, self.google_id, self.updated_at, self.created_at, self.email_verified, self.role)
    
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "google_id": self.google_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "email_verified": self.email_verified,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "activated": self.activated
        }
    