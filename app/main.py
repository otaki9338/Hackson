from flask import Flask, render_template
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import ssl

from app.models import init_app
from app.routers.start import start_bp
from app.routers.questions import questions_bp
from app.routers.complete import complete_bp


app = Flask(__name__)
# MongoDBの初期化
load_dotenv()
uri = os.getenv("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(
    uri,
    server_api=ServerApi("1"),
    tls=True,
    tlsAllowInvalidCertificates=False,  # 本番環境では証明書検証を有効にする # 証明書の検証を行わない
)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# app.config['MONGO_URI'] = uri
app.config["MONGO_URI"] = "mongodb://mongo:27017/web_app_db"
init_app(app)
# ルーティングの登録
app.register_blueprint(start_bp)
app.register_blueprint(questions_bp)
app.register_blueprint(complete_bp)


@app.route("/")
def index():
    return render_template("start.html")


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
