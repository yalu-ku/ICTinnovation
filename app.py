## Flask
import os

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

from flask import session


@app.route('/', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = request.form
        print(form)
        id = form['id']
        phone = form['phone']
        addr = form['addr']
        if id == '' and phone == '' and addr == '':
            return redirect('/join')

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        sql = "SELECT * FROM customer WHERE id = '%s' and phone = '%s' and addr = '%s'" % (id, phone, addr)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        if result[0] == 'id' and result[1] == phone and result[2] == addr:
            session['id'] = result[0]

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('order')


@app.route('/join', methods=['get', 'post'])
def join():
    if request.method == "GET":
        return render_template('join.html')
    else:
        form = request.form
        print(form)
        user_id = form['user_id']
        user_ph = form.get('user_ph')
        user_addr = form.get('user_addr')

        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        sql = '''insert into customer (id, phone, addr)
                values (?, ?, ?)'''
        cursor.execute(sql, (user_id, user_ph, user_addr))

        conn.commit()
        cursor.close()
        cursor.close()

        return redirect('/')
        # return '가입완료! {}님 반갑습니다.'.format(user_id)


@app.route('/order', methods=['get', 'post'])
def order():
    if request.method == 'GET':
        return render_template('order.html')
    else:  # POST
        request.form.get('checkbox')
        return render_template('order_complete.html')


@app.route('/write', methods=['get', 'post'])
def write():
    if request.method == 'GET':
        return render_template('write.html')
    else:
        form = request.form
        do = form['do']
        detail = form['detail']

        # 세션 생성
        db_session = scoped_session(
            sessionmaker(bind=engine, autocommit=False, autoflush=False))
        lau = laundry()
        lau.do = '일반세탁'
        lau.price = '3000'

        db_session.add(lau)
        db_session.commit()
        db_session.close()

    return 'ok2'


@app.route('/popup')
def popup():
    return render_template('popup.html')


@app.route('/save_session/<username>')
def save_session(username):
    session['username'] = username
    return '<h1>Save %s</h1>' % username


@app.route('/read_session')
def read_session():
    username = ''
    try:
        username = session['username']
    except KeyError as e:
        username = 'Unknown'
        return '<h1>Read %s</ha>' % username


@app.route('/use_js')
def use_js():
    return render_template('use_js.html')


@app.route('/use_css')
def use_css():
    return render_template('use_css.html')


from flask.wrappers import Response


@app.route('/res')
def res():
    result = Response('Response test')
    # result.content_type = 'application/json' #pdf
    # result.content_type = 'text/html' #/plain
    result.headers.add('webapp-name', 'Test')
    return result


from sqlalchemy import create_engine

# 1. 사용하고자 하는 데이터베이스의 종류 지정
# engine = create_engine('mysql+mysql://ict:1234@127.0.0.1:3366/flask')
engine = create_engine('sqlite:///data.db')

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# 2. Base 객체 생성
BASE = declarative_base()


# 3. 테이블에 해당하는 클래스를 작성
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     phone = Column(String(10), nullable=False)
#     addr = Column(String(30), unique=True)
#
#     def __init__(self, id=None, addr=None):
#         self.id = id
#         self.addr = addr


class customer(BASE):
    __tablename__ = 'customer'
    id = Column(String, primary_key=True)
    phone = Column(String)
    addr = Column(String)


class laundary(BASE):
    __tablename__ = 'laundary'
    lno = Column(Integer, primary_key=True)
    do = Column(String(20))
    price = Column(String(10))


BASE.metadata.create_all(bind=engine)  # 테이블 생성

from sqlalchemy.orm import scoped_session, sessionmaker


@app.route('/insert')
def insert():
    form = request.args
    name = form['name']
    try:
        conn = connect_db()
        sql = 'insert into member (name) valuse (?)'
        # cursor = conn.cursor()
        conn.execute(sql, (name,))
        conn.commit()
        # cursor.close()
        conn.close()
    except Exception as e:
        print(e)
    return 'ok'


@app.route('/append')
def append():
    db_session = scoped_session(
        sessionmaker(bind=engine, autocommit=False, autoflush=False))
    cus = customer()
    cus.id = 'rong'
    cus.phone = '010-1234-1234'
    cus.addr = '신림동'

    db_session.add()
    db_session.commit()
    db_session.close()


@app.route('/add')
def add():
    # 활용 1. session 생성
    db_session = scoped_session(
        sessionmaker(
            bind=engine, autocommit=False, autoflush=False))

    # 활용 2. (데이터 추가 시) 클래스 생성 + 데이터 대입
    u = customer('id', 'phone')
    u.id = 'aro123'
    u.phone = '010-xxxx-xxxx'

    # 활용 3. 세션의 add 함수로 데이터 임시 저장
    db_session.add(u)  # Pending 상태로 저장

    # 활용 4. 임시 저장된 데이터를 영구적인 저장, 접속 종료
    db_session.commit()  # Pending 상태를 Persist 상태로 저장
    db_session.close()

    return 'ok'


DATABASE = 'my.db'
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


# Base = declarative_base()


@app.route('/select')
def select_db():
    try:
        conn = connect_db()
        sql = 'select * from member'
        cursor = conn.execute(sql)
        result = cursor.fetchall()
        # result = [ dict(name=r) for r in result ]
        conn.close()
    except Exception as e:
        print(e)
    return json.dumps(result, ensure_ascii=False)


# @app.route('/')
# def index():
#     return render_template('index.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


import sqlite3

from flask import json


@app.route('/join_complete', methods=['get', 'post'])
def join_complete():
    if request.method == 'GET':
        return render_template('join_complete.html')
    # else:
    #     return render_template('join_complete.html', **locals())


@app.route('/laundry')
def laundry():
    return render_template('laundry.html')


@app.route('/laundry_check.html')
def laundry_check():
    return render_template('laundry_check.html')


@app.route('/log_check', methods=['get', 'post'])
def log_check():
    return render_template('log_check.html')


basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'asdfqer1234'

# db.init_app(app)
# db.app = app
# db.create_all()

from datetime import timedelta

if __name__ == '__main__':
    app.secret_key = 'any random string'
    app.permanent_session_lifetime = timedelta(minutes=10)
    app.run()
