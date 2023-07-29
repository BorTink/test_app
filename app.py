from flask import Flask, render_template, g
import sqlite3
from flask_socketio import SocketIO, emit
import os

from loguru import logger

app = Flask(__name__)

app.config.from_object(__name__)

app.config.update(dict(data=os.path.join(app.root_path, 'instance/test.db')))


def connect_db():
    conn = sqlite3.connect(app.config['data'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


basedir = os.path.abspath(os.path.dirname(__file__))


socket = SocketIO(app)


@app.route('/', methods=['POST', 'GET'])
def home():
    db = get_db()
    return render_template('home.html', menu = [])


@socket.on("filter")
def filter(data):
    query = f"""
        SELECT *
        FROM courses
        WHERE 
        {data['field']} = '{data['value']}' 
    """

    db = get_db()
    filtered_courses = db.cursor().execute(query).fetchall()

    logger.info(filtered_courses)
    db.close()

    for course in filtered_courses:
        emit("filter", dict(course))


if __name__ == "__main__":
    socket.run(app, debug=True)