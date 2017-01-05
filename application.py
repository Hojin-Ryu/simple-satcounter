from flask import Flask, g, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect("entry.db")
    return db

@app.teardown_appcontext
def close_connection(expn):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()





@app.route('/')
def index():
    countdown = datetime(2017, 11, 16) - datetime.now()
    dday = countdown.days

    db = get_db()
    comments = db.execute("SELECT * FROM entries LIMIT 10").fetchall()
    return render_template('index.html', countdown=dday, comments=comments)


@app.route('/new_comment')
def new_comment():
    return render_template('write.html')


@app.route('/new_comment', methods=['POST'])
def post_comment():

    db = get_db()
    db.execute(
        "INSERT INTO entries (writer, content) VALUES (?, ?)",
        (request.form['writer'], request.form['content'])
        )
    db.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
