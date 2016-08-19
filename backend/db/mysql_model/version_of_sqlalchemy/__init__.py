# coding:utf-8

import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

db_mysql = create_engine(config.BACKEND_MYSQL)
BaseModel = declarative_base()
DBSession = sessionmaker(bind=db_mysql)
