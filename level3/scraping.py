import requests
from bs4 import BeautifulSoup
import time

# ユーザーエージェント設定
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# 1.ぐるなび店舗一覧ページから店舗ページのURL取得-------------------

# 店舗のURLリストを取得する関数定義
def get_shop_urls(url):

    time.sleep(3)

    res = requests.get(url, headers=headers)   # URLからサイトのHTML情報を取得
    res.encoding = res.apparent_encoding  # 取得した情報を自動でエンコード
    bs_date = BeautifulSoup(res.text,"html.parser")  # HTMLパーサーを使用し取得した情報をテキストとして解析

    # 解析したデータの中で、特定のクラスのaタグを全て取得する
    shops_list = bs_date.find_all("a", class_="style_titleLink___TtTO")

    urls = []

    for a_tag in shops_list:
        shop_url = a_tag.get("href")
        urls.append(shop_url)

    return urls


# 関数呼び出し
url1 = "https://r.gnavi.co.jp/area/jp/rs/"
url_list = get_shop_urls(url1)

list1 = get_shop_urls(url1)

url2 = "https://r.gnavi.co.jp/area/jp/rs/?p=2"
list2 = get_shop_urls(url2)

# 取得した店舗ページURLのリスト統合、URLの件数を50にする
url_list = list1 + list2
del url_list[50:]


# 2.取得したURLのリストから店舗情報を取得-------------------

# 最終的に全店舗情報を格納するリスト
all_shops_list = []

for info_url in url_list:

    time.sleep(3)

    res = requests.get(info_url, headers=headers)
    
    res.encoding = res.apparent_encoding
    
    bs_data = BeautifulSoup(res.text, "html.parser")

    # 1 店舗名取得
    shop_name_tag = bs_data.find("table", class_="basic-table").find("p", id="info-name")
    shop_name = shop_name_tag.text
    
    # 2 電話番号取得
    shop_tel_tag = bs_data.find("table", class_="basic-table").find("span", class_="number")
    shop_tel = shop_tel_tag.text
    
    # 3 住所取得
    shop_addr_tag = bs_data.find("table", class_="basic-table").find("span", class_="region")
    shop_addr = shop_addr_tag.text
    
    # >>> 取得した住所を分割して辞書型にする
    from normalize_japanese_addresses import normalize
    dic = normalize(shop_addr)
    addr_list = [ dic['pref'], dic['city'] + dic['town'], dic['addr'] ]
    
    # 4 建物名取得
    shop_building_tag = bs_data.find("table", class_="basic-table").find("span", class_="locality")
    if shop_building_tag:
        shop_building = shop_building_tag.text
    else:
        shop_building = ""

    
    # 5 URL取得
    sv_site_ul = bs_data.find("ul", id="sv-site")

    # ul→li→aタグの順で確認して取得
    if sv_site_ul:
        clickable_li = sv_site_ul.find("li", class_="clickable")
    
        if clickable_li and clickable_li.find("a"):
            shop_check_url = clickable_li.find("a").get("href")
        else:
            shop_check_url = "" # aタグがなければ空欄
    else:
        shop_check_url = "" # ulがなければ空欄

    
    # 正式なURLを取得、SLLを確認
    def check_site(url):
        try:
            
            time.sleep(3)

            res_move = requests.get(shop_check_url, timeout=10)

            # 転送先のURLを取得
            shop_url = res_move.url

            # 6 SSLの確認
            is_ssl = shop_url.startswith("https://")

            return shop_url, is_ssl

        except requests.exceptions.RequestException as e:
            # サイトが開けなかった場合のエラー処理
            print(f"転送先サイトでエラーが発生しました: {e}")
            return None, False

    target_url = shop_check_url
    shop_url, ssl_status = check_site(target_url)
    
    # 1店舗の情報をリストにまとめる
    shop_info_list = [shop_name, shop_tel] + addr_list + [shop_building, shop_url, ssl_status]
    print(shop_info_list)
    
    all_shops_list.append(shop_info_list)

    print(f"追加店舗: {shop_name}")


# 3.取得した店舗のリストをcsvに書き込み-------------------

import csv
import unicodedata

# shift-jis用の変換関数
def clean_text(text):
    if text is None:
        return ""

    return unicodedata.normalize("NFKC", str(text))

file_path = "./shop_data.csv"

# 作成した全店舗リストを変換する
cleaned_all_shops_list = []
for shop in all_shops_list:
    cleaned_row = [clean_text(item) for item in shop]
    cleaned_all_shops_list.append(cleaned_row)

with open(file_path, "w", newline="", encoding="shift_jis", errors="replace") as f:
    writer = csv.writer(f)
    # ヘッダー（項目名）を書き込む
    writer.writerow(["店舗名", "電話番号", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])
    writer.writerows(cleaned_all_shops_list)

print("CSVファイルへの書き出しが完了しました。")