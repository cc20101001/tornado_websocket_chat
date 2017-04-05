# coding=utf-8
__author__ = "hbw"

# 导入:
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    password = Column(String(120))

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }
# 初始化数据库连接:
engine = create_engine('sqlite:///./chat.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
db_session = DBSession()
print db_session.query(User).one().json()#.filter(User.id == id).one()