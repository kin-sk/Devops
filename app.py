from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_projects():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, description FROM projects")
    projects = cursor.fetchall()
    connection.close()
    return projects

@app.route('/')
def home():
    projects = get_projects()
    return render_template('index.html', projects=projects)
