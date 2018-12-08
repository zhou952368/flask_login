import datetime
import os

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, DOCUMENTS, configure_uploads


def init_ext(app):
    # 配置session
    init_session(app)
    # 配置cookie
    inti_cookie(app)
    # 配置缓存
    init_cache(app)
    # 邮件
    init_email(app)
    # 数据库
    init_db(app)
    # 用户系统
    init_login(app)
    # 文件上传
    init_upload(app)


# 实例化SQLAlchemy  全局变量  方便其他模块引用
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
cache = Cache()
# 实例化登录对象
lm = LoginManager()


# 初始化数据库操作
def init_db(app):
    # 配置数据库的链接地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:952368@127.0.0.1:3306/flask_account?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 打印sql语句
    app.config['SQLALCHEMY_ECHO'] = True
    # 懒加载
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)


def init_login(app: Flask):
    lm.login_view = '/account/login/'
    lm.session_protection = 'strong'
    lm.init_app(app)


"""
session 存储的位置
cookie 相关配置
"""


def init_email(app):
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_PORT'] = 25
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '15571383682@163.com'
    app.config['MAIL_PASSWORD'] = 'zhou952368'


def init_cache(app: Flask):
    cache.init_app(app, config={
        # 使用redis数据库作为缓存
        'CACHE_TYPE': 'redis',
        # IP
        'CACHE_REDIS_HOST': '127.0.0.1',
        # 端口
        'CACHE_REDIS_PORT': '6379',
        # redis数据库的索引号
        'CACHE_REDIS_DB': '1',
    })


# session配置
def init_session(app: Flask):
    # 配置加密session数据的秘钥
    app.config['SECRET_KEY'] = 'zhoujianan123456789'
    # 表示使用redis数据库来存储session信息
    app.config['SESSION_TYPE'] = 'redis'
    # 设置session的过期时间  默认关闭浏览器session失效
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(weeks=1)


def inti_cookie(app: Flask):
    app.config['REMEMBER_COOKIE_NAME'] = ''
    # 设置过期时间  默认365天
    app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(weeks=1)
    # 路径
    app.config['REMEMBER_COOKIE_PATH'] = '/'
    # 域名


"""
文件上传
pip install flask-uploads
post 请求 form-data
uploadSet  文件上传的核心对象
name 上传文件的子目录 默认为files
extensions  上传文件的类型(扩展名)  默认是TXT+IMAGES+DOCUMENTS

"""

# 上传图片
img_set = UploadSet(name='images', extensions=IMAGES)
# 上传文档文件
doc_set = UploadSet(name='doc', extensions=DOCUMENTS)
BASE_DIR = os.path.dirname(__file__)
UPLOAD_ROOT_PATH = os.path.join(BASE_DIR, 'static/upload')


def init_upload(app: Flask):
    # 上传文件的根目录
    app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_ROOT_PATH
    # 配置上传文件的最大长度
    app.config['MAN_CONTENT_LENGTH'] = 10 * 1024 * 1024
    # 生成图片的url地址
    app.config['UPLOADS_DEFAULT_URL'] = '/static/upload'
    # 初始化img_set
    configure_uploads(app, img_set)
    # 初始化doc_set
    configure_uploads(app, doc_set)
