import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from io import BytesIO
from PIL import Image
import os
from flagpy import get_flag_img
from flagpy import FlagIdentifier

"""
    取得したデータから画像生成を行うプログラム
    引数: 取得したデータ(key: value)
    返り値: profile(バイナリデータ)
"""


def generate_profile(data: dict) -> bytes:
    # 画像生成処理
    pass


"""
    入力された国名から国の部分を作成
    引数: 国名
"""


def generate_country(country_name: str, color, world) -> Image.Image:
    # 座標系の確認と変換
    if world.crs is None:
        print("シェープファイルの座標系が未設定です。")
        world = world.set_crs(epsg=4326, allow_override=True)
    else:
        print(f"元の座標系: {world.crs}")
        if world.crs != "EPSG:4326":
            world = world.to_crs(epsg=4326)
            print("座標系をEPSG:4326に変換しました。")
    # 国名カラムの確認
    world["country_name_lower"] = world["NAME"].str.lower()
    country_shape = world[world["country_name_lower"] == country_name.lower()]
    print(country_shape)
    # 地図の描画
    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw={"projection": ccrs.PlateCarree(central_longitude=150)})
    # 世界地図全体を表示
    ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
    map_color = (float(color[0]) / 255.0, float(color[1]) / 255.0, float(color[2]) / 255.0, 0.5)
    # 国を薄い紫色で塗りつぶし、境界線を表示しない
    ax.add_geometries(world["geometry"], crs=ccrs.PlateCarree(), facecolor=map_color, edgecolor="none")
    # 目盛りを消す
    ax.axis("off")
    # 国名が見つからない場合，世界地図を返す
    if country_shape.empty:
        print(f"{country_name.capitalize()} という国は見つかりませんでした。")
        print("利用可能な国名リスト:", world["NAME"].unique())
        flag_img = None
    # 国名が見つかる場合，国旗と世界地図（マーカ付き）を返す
    else:
        # 国の重心を取得
        country_centroid = country_shape.geometry.centroid.iloc[0]
        # 国の中心に赤い点を打つ（投影法を指定）
        ax.plot(country_centroid.x, country_centroid.y, marker="o", color="black", markersize=30, transform=ccrs.PlateCarree())
        # FlagIdentifierのインスタンスを作成
        id = FlagIdentifier()
        # 内部データフレームのインデックスを小文字に変換してリストにする
        # country_list = [country for country in id.flag_df.index.tolist()]
        # print(country_list)
        # エラーハンドリングのための try-except ブロック
        try:
            # 国旗の取得
            if country_name == "United States of America":
                flag_name = "The United States"
            elif country_name == "United Kingdom":
                flag_name = "The United Kingdom"
            # elif country_name not in country_list:
            #     raise ValueError(f"Error: The country '{country_name}' is not in the list.")
            else:
                flag_name = country_name
        except ValueError as e:
            # エラーが発生した後の処理
            print(e)
            # Noneを返す
            return None, None
        flag_img = get_flag_img(flag_name)
        # 国旗の描画
        if flag_img is None:
            print(f"{flag_name.capitalize()} の国旗が見つかりませんでした。")
        # plt.savefig("/app/app/static/data/image/country.png", bbox_inches="tight", pad_inches=0)
    # 画像をバイトストリームに保存し、PIL Imageとして読み込む
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0, transparent=True)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)
    return img, flag_img


if __name__ == "__main__":
    img, flag = generate_country("Japan", (200, 200, 200))
    img.show()
