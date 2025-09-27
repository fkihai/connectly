from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from app.models.user_model import UserModel
from app.enums.role_enum import UserRole

from .config import settings

# create the SQLAlchemy ensgine
engine = create_engine(settings.database_url)

# create the session local class
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# base class for the models
Base = declarative_base()
