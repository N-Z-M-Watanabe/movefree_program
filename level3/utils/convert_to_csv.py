# convert_to_csv.py

# ◆ 03_店舗情報リストからcsv作成

def lists_convert_csv(data_list, file_name):

    import csv
    import unicodedata
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))  #カレントディレクトリ取得
    file_path = os.path.join(current_dir, "..", file_name)  # 保存するCSVのフルパスを作成

    # shift-jis用の変換関数
    def clean_text(text):
        if text is None:
            return ""

        return unicodedata.normalize("NFKC", str(text))

    # 全店舗リストを変換する
    cleaned_list = []
    for shop in data_list:
        cleaned_row = [clean_text(item) for item in shop]
        cleaned_list.append(cleaned_row)

    with open(file_path, "w", newline="", encoding="shift_jis", errors="replace") as f:
        writer = csv.writer(f)
        # ヘッダー（項目名）を書き込む
        writer.writerow(["店舗名", "電話番号", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])
        writer.writerows(cleaned_list)
