# 初始化資料庫連線
import os
import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASSWORD") or ""
password = urllib.parse.quote_plus(raw_password)
host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DB_NAME")

uri = f"mongodb+srv://{user}:{password}@{host}/?appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client[db_name]
collection = db.user

try:
    # 強制發送 ping 指令進行實時連線驗證
    client.admin.command('ping')
    print("資料庫連線成功")
except Exception as e:
    print(e)


# 初始化 Flask 伺服器
from flask import *
app = Flask(__name__,static_folder='static',static_url_path='/')

# 設定 Session 的密鑰
app.secret_key="asdfghjkl"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "username" in session:
        return render_template("member.html")
    return redirect(url_for("index"))

# /error?msg=錯誤訊息
@app.route("/error")
def error():
    message = request.args.get("msg","發生錯誤，請聯繫客服")
    return render_template("error.html",message=message)

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    result = collection.find_one({
        "email":email
    })
    if result:
        return redirect(url_for("error",msg="信箱已經被註冊"))
    collection.insert_one({
        "username":username,
        "email":email,
        "password":password
    })
    return redirect(url_for("index"))

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")
    result = collection.find_one({
        "email":email,
        "password":password
    })
    if result:
        session["username"] = result["username"]
        return redirect(url_for("member"))
    return redirect(url_for("error",msg="帳號或密碼輸入錯誤"))

@app.route("/signout")
def signout():
    session.pop("username",None)
    return redirect(url_for("index"))



# uv run flask run --debug --port 3000
