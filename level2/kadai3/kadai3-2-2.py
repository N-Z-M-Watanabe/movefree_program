# 演習4-2

# ターミナルに手動入力の場合

# ======= 関数定義 ==============
def calculate_payment(amount: int, rank: str) -> int:
    if rank == "gold":
        discount_rate = 0.8
    elif rank == "silver":
        discount_rate = 0.9
    else:
        discount_rate = 1.0

    discounted_price = amount * discount_rate
    tax_included = int(discounted_price * 1.1)
    return tax_included


# ======= 手入力による実行と出力 ==============

# 1. 合計金額の入力（数値に変換）
input_amount = int(input("合計金額（税抜き）を入力してください: "))

# 2. 会員ランクの入力（文字列として受け取り）
input_rank = input("会員ランク（gold, silver, bronze）を入力してください: ")

# 3. 入力された値を引数として関数を実行
result = calculate_payment(input_amount, input_rank)

# 4. 結果の表示
print(f"--- 計算結果 ---")
print(f"合計金額: {input_amount}円, ランク: {input_rank} -> 支払い金額: {result}円")