# coding=utf-8
__author__ = "hbw"

from db_base import BaseDB, Base
from sqlalchemy import Column, String, Integer, create_engine, Table, DateTime


class Chain(Base, BaseDB):
    id = Column(Integer, primary_key=True)  # 酒店连锁id
    group_name = Column(String(40))     # 酒店集团名
    register_time = Colume(DateTime)       # 注册时间


class Hotel(Base, BaseDB):
    # 表的名字:
    __tablename__ = 'hotel'

    # 表的结构:
    id = Column(Integer, primary_key=True)     # 酒店id
    name = Column(String(40))       # 酒店名
    address = Column(String(40))    # 酒店地址
    manager_name = Column(String(40))   # 酒店超级管理者姓名
    chain_id = Column(Integer)      # 酒店连锁id
    register_time = Colume(DateTime)       # 注册时间

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.password,
            "owner": self.owner,
        }

    # def __init__(self, *args, **kwargs):
    #
    #     super(User, self).__init__(*args, **kwargs)
    #
    def add_user(self, name, password):
        # 创建新User对象:
        new_user = Hotel(name=name, password=password)
        # 添加到session:
        self.db_session.add(new_user)
        # 提交即保存到数据库:
        self.db_session.commit()
        # # 关闭session:
        #.db_session.close()

    def query_user_by_id(self, id):
        objs = self.db_session.query(Hotel).filter(Hotel.id == id).all()
        return [obj.json for obj in objs]

    def query_user_by_name(self, name):
        objs = self.db_session.query(Hotel).filter(Hotel.name == name).all()
        return [obj.json for obj in objs]

    def query_all_user(self):
        objs = self.db_session.query(Hotel).all()
        return [obj.json for obj in objs]

    def delete_by_name(self, name):
        objs = self.db_session.query(Hotel).filter(Hotel.name == name).delete()
        self.db_session.commit()

    def delete_by_id(self, id):
        # 0 error 1 right
        ret = self.db_session.query(Hotel).filter(Hotel.id == id).delete()
        ret_1 = self.db_session.commit()
        print ret
        # print ret_1

    def update_by_name(self, dict):
        self.db_session.query(Hotel).filter(Hotel.id == 1).update(dict)
