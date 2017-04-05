# coding=utf-8
__author__ = "hbw"

from db_base import BaseDB, Base
from sqlalchemy import Column, String, Integer


class User(Base, BaseDB):
    # 表的名字:
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    wx_num = Column(String(40))     #微信号
    name = Column(String(40))       # 个人姓名
    password = Column(String(40))   # 密码
    phone_num = Column(String(40))  # 手机号
    idcard_num = Column(String(40))     # 身份证号码
    birthday = Column(String(40))   # 生日
    address = Column(String(40))    # 居住地
    role = Column(String(40))   # super_admin 10, admin 8,  customer 0, employee 1
    is_vip = Column(String(40))   # 不是 0, 是 1
    vip_point = Column(Integer)     # 会员积分
    head_pic_id = Column(Integer)   # 头像图片id号

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
        }

    # def __init__(self, *args, **kwargs):
    #
    #     super(User, self).__init__(*args, **kwargs)
    #
    def add_user(self, name, password):
        # 创建新User对象:
        new_user = User(name=name, password=password)
        # 添加到session:
        self.db_session.add(new_user)
        # 提交即保存到数据库:
        self.db_session.commit()
        # # 关闭session:
        #.db_session.close()

    def query_user_by_id(self, id):
        objs = self.db_session.query(User).filter(User.id == id).all()
        return [obj.json for obj in objs]

    def query_user_by_name(self, name):
        objs = self.db_session.query(User).filter(User.name == name).all()
        return [obj.json for obj in objs]

    def query_all_user(self):
        objs = self.db_session.query(User).all()
        return [obj.json for obj in objs]

    def delete_by_name(self, name):
        objs = self.db_session.query(User).filter(User.name == name).delete()
        self.db_session.commit()

    def delete_by_id(self, id):
        # 0 error 1 right
        ret = self.db_session.query(User).filter(User.id == id).delete()
        ret_1 = self.db_session.commit()
        print ret
        # print ret_1

    def update_by_name(self, dict):
        self.db_session.query(User).filter(User.id == 1).update(dict)


# User().add_user("123123", "234234")
User().update_by_name({"name": "23232332232"})

users = User().query_all_user()
print len(users)
for one in users:
    print one
