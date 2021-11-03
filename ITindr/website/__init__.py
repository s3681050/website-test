from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from datetime import datetime

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Potato Salad'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    write_to(f'Application-Initialised,\tAttempted,\tSystem')

    from .models import User, ForumPost, Reply

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(email):
         return User.query.get(email)

    return app


def create_database(app):
    try:
        if not path.exists('website/'+DB_NAME):
            db.create_all(app=app)
            log = f'Database-Creation,\tSuccess,\tSystem'
            write_to(log)
    except:
        log = f'Database-Creation,\tFailed,\tSystem'
        write_to(log)


def write_to(log_input):
    log_path = 'website/static/logs/log.txt'
    if not path.exists(log_path):
        file = open(log_path, "a")
        log = f'Log-Created,\tSuccess,\tSystem\t,{datetime.now()}\n'
        file.write(log)
        print(log)
        file.close()
    file = open(log_path, "a")
    currentTime = f',\t{datetime.now()}'
    log = log_input + currentTime
    file.write(log + '\n')
    print(log)
    file.close
