from flask import Blueprint, request, redirect, url_for, current_app
from flask import Blueprint, render_template, request
from io import BytesIO
from flask import jsonify

from app.models import get_db, User
from app.utils.analyze import generate_country
from app.utils.profile import Profile
from app.utils.gpt_integration import get_personal_specific

from PIL import Image
import base64


questions_bp = Blueprint("questions", __name__)


@questions_bp.route("/questions", methods=["POST"])
def questions():
    # JSON形式で送られてきたデータ（質問項目とその回答）
    data = request.json

    group_name = data["group_name"]
    name = data["name"]
    age = data["age"]
    country = data["country"]
    favorite_things = data["favorite_things"]
    mbti = data["mbti"]

    image_data_url = data.get("image", None)
    if image_data_url:
        image_data = base64.b64decode(image_data_url.split(",")[1])
        # デバック用に画像を保存
        # with open("/app/app/static/data/image/captured_image.png", "wb") as f:
        #     f.write(image_data)
        #     data["image"] = image_data

        # 画像をRGB形式に変換
        picture = Image.open(BytesIO(image_data))

    # 上記のデータ以外は質問とその回答
    questions_and_answers = {
        key: value for key, value in data.items() if key not in ["group_name", "name", "age", "country", "favorite_things", "mbti", "image"]
    }
    questions = list(questions_and_answers.keys())
    answers = list(questions_and_answers.values())

    # 国の地図を取得
    # country_map, flag = generate_country(country)

    text_list = {
        "name": name,
        "age": age,
        "country": country,
        "mbti": mbti,
        "favorite": favorite_things,
        "question1": questions[0] if len(questions) > 0 else "",
        "question2": questions[1] if len(questions) > 1 else "",
        "question3": questions[2] if len(questions) > 2 else "",
        "answer1": answers[0] if len(answers) > 0 else "",
        "answer2": answers[1] if len(answers) > 1 else "",
        "answer3": answers[2] if len(answers) > 2 else "",
    }

    # グラフようの値を取得(dict)
    personal_specific = get_personal_specific(data, questions_and_answers)
    # with open("/app/app/static/data/test.txt", "w") as f:
    #     f.write("Personal Specific\n")
    #     for trait, value in personal_specific.items():
    #         f.write(f"{trait}: {value}\n")
    #         print(f"{trait}: {value}")
    print(personal_specific)

    # 取得したデータを元にプロフィールを作成, バイナリーデータに変換
    profiler = Profile()
    profile = profiler.create_profile(
        text_list=text_list,
        personality=personal_specific,
        picture=picture,
    )
    buffer = BytesIO()
    profile.save(buffer, format="PNG")
    profile_data = buffer.getvalue()

    # MongoDBに接続し，Userクラスのインスタンスを作成
    db = get_db()
    user_model = User(db)

    # MongoDBにデータを格納
    result = user_model.create_user(
        group_name=group_name,
        name=name,
        age=age,
        country=country,
        favorite_things=favorite_things,
        mbti=mbti,
        image_data=image_data,
        questions_and_answers=questions_and_answers,
        profile=profile_data,  # バイナリデータとして保存
    )

    # MongoDBへの挿入が成功したか確認
    if result.acknowledged:
        # profileの生成が終了したら，別のURLに切り替える
        return jsonify({'message': 'Profile created', 'group_name': group_name, 'name':name}), 200
    else:
        return jsonify({'message': 'Failed to create profile'}), 500



if __name__ == "__main__":
    generate_country("Japan")
