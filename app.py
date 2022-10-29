from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash
import os, sys

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class Config:
    DEBUG = False
    TESTING = False
    SSL_REDIRECT = False

    SECRET_KEY = os.getenv("SECRET_KEY", "hard-to-guess")

    SQLALCHEMY_POOL_RECYCLE = 10
    SQLQLCHEMY_POOL_SIZE = 30
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))

    REMEMBER_COOKIE_DURATION = timedelta(days=14)


app.config.from_object(Config)
bootstrap = Bootstrap5(app)

db = SQLAlchemy()
db.init_app(app)

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(16))
    name = db.Column(db.String(20))
    password_hash = db.Column(db.String)
    email = db.Column(db.String(256))

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    remote_addr = db.Column(db.String)

    color = db.Column(db.String(7))

    verified = db.Column(db.Boolean)

    capital = db.Column(db.String)

    def __str__(self):
        return f"<User '{self.username}'>"

    def set_password(self, pwd):
        pwd_hash = generate_password_hash(pwd)
        self.password_hash = pwd_hash
        db.session.commit()

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    def gen_email_verify_token(self):
        header = {"alg": "HS256"}
        payload = {"uid": self.id, "email": self.email, "time": time()}
        token = jwt.encode(header, payload, current_app.config["SECRET_KEY"]).decode(
            "utf-8"
        )
        return token


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/construction_site')
def construction_site():
    return render_template('construction_site.html')


@app.route('/playground')
def playground():
    return render_template('playground.html')


@app.route('/register', methods=("GET", "POST",))
def register():
    if request.method == "POST":
        f = request.form
        username = f.get("username")
        email = f.get("email")
        name = f.get("name")
        pwd = f.get("pwd")
        color = f.get("color")
        interest = f.get("interest")

        u = User()
        u.username = username
        u.email = email
        u.name = name
        u.color = color
        u.interest = interest
        u.set_password(pwd)

        u.remote_addr = request.remote_addr
        u.verified = False

        u.capital = "10000.0"

        db.session.add(u)
        db.session.commit()

    return render_template('register.html')
