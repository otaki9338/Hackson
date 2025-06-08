from io import BytesIO
import os
import geopandas as gpd

from PIL import Image, ImageDraw, ImageFont
import math
import os
from app.utils.analyze import generate_country

import numpy as np

template_text = {
    "name": "Taro",
    "age": "22",
    "country": "Mali",
    "mbti": "INFJ",
    "favorite": "お肉を食べることが好きです",
    "question1": "aaaaaaaaaaaaaaaaaaaaa",
    "question2": "焼肉としゃぶしゃぶはどっちが好きですか",
    "question3": "question3",
    "answer1": "Aaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "answer2": "麻婆豆腐が好きです！",
    "answer3": "answer",
}

personality_key = ["PositiveMonster", "Active", "JokeStar", "Ambitious", "Passion"]

template_personality = [100, 100, 100, 100, 100]

# 黒，紫，青，赤，緑
sub_color = [(0, 0, 0, 128), (70, 0, 70, 128), (0, 80, 100, 128), (170, 0, 0, 128), (0, 60, 0, 128)]


class Profile:
    def __init__(
        self,
        template_path="/app/app/static/data/image/template",
        font_path="/app/app/static/data/font/HGRPP1.TTC",
        output_path="/app/app/static/data/image/output.png",
        no_image_path="/app/app/static/data/image/no_image.png",
        shape_path="/app/app/static/data/map/ne_110m_admin_0_countries.shp",
        color=1,
        language="ENG",
    ):
        self.template_path = template_path
        self.template = [None, None, None, None]
        for i in range(4):
            self.template[i] = Image.open(os.path.join(self.template_path, f"template{i+1:02d}.png")).convert("RGBA")
        self.color = color
        self.laguage = language
        self.font_path = font_path
        self.output_path = output_path
        self.no_image = Image.open(no_image_path).convert("RGBA").resize((450, 450))
        self.world = gpd.read_file(shape_path)

    def create_profile(self, text_list=template_text, personality=template_personality, picture=None):

        # プロフィール帳のcolorを決定 (color=1:緑・紫, 2:紫・青, 3:黄・赤, 4:青・緑)
        self.deside_color(text_list["mbti"])

        # 国名から世界地図を生成
        country_img, flag_img = generate_country(country_name=text_list["country"], color=sub_color[self.color], world=self.world)

        # プロフィール帳のひな型を作成
        self.output_profile = self.template[self.color - 1]

        self.draw_free_text(text=text_list["name"], position=(750, 836), ancher="right", max_width=250, font_size=80)
        self.draw_free_text(text=text_list["age"], position=(750, 1026), ancher="right", max_width=250, font_size=80)
        self.draw_free_text(text=text_list["favorite"], position=(480, 1380), ancher="center", max_width=540, font_size=80)
        self.draw_free_text(text=text_list["country"], position=(1382, 234), ancher="bottom", max_width=460, font_size=80)
        self.draw_free_text(text=text_list["mbti"], position=(1340, 1521), ancher="center", font_size=80)

        self.draw_free_text(text=text_list["question1"], position=(160, 1750), ancher="left_top", max_width=1040, font_size=60)
        self.draw_free_text(text=text_list["question2"], position=(160, 1960), ancher="left_top", max_width=1040, font_size=60)
        self.draw_free_text(text=text_list["question3"], position=(160, 2170), ancher="left_top", max_width=1040, font_size=60)
        self.draw_free_text(text=text_list["answer1"], position=(1573, 1900), ancher="right_bottom", max_width=820, font_size=60)
        self.draw_free_text(text=text_list["answer2"], position=(1573, 2105), ancher="right_bottom", max_width=820, font_size=60)
        self.draw_free_text(text=text_list["answer3"], position=(1573, 2321), ancher="right_bottom", max_width=820, font_size=60)

        self.draw_face_image(image=picture, position=(178, 192))
        self.draw_country_image(image=country_img, position=(830, 292), image_size=(760, 360))
        self.draw_flag_image(image=flag_img, position=(1500, 260), image_size=(150, 75))
        self.draw_personality(center=(1300, 1160), personality=personality)

        return self.output_profile

    def draw_face_image(self, image, position, target_size=450):
        self.output_profile.paste(self.no_image, position, self.no_image)
        if image is None:
            return
        # 貼り付ける画像のリサイズ
        image = resize_and_crop(image, target_size=target_size).convert("RGBA")
        # 背景画像に貼り付ける
        self.output_profile.paste(image, position, image)

    def draw_country_image(self, image, position, image_size):
        if image is None:
            return
        image = image.resize(image_size).convert("RGBA")
        # 背景画像に貼り付ける
        self.output_profile.paste(image, position, image)

    def draw_flag_image(self, image, position, image_size):
        if image is None:
            return
        image = image.resize(image_size).convert("RGBA")
        # 背景画像に貼り付ける
        self.output_profile.paste(image, position, image)

    def draw_free_text(self, text, position, ancher="center", color=(0, 0, 0), font_size=60, max_width=540):

        text = capitalize_first_letter(text)
        # フォントを定義
        font = ImageFont.truetype(self.font_path, size=font_size)
        draw = ImageDraw.Draw(self.output_profile)
        # テキストのサイズを取得
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]

        # フォントサイズを自動で縮小する処理（二分探索を使用）
        if max_width is not None and text_width > max_width:
            min_size = 1
            max_size = font_size

            while min_size < max_size:
                mid_size = (min_size + max_size) // 2
                font = ImageFont.truetype(self.font_path, size=mid_size)
                text_bbox = draw.textbbox((0, 0), text, font=font, align="center")
                text_width = text_bbox[2] - text_bbox[0]

                if text_width <= max_width:
                    min_size = mid_size + 1
                else:
                    max_size = mid_size - 1

            # 縮小したフォントサイズを最終的に適用
            font_size = min_size - 1

        font = ImageFont.truetype(self.font_path, size=font_size)
        text_bbox = draw.textbbox((position[0], position[1]), text, font=font)

        fixed_position = self.fix_text_positon(position, text_bbox, ancher=ancher)
        # 画像にテキストを描画
        draw.text(fixed_position, text, fill=color, font=font)
        # draw.rectangle(
        #     (
        #         (fixed_position[0], fixed_position[1]),
        #         (fixed_position[0] + text_bbox[2] - text_bbox[0], fixed_position[1] + text_bbox[3] - text_bbox[1]),
        #     ),
        #     outline="black",
        # )

    def fix_text_positon(self, position, text_bbox, ancher="center"):
        fixed_position = position
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # アンカーによるテキスト位置の調整
        if ancher == "center":
            fixed_position = (position[0] - text_width // 2, position[1] - text_height // 2)
        elif ancher == "left":
            fixed_position = (position[0], position[1] - text_height // 2)
        elif ancher == "right":
            fixed_position = (position[0] - text_width, position[1] - text_height // 2)
        elif ancher == "top":
            fixed_position = (position[0] - text_width // 2, position[1])
        elif ancher == "bottom":
            fixed_position = (position[0] - text_width // 2, position[1] - text_height)
        elif ancher == "right_bottom":
            fixed_position = (position[0] - text_width, position[1] - text_height)

        return fixed_position

    def deside_color(self, mbti):
        if mbti in ["ISTJ", "ISFJ", "ESTJ", "ESFJ"]:
            self.color = 4
        elif mbti in ["INTJ", "INTP", "ENTJ", "ENTP"]:
            self.color = 2
        elif mbti in ["ISTP", "ISFP", "ESTP", "ESFP"]:
            self.color = 3
        elif mbti in ["INFJ", "INFP", "ENFJ", "ENFP"]:
            self.color = 1

    def save_profile(self):
        # 結果を保存
        self.output_profile.save("/app/app/static/data/image/output_profile.png")

    def draw_personality(self, center, personality, scale=2.0):

        # 結果を格納するリスト
        radius = []
        # 辞書から値をリストに追加
        for key in personality_key:
            if key in personality:
                radius.append(personality[key])
            else:
                radius.append(100)

        # personalityのvalueを(0, 100)に限定
        radius = np.array(radius).clip(0, 100)

        # 五角形を描画するための新しい画像を作成
        pentagon_image = Image.new("RGBA", self.output_profile.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(pentagon_image)
        # 中心座標を指定
        cx, cy = center

        # 五角形の頂点を計算
        points = []
        for i in range(5):
            angle = math.radians(72 * i - 90)  # 72度ごとに頂点を配置 (-90は最初の頂点を上に向けるため)
            x = cx + scale * radius[i] * math.cos(angle)
            y = cy + scale * radius[i] * math.sin(angle)
            points.append((x, y))

        draw.polygon(points, fill=sub_color[self.color])

        # 五角形画像を元の画像に貼り付け
        self.output_profile = Image.alpha_composite(self.output_profile, pentagon_image)


def resize_and_crop(image, target_size=450):
    # 画像のサイズを取得
    original_width, original_height = image.size

    # アスペクト比を保持してリサイズ
    aspect_ratio = original_width / original_height

    if aspect_ratio > 1:  # 横長の画像
        new_height = target_size
        new_width = int(aspect_ratio * target_size)
    else:  # 縦長または正方形の画像
        new_width = target_size
        new_height = int(target_size / aspect_ratio)

    # 画像をリサイズ
    image = image.resize((new_width, new_height), Image.LANCZOS)

    # クロップする位置を計算（画像の中心を基準）
    left = (new_width - target_size) // 2
    top = (new_height - target_size) // 2
    right = (new_width + target_size) // 2
    bottom = (new_height + target_size) // 2

    # 画像をクロップ
    image = image.crop((left, top, right, bottom))
    return image


def capitalize_first_letter(text):

    if len(text) == 0:
        return text
    else:
        # 1文字目を取得
        first_char = text[0]

        # 1文字目が半角の小文字英字かどうかを確認
        if "a" <= first_char <= "z":
            # 大文字に変換して、残りの文字列と結合
            return first_char.upper() + text[1:]
        else:
            # 変更せずに返す
            return text


if __name__ == "__main__":
    template_path = r"app\static\data\image\template"
    output_path = r"./test/image/output.png"
    font_path = r"app\static\data\font\HGRPP1.TTC"
    no_image_path = r"app\static\data\image\no_image.png"
    shape_path = r"app/static/data/map/ne_110m_admin_0_countries.shp"
    profile = Profile(
        template_path=template_path, output_path=output_path, font_path=font_path, no_image_path=no_image_path, shape_path=shape_path
    )

    output_profile = profile.create_profile(text_list=template_text, picture=None)
    output_profile.show()
