import requests

# 1. 郵便番号を入力する
zipcode = input("7桁の郵便番号を入力 ※ハイフンなし: ")

# 2. エンドポイントURLとパラメータの設定
# zipcloud APIのURLです
url = "https://zipcloud.ibsnet.co.jp/api/search"
# URLの末尾に「?zipcode=番号」を付けるため、辞書形式でパラメータを用意
params = {"zipcode": zipcode}

try:
    # 3. APIにリクエスト（GET）を送る
    response = requests.get(url, params=params)
    
    # 4. レスポンスが成功（200 OK）か確認 
    if response.status_code == 200:
        # JSONデータをPythonの辞書形式に変換
        data = response.json()
        
        # 5. データの取得結果を確認
        if data["results"] is not None:
            # 取得したデータから都道府県、市区町村、町域名を連結して表示
            result = data["results"][0]
            address = f"{result['address1']}{result['address2']}{result['address3']}"
            print(f"住所: {address}")
        else:
            print("該当する住所が見つかりませんでした。")
    else:
        print(f"エラーが発生しました。ステータスコード: {response.status_code}")

except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")