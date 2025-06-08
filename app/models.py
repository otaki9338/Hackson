from bson.binary import Binary
from pymongo import MongoClient
from flask import current_app, g


def get_db():
    if "mongo_client" not in g:
        g.mongo_client = MongoClient(current_app.config.get("MONGO_URI"))  # 新しいMongoClientインスタンスを作成し、gオブジェクトに格納
    return g.mongo_client.web_app_db


def close_db(e=None):
    mongo_client = g.pop("mongo_client", None)
    if mongo_client is not None:
        mongo_client.close()  # MongoDBクライアントを閉じる


# Faskの初期化
def init_app(app):
    app.teardown_appcontext(close_db)  # アプリケーションコンテキストが終了するときにclose_db関数を呼び出す


"""
    MongoDBには複数のCollection(Tableみたいなもの)
    CollectionにはDocumentが格納され，JSON形式でデータを格納
"""


class User:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, group_name, name, age, country, favorite_things, mbti, image_data, questions_and_answers, profile):
        user_data = {
            "group_name": group_name,
            "name": name,
            "age": age,
            "country": country,
            "favorite_things": favorite_things,
            "mbti": mbti,
            "image": Binary(image_data) if image_data is not None else None,  # 画像データをバイナリ形式で格納
            "questions_and_answers": questions_and_answers,
            "profile": profile,
        }
        return self.collection.insert_one(user_data)

    def get_user_by_name(self, name):
        return self.collection.find({"name": name}).sort("_id", -1).limit(1).next()

    # 返り値 :  (pymongo.cursor.Cursor) 全てのドキュメントを含む
    def get_user_by_group_name(self, group_name):
        return self.collection.find({"group_name": group_name})

    """
        MBTIでグループ分けとかもあり
    """
