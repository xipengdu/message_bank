from flask import Flask, g, render_template, request

import sklearn as sk
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import base64

### stuff from last class
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('hello.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/view')
def view():
    result = random_messages(5)
    return render_template('view.html', result = result)

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    get_message_db()
    if request.method == 'GET':
        return render_template('submit.html')     
    else:
        # split successful and error case for inputs. 
        insert_message(request)
        try: 
            insert_message(request)
            return render_template('submit.html', thanks = True, handle = request.form['handle'])
        except:
            return render_template('submit.html', error = True)


def get_message_db():
  # Use create table if not exists to create a message_db with handle and message for text. 
  try:
      return g.message_db
  except:
      g.message_db = sqlite3.connect("messages_db.sqlite")
      cmd = 'CREATE TABLE IF NOT EXISTS messages_table (handle TEXT, message TEXT)' # replace this with your SQL query
      cursor = g.message_db.cursor()
      cursor.execute(cmd)
      return g.message_db

def insert_message(request):
    """
    use sql command insert into table .. values .. to insert input into the database. 
    """
    cmd = f'INSERT INTO messages_table (handle, message) VALUES ("{request.form["handle"]}", "{request.form["message"]}")'
    cursor = g.message_db.cursor()
    cursor.execute(cmd)
    g.message_db.commit()
    pass
    
def random_messages(n): 
    # fetch n elements from the table with random() 
    cmd = f'SELECT * FROM messages_table ORDER BY RANDOM() LIMIT {n};'
    cursor = get_message_db().cursor()
    result = cursor.execute(cmd).fetchall()
    return result

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))