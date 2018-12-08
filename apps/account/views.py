from operator import or_

from flask import Blueprint, render_template, redirect, request
from flask_login import login_required, logout_user, login_user

from apps.account.models import User
from apps.ext import db, lm

account = Blueprint('account', __name__, template_folder='templates')


# 插件必须要实现的方法 session获取用户的对象
@lm.user_loader
def load_user(uid):
    return User.query.get(uid)


@account.route('/login/', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('account.html')
    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        users = User.query.filter(User.username == username)
        if users:
            if users.first() and users.first().is_active:
                user = users.first()
                if user.verify_password(password):
                    login_user(user, remember=True)
                    return render_template('index.html', msg='登录成功!!!')
                else:
                    return render_template('account.html', msg='账号或者密码有误,请重新输入!!!!')
            else:
                return render_template('account.html', msg='账号未激活,请激活后再登录!!!')
        else:
            return render_template('account.html', msg='用户不存在,请先注册在登录!!!')


@account.route('/register/', methods=['get', 'post'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')
        phone = request.values.get('phone')
        email = request.values.get('email')
        if username and password and phone:
            user = User.query.filter(or_(User.username == username, User.phone == phone)).first()
            if user:
                return render_template('register.html', msg='该用户名或者电话号码已经注册过了!!!')
            else:
                user = User(username=username, password=password, phone=phone, email=email, _is_active=0)
                db.session.add(user)
                db.session.commit()
                return render_template('index.html', msg='注册成功!!!')
        else:
            return render_template('register.html', msg='注册失败,请核对您的输入!!!!')


@account.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


@account.route('/')
def index():
    return render_template('index.html')
