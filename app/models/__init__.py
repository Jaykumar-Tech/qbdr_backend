from sqlalchemy import MetaData

from app.user.model import Base as UserBase
from app.email_verify.model import Base as EmailVerifyBase

# Combine all Base.metadata objects into a single MetaData object
metadata = MetaData()
UserBase.metadata.bind = metadata
EmailVerifyBase.metadata.bind = metadata

# Create a combined Base class if needed for other purposes
from sqlalchemy.ext.declarative import declarative_base
CombinedBase = declarative_base(metadata=metadata)