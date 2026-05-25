# 初始化資料庫連線
import os
import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ConfigurationError
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MONGO_USER")
raw_password = os.getenv("MONGO_PASSWORD") or ""
password = urllib.parse.quote_plus(raw_password)
host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DB_NAME")

uri = f"mongodb+srv://{user}:{password}@{host}/?appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

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




# uv run flask run --debug --port 3000
