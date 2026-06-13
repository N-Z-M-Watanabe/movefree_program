# scraping.py

import requests
from bs4 import BeautifulSoup
import time
from normalize_japanese_addresses import normalize
import csv
import unicodedata
import logging
import os
import sys
from utils.convert_to_csv import lists_convert_csv

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# ログ設定
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # すべてのレベルのログを記録対象する

# logsディレクトリの作成
current_dir = os.path.dirname(os.path.abspath(__file__))  #カレントディレクトリ取得
log_dir_path = os.path.join(current_dir, "logs") # カレントディレクトリ+logsファイルのパスを変数化
os.makedirs(log_dir_path, exist_ok=True) # ログ保存用フォルダ作成
log_file_fullpath = os.path.join(log_dir_path, "scraping_log.txt")

sh = logging.StreamHandler()  # 画面（コンソール）出力設定
sh.setLevel(logging.INFO)  # 画面にはINFO以上のログを出力

fh = logging.FileHandler(log_file_fullpath, encoding="utf-8")  # ファイル保存用設定
fh.setLevel(logging.DEBUG)  # ファイルにはDEBUGも含めてすべて記録

# ログフォーマット「日時 - ログの重要度 - メッセージ」
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)
fh.setFormatter(formatter)

# ロガーに2つのハンドラを追加
logger.addHandler(sh)
logger.addHandler(fh)


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# スクレイピング共通設定
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ユーザーエージェント設定
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 関数定義
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ◆◆◆ 01_店舗URLリスト作成 ◆◆◆
# ー引数：店舗一覧のURL
# ー戻り値：店舗ページURLのリスト

def get_shop_urls(url):

    try:
        time.sleep(3)
        res = requests.get(url, headers=headers, timeout=10)  # URLからサイトのHTML情報を取得
        res.raise_for_status()  # エラーチェック(ステータス200以外はエラーになる)

    except requests.exceptions.RequestException as e:
        # エラー発生時は「ERROR」としてログを残す
        logger.error(f"一覧ページの取得に失敗 ({url}): {e}")
        return []

    res.encoding = res.apparent_encoding  # 取得情報をエンコード
    bs_data = BeautifulSoup(res.text,"html.parser")  # HTMLパーサーを使用し取得情報をテキストとして解析

    # 解析データから、特定のクラスのaタグを全取得
    shops_list = bs_data.find_all("a", class_="style_titleLink___TtTO")
    logger.debug(f"取得したaタグ:{len(shops_list)})件")

    urls = []

    for a_tag in shops_list:
        shop_url = a_tag.get("href")
        urls.append(shop_url)

    logger.debug(f"URL抽出件数:{len(urls)})件")

    return urls


# ◆◆◆ 0201_住所の正規表現分割 ◆◆◆
# ー引数：分割する住所
# ー戻り値：分割した住所のリスト

def normalize_address(text_address):
    dic = normalize(text_address)
    addr_list = [ dic['pref'], dic['city'] + dic['town'], dic['addr'] ]
    return addr_list


# ◆ 02_店舗情報取得
# ー引数：店舗ページのURL(リストから)
# ー戻り値：

def get_shop_info(url):

    time.sleep(3)

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()  # エラーチェック

    except requests.exceptions.RequestException as e:
        logger.error(f"店舗ページの取得に失敗 ({url}): {e}")
        
    return
    
    res.encoding = res.apparent_encoding
    bs_data = BeautifulSoup(res.text, "html.parser")

    # 1 店舗名取得
    shop_name_tag = bs_data.find("table", class_="basic-table").find("p", id="info-name")
    shop_name = shop_name_tag.text
    logger.debug(f"店舗名:{shop_name}")
    
    # 2 電話番号取得
    shop_tel_tag = bs_data.find("table", class_="basic-table").find("span", class_="number")
    shop_tel = shop_tel_tag.text
    logger.debug(f"電話番号:{shop_tel}")

    # 3 住所取得
    shop_addr_tag = bs_data.find("table", class_="basic-table").find("span", class_="region")
    shop_addr = shop_addr_tag.text
    logger.debug(f"住所:{shop_addr}")

    # ◆ 0201_住所の正規表現分割
    addr_list = normalize_address(shop_addr)

    # 4 建物名取得
    shop_building_tag = bs_data.find("table", class_="basic-table").find("span", class_="locality")
    if shop_building_tag:
        shop_building = shop_building_tag.text
    else:
        shop_building = ""
    logger.debug(f"建物名:{shop_building}")

    # 5 URL取得
    sv_site_ul = bs_data.find("ul", id="sv-site")

    # ul→li→aタグの順で確認
    if sv_site_ul:
        clickable_li = sv_site_ul.find("li", class_="clickable")
    
        if clickable_li and clickable_li.find("a"):
            shop_check_url = clickable_li.find("a").get("href")
        else:
            shop_check_url = "" # aタグがなければ空欄
    else:
        shop_check_url = "" # ulがなければ空欄
        logger.debug(f"URL:{shop_check_url}")

    # 正式なURLを取得、SLLを確認
    try:
        time.sleep(3)

        res_move = requests.get(shop_check_url, timeout=10)
        res_move.raise_for_status()  # エラーチェック

        shop_url = res_move.url  # 転送先のURL取得
        ssl_status = shop_url.startswith("https://")  # SSL確認

    except requests.exceptions.RequestException as e:
        # サイトが開けなかった場合
        logger.error(f"転送先サイトでエラーが発生しました: {e}")
        shop_url = ""
        ssl_status = False

    logger.debug(f"遷移先URL:{shop_url}")
    logger.debug(f"SSL:{ssl_status}")

    # 店舗情報をリストにまとめる
    shop_info_list = [shop_name, shop_tel] + addr_list + [shop_building, shop_url, ssl_status]

    all_shops_list.append(shop_info_list)


# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# 実行
# ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

# ◆ 01_店舗URLリスト作成
url_list = []

for page_num in range(1, 3):

    if page_num == 1:
        url = "https://r.gnavi.co.jp/area/jp/rs/"
    else:
        url = f"https://r.gnavi.co.jp/area/jp/rs/?p={page_num}"
        
    logger.info(f"店舗URL取得:開始({page_num}回目)")
    url_list.extend(get_shop_urls(url))
    logger.info(f"店舗URL取得:終了({page_num}回目)")

del url_list[50:]
logger.info(f"店舗URLリストを作成 ({len(url_list)}件)")


# ◆ 02_店舗情報取得
all_shops_list = []  # 最終的に全店舗情報を格納するリスト

count = 1  # ループ件数確認用

for info_url in url_list:

    logger.info(f"店舗情報抽出:開始({count}回目)")
    # ◆ 02_店舗情報取得
    get_shop_info(info_url)
    logger.info(f"店舗情報抽出:終了({count}回目)")
    count = count + 1


# ◆ 03_店舗情報リストからcsv作成

csv_file_name = "shop_data.csv"

try:
    lists_convert_csv(all_shops_list, csv_file_name)
    logger.info("CSVへの書き出しが完了しました。")

except OSError as e:
    logger.error(f"CSVが作成できませんでした。処理を終了します。 (エラー内容: {e})")