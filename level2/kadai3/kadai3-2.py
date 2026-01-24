# 演習4-2

# 合計金額(int)とランク(str)を受け取り、支払い金額(int)を返す関数
# defで関数宣言、「calculate_payment」というリストを作成
# amountは合計金額で整数、rankはランクで文字列、これらが引数
def calculate_payment(amount: int, rank: str) -> int:

# ランクに応じた割引率の設定
    if rank == "gold":
        discount_rate = 0.8 # 20%割引
    elif rank == "silver":
        discount_rate = 0.9 # 10%割引
    else:
        discount_rate = 1.0 # 割引なし

# 合計金額×割引率=割引後の金額計算
    discounted_price = amount * discount_rate
 
# 割引後の金額計算に消費税10%を加算し、整数に変換して返す(最終金額)
# 割引後の金額×1.1(消費税)を変数tax_includedに当てはめる
# 戻り値が変数tax_included
    tax_included = int(discounted_price * 1.1)
    return tax_included

# defからreturnまででひとまとまり。
# 関数外で変数にcalculate_paymentを当てはめると、
# 最終金額であるtax_includedが反映される。


# ======= 実行と出力 =====================

# パターン1：ランク gold
amnt_res1 = 12800
rnk_res1 = "gold"
res1 = calculate_payment(amnt_res1, rnk_res1)
print(f"合計金額: {amnt_res1}, ランク: {rnk_res1} -> 支払い金額: {res1}円")

# パターン2：ランク silver
res2 = calculate_payment(27000, "silver")
print(f"合計金額: 27000, ランク: silver -> 支払い金額: {res2}円")

# パターン3：ランク bronze
res3 = calculate_payment(1680, "bronze")
print(f"合計金額: 1680, ランク: bronze -> 支払い金額: {res3}円")