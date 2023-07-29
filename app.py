import os

from loguru import logger

from flask import Flask, render_template, g
import sqlite3
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(data=os.path.join(app.root_path, 'instance/test.db')))
socket = SocketIO(app)


def connect_db():
    conn = sqlite3.connect(app.config['data'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@socket.on("filter")
def filter(data):
    query = f"""
        SELECT *
        FROM courses
        WHERE 
        {data['field']} = '{data['value']}' 
    """

    db = connect_db()
    filtered_courses = db.cursor().execute(query).fetchall()

    logger.info(filtered_courses)

    for course in filtered_courses:
        emit("filter", dict(course))


if __name__ == "__main__":
    socket.run(app, debug=True)