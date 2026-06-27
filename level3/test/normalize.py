# normalize.py

# ◆◆◆ 0201_住所の正規表現分割 ◆◆◆
# ー引数：分割する住所
# ー戻り値：分割した住所のリスト

def normalize_address(text_address):
    # 型チェックと空文字チェック
    if not isinstance(text_address, str) or not text_address.strip():
        return ["", "", ""] 
        
    from normalize_japanese_addresses import normalize
    
    try:
        dic = normalize(text_address)
        # 必要なキーが揃っているか確認しつつリスト化
        addr_list = [ dic['pref'], dic['city'] + dic['town'], dic['addr'] ]
        return addr_list
        
    except Exception:
        # 解析不能なエラーが発生した場合のフォールバック
        return ["", "", text_address]
    
