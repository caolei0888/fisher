# _*_ coding:utf-8 _*_
from flask import Flask
from flask_login import LoginManager

from app.models.base import db
from flask_mail import Mail

login_manager=LoginManager()
mail=Mail()
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view='web.login'
    login_manager.login_message="请先登录或注册"
    mail.init_app(app)
    db.create_all(app=app)
    return app

def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
