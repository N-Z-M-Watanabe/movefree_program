# 標準ライブラリを読み込む
import datetime
import os
import random

# 今日の日付を取得（datetime.date）
today: datetime.date = datetime.date.today()

# 日付を文字列「yyyy-mm-dd」に変換
date_str: str = today.strftime("%Y-%m-%d")

# カレントディレクトリに「yyyy-mm-dd」フォルダを作成
# exist_ok=True にしてフォルダがあってもエラーにならないようにする
os.makedirs(date_str, exist_ok=True)

# 1〜100の中からランダムな整数を1つ生成
lucky_number: int = random.randint(1, 100)

# 作成するテキストファイルのパスを指定
file_path: str = os.path.join(date_str, "kadai4-2.txt")

# テキストファイルを作成し、ラッキーナンバーを書き込む
with open(file_path, "w", encoding="utf-8") as file:
    file.write(f"今日のラッキーナンバーは「{lucky_number}」です！")