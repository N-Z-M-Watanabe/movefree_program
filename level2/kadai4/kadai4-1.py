# # 演習1

# 1 標準ライブラリから random モジュールを読み込む
import random

# 2 サイコロの結果を保存するための空のリストを用意
dice_results = []

# 3 サイコロを10回振る処理
for i in range(10):
    # 1〜6のランダムな整数を作成（サイコロの目）
    dice = random.randint(1, 6)
    
    # 作成した整数をリストに追加
    dice_results.append(dice)
    
    # その都度、出た目を表示
    print(f"{i+1}回目のサイコロの目: {dice}")

# 4 合計値を計算
total = sum(dice_results)

# 5 平均値を計算
average = total / len(dice_results)

# 6 合計値と平均値を表示
print("合計値:", total)
print("平均値:", average)