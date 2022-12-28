from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DB_URL = 'postgresql://postgres:123@localhost:5432/fastApiTodo'
# engine = create_engine(SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False})   # TO BE USED WITH SQLite
engine = create_engine(SQLALCHEMY_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
