# coding=utf-8
__author__ = "hbw"

import functools
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# 创建对象的基类:
Base = declarative_base()


class Single(object):

    obj_list = {}

    def __call__(self, cls):
        @functools.wraps(cls)
        def wraper():
            obj_cls = self.obj_list.get(cls, "")
            if not obj_cls:
                obj_cls = cls()
                self.obj_list[cls] = obj_cls
            return self.obj_list[cls]
        return wraper


@Single()
class DbClient(object):

    @classmethod
    def get_db_client(cls):
        if not hasattr(cls, "_instances"):
            print "create"
            # 初始化数据库连接:
            engine = create_engine('sqlite:///./chat.db')
            # 创建DBSession类型:
            DBSession = sessionmaker(bind=engine)
            cls._instances = DBSession()
        return cls._instances



class BaseDB(object):
    db_session = DbClient().get_db_client()
