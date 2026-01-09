# 【演習7】

# 単価
apple_price = 150
orange_price = 50

# 個数
apple_count = 2
orange_count = 5

# 消費税率
tax_rate = 0.08

# 税抜合計金額
subtotal = apple_price * apple_count + orange_price * orange_count

# 税込合計金額
total = int(subtotal * (1 + tax_rate))

# 4人で割る
per_person = total // 4
remainder = total % 4

# 結果を表示
print("合計金額:", total, "円")
print("一人分の金額:", per_person, "円")
print("あまり:", remainder, "円")
