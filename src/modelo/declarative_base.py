from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

engine = create_engine('sqlite:///baseDatosSoftOne.sqlite', poolclass=SingletonThreadPool)

Session = sessionmaker(bind=engine)

Base = declarative_base()