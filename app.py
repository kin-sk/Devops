from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import json

# Flaskアプリの初期化
app = Flask(__name__)

# JSONファイルのパス
DATA_FILE = "data.json"

# 設定をJSONから読み込む
def load_config():
    with open("config.json", "r") as file:
        return json.load(file)

# 設定をJSONから読み込む
def load_data(file_path="data.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"profile": {}, "projects": []}

# JSONに書き込む
def save_data(data, file_path="data.json"):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
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

# ユーティリティ関数
def load_data(file_path=DATA_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"profile": {}, "projects": []}

def save_data(data, file_path=DATA_FILE):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# ホームページ
@app.route("/")
def home():
    data = load_data()
    return render_template("profile.html", profile=data["profile"])

# 履歴書ページ
@app.route("/resume")
def resume():
    return render_template("resume.html")

# プロジェクトページ
@app.route("/project")
def project():
    return render_template("project.html")

# お問い合わせページ
def contact():
    return render_template("contact.html")

@app.route("/submit_contact", methods=["POST"])
def submit_contact():
    # フォームからのデータを取得
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    # データを確認 (開発用)
    print(f"姓: {first_name}, 名: {last_name}, メール: {email}, 件名: {subject}, 内容: {message}")

    # TODO: データを保存するか、メールで送信する

    # ユーザーをサンクスページにリダイレクト
    return redirect(url_for("thank_you"))

@app.route("/thank_you")
def thank_you():
    return "<h1>お問い合わせありがとうございました！</h1>"

# プロジェクトの追加
@app.route("/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        new_project = {
            "title": request.form["title"],
            "description": request.form["description"],
            "image_url": request.form["image_url"]
        }
        data = load_data()
        data["projects"].append(new_project)
        save_data(data)
        return redirect(url_for("home"))
    return render_template("add_project.html")

if __name__ == "__main__":
    app.run(debug=True)