from apps.ext import db
from flask_login import UserMixin
from passlib.apps import custom_app_context

"""
如果使用当前user对象作为登录模块的模型
必须提供
is_active
is_authenticated
is_anonymous
"""


class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    phone = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128), nullable=False)
    _is_active = db.Column(db.Boolean, default=False)
    is_delete = db.Column(db.Boolean, default=False)

    @property
    def is_active(self):
        return self._is_active

    def get_id(self):
        return self.uid

    @property
    def password(self):
        return self._password

    # 设置密码  对密码进行加密
    @password.setter
    def password(self, password):
        if password:
            self._password = custom_app_context.encrypt(password)
        else:
            raise Exception('密码为空!!!!')

    # 验证密码
    def verify_password(self, password):
        return custom_app_context.verify(password, self._password)
