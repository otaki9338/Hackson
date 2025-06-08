import os
import openai
from dotenv import load_dotenv
import logging


load_dotenv()
# ロガーの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# キー取得フラグの初期化
api_key_missing = False

# APIキーの取得
api_key = os.getenv("CHATGPT_API_KEY")
if not api_key:
    print("API key not found. Switch to default mode.")
    api_key_missing = True
else:
    openai.api_key = api_key
    print(openai.api_key)

# client = OpenAI(
#     api_key="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",
# )
"""
    コミュニケーションのきっかけになるような項目が良いかも

    - 話しかけてほしい指数（かまちょ）
    - 天然指数
    - イベント好き（飲み好き）
    - アウトドア，インドア
    - 遊びたい欲
    - 素敵度（高めに設定）
    - 天才指数
    - おしゃべり度
    - 彼氏感，彼女感
    - 母性度合い
    - ネジのハズレ度合い，ぶっ飛び度合い
    - カリスマ性
    - インフルエンス力
    - 頭の回転速度
"""

"""
    age = data['age']
    country = data['country']
    favorite_things = data['favorite_things']
    mbti = data['mbti']
    
    questions_and_answers = {key: value}
"""

def get_personal_specific(data, questions_and_answers):
    # APIキーがない場合はデフォルト値を返す
    if api_key_missing:
        print("Returns default value because API key is not found.")
        logger.warning("Returns default value because API key is not found.")
        return {
            "Ambitious": 80,
            "Passion": 60,
            "JokeStar": 90,
            "Active": 70,
            "PositiveMonster": 80,
        }
    
    # プロンプトの作成
    prompt = f"""
    Based on the following information, please evaluate the five personality traits on a scale of 0 to 100:
    Ambitious 
    Passion
    Joke Star
    Active 
    Positive Monster

    Profile Information:
    - Age: {data['age']}
    - Country of Origin: {data['country']}
    - Interests: {data['favorite_things']}
    - MBTI: {data['mbti']}
    
    Questions and Answers:
    {questions_and_answers}

    Please return the results in a dictionary format with scores out of 100 for each trait.
    """

    # GPT-3.5 APIを呼び出し
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a knowledgeable AI that understands MBTI and can analyze personality traits based on various profile information."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # 辞書形式で結果を返す
    result = response.choices[0].message.content.strip()
    
    # 返り値を辞書形式に変換
    try:
        print(result)
        return eval(result)  # 生成された結果が辞書形式であれば、それを評価して辞書に変換
    except:
        print("Could not parse GPT output as a dictionary.")
        print(result)
        return {
            "Ambitious": 80,
            "Passion": 60,
            "JokeStar": 90,
            "Active": 70,
            "PositiveMonster": 80,
        }
    
    
if __name__ == '__main__':
    # サンプルデータの設定
    sample_data = {
        'age': 25,
        'country': 'Japan',
        'favorite_things': 'プログラミング, 読書, ゲーム',
        'mbti': 'INTJ'
    }

    # サンプル質問と回答の設定
    sample_questions_and_answers = {
        '趣味は何ですか？': 'プログラミングが大好きです。',
        'どんな本を読みますか？': '主にSF小説を読みます。',
        '最近ハマっていることは？': '新しいゲームの開発です。'
    }

    result = get_personal_specific(sample_data, sample_questions_and_answers)

    print("GPT-3.5による数値化結果:")
    for trait, score in result.items():
        print(f"{trait}: {score}")
        