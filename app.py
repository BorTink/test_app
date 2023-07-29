from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import select, create_engine, text
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bruhh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'


socket = SocketIO(app)

db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@socket.on("filter")
def filter(data):
    # print('ASDSAODHASOIDHASOID ' + data['field'] + " " + data['value'])

    # print(type(Courses))

    # statement = f"SELECT * FROM courses WHERE {data['field']} = \"{data['value']}\""

    # with engine.connect() as conn:
    #     result = conn.execute(
    #         text(statement)
    #     )

    emit("filter", data)


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    topic = db.Column(db.String(150))
    field = db.Column(db.String(150))
    university = db.Column(db.String(150))


if __name__ == "__main__":
    with app.app_context():
        engine = create_engine('sqlite:///test.db')
        db.create_all()
    

    socket.run(app, debug=True)