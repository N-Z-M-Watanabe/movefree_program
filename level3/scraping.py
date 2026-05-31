import requests
from bs4 import BeautifulSoup
import time
from normalize_japanese_addresses import normalize
import csv
import unicodedata
import logging
import os

# --- ログの設定 -----------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # すべてのレベルのログを記録対象にします

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

# --- ログの設定おわり -----------------------------


# ユーザーエージェント設定
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

timenum = 3

# 1.ぐるなび店舗一覧ページから店舗ページのURL取得 -------------------

# 【関数定義】店舗のURLリストを取得 -------------
def get_shop_urls(url):

    time.sleep(timenum)

    try:
        res = requests.get(url, headers=headers, timeout=10)  # URLからサイトのHTML情報を取得
        res.raise_for_status()  # エラーチェック(ステータス200以外はエラーになる)

    except requests.exceptions.RequestException as e:
        # エラー発生時は「ERROR」としてログを残す
        logger.error(f"一覧ページの取得に失敗しました ({url}): {e}")
        return []

    res.encoding = res.apparent_encoding  # 取得した情報を自動でエンコード
    bs_date = BeautifulSoup(res.text,"html.parser")  # HTMLパーサーを使用し取得した情報をテキストとして解析

    # 解析したデータの中で、特定のクラスのaタグを全て取得する
    shops_list = bs_date.find_all("a", class_="style_titleLink___TtTO")

    urls = []

    for a_tag in shops_list:
        shop_url = a_tag.get("href")
        urls.append(shop_url)

    return urls

# 【関数定義】おわり -------------

# 関数呼び出し
url1 = "https://r.gnavi.co.jp/area/jp/rs/"
logger.info("店舗URL取得:開始(1回目)")
list1 = get_shop_urls(url1)
logger.info("店舗URL取得:終了(1回目)")

url2 = "https://r.gnavi.co.jp/area/jp/rs/?p=2"
logger.info("店舗URL取得:開始(2回目)")
list2 = get_shop_urls(url2)
logger.info("店舗URL取得:終了(2回目)")

# 取得した店舗ページURLのリスト統合、URLの件数を50にする
url_list = list1 + list2
del url_list[50:]
logger.info(f"店舗URLリストを作成 ({len(url_list)}件)")


# 2.取得したURLのリストから店舗情報を取得 -------------------

all_shops_list = []  # 最終的に全店舗情報を格納するリスト

count = 1

for info_url in url_list:

    logger.info(f"URLリストから店舗情報抽出を開始({count}回目)")

    time.sleep(timenum)

    try:
        res = requests.get(info_url, headers=headers, timeout=10)
        res.raise_for_status()  # エラーチェック

    except requests.exceptions.RequestException as e:
        logger.error(f"店舗ページの取得に失敗 ({info_url}): {e}")
        continue
    
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
            time.sleep(timenum)

            res_move = requests.get(shop_check_url, timeout=10)
            res_move.raise_for_status()  # エラーチェック

            shop_url = res_move.url  # 転送先のURLを取得
            is_ssl = shop_url.startswith("https://")  # SSLの確認
            return shop_url, is_ssl

        except requests.exceptions.RequestException as e:
            # サイトが開けなかった場合
            logger.error(f"転送先サイトでエラーが発生しました: {e}")
            return None, False

    if shop_check_url != "":
        target_url = shop_check_url
        shop_url, ssl_status = check_site(target_url)

    else:
        shop_url = ""
        ssl_status = False

    # 店舗情報をリストにまとめる
    shop_info_list = [shop_name, shop_tel] + addr_list + [shop_building, shop_url, ssl_status]

    all_shops_list.append(shop_info_list)

    logger.info(f"書き出し用リストに追加: {shop_name}")

    count = count + 1


# 3.取得した店舗のリストをcsvに書き込み-------------------
file_path = os.path.join(current_dir, "shop_data.csv")  # カレントディレクトリ+CSVのパスを変数化

# shift-jis用の変換関数
def clean_text(text):
    if text is None:
        return ""

    return unicodedata.normalize("NFKC", str(text))

# 作成した全店舗リストを変換する
cleaned_all_shops_list = []
for shop in all_shops_list:
    cleaned_row = [clean_text(item) for item in shop]
    cleaned_all_shops_list.append(cleaned_row)

try:
    with open(file_path, "w", newline="", encoding="shift_jis", errors="replace") as f:
        writer = csv.writer(f)
        # ヘッダー（項目名）を書き込む
        writer.writerow(["店舗名", "電話番号", "都道府県", "市区町村", "番地", "建物名", "URL", "SSL"])
        writer.writerows(cleaned_all_shops_list)

    logger.info("CSVファイルへの書き出しが完了しました。")

except OSError as e:
    logger.error(f"CSVファイルが作成できませんでした。処理を終了します。 (エラー内容: {e})")
    raise