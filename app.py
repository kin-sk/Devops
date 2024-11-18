from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import json

app = Flask(__name__)

from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import json

# Flaskアプリの初期化
app = Flask(__name__)

# 設定をJSONから読み込む
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# データベースパスを取得
def get_database_path(env="development"):
    config = load_config()
    relative_path = config[env]["database_path"]
    return os.path.abspath(relative_path)

# データベースの初期化
def initialize_database(db_path):
    db_folder = os.path.dirname(db_path)
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # テーブル作成
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        profile TEXT,
        email TEXT NOT NULL,
        phone TEXT
    );

    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        url TEXT,
        technologies TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    connection.commit()
    connection.close()
    print(f"データベースを初期化しました: {db_path}")

# データ取得
def get_data_from_db(query, params=()):
    db_path = get_database_path()
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row  # カラム名でアクセス可能
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    connection.close()
    return rows

# データ登録
def insert_data(query, params):
    db_path = get_database_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()

# ルート: ホームページ
@app.route("/")
def home():
    projects = [
        {"title": "Project 1", "description": "This is project 1", "image_url": "/static/images/project1.jpg"},
        {"title": "Project 2", "description": "This is project 2", "image_url": "/static/images/project2.jpg"}
    ]
    return render_template("index.html", projects=projects)

if __name__ == "__main__":
    app.run(debug=True)