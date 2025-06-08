# from flask import Blueprint, render_template, request, url_for
# from app.models import get_db, User

from flask import Blueprint, render_template, request, url_for
from io import BytesIO
import base64
from app.models import get_db, User

complete_bp = Blueprint("complete", __name__)


@complete_bp.route("/complete", methods=["GET"])
def complete():
    group_name = request.args.get("group_name")
    name = request.args.get("name")

    db = get_db()
    user_model = User(db)
    profile = user_model.get_user_by_name(name)

    image_data = profile.get("profile")
    if image_data:
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        send_profile = {"profile_image_url": f"data:image/png;base64,{image_base64}", "name": profile["name"]}

    return render_template("complete.html", profile=send_profile, group_name=group_name)


@complete_bp.route("/show_group_members", methods=["GET"])
def show_group_members():
    group_name = request.args.get("group_name")

    if not group_name:
        return "Group name is not found", 400

    db = get_db()
    user_model = User(db)
    profiles = user_model.get_user_by_group_name(group_name)

    # プロフィールをユーザー名でグループ化
    grouped_profiles = {}
    for profile in profiles:
        name = profile["name"]
        if name not in grouped_profiles:
            grouped_profiles[name] = []

        # 画像データを取得し、base64エンコードしてHTMLに渡せるようにする
        image_data = profile.get("profile")
        if image_data:
            image_base64 = base64.b64encode(image_data).decode("utf-8")
            grouped_profiles[name].append({"profile_image_url": f"data:image/png;base64,{image_base64}", "name": profile["name"]})

    return render_template("group_member.html", profiles=grouped_profiles, group_name=group_name)
