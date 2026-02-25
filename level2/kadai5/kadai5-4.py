# 演習4
import numpy as np

scores = np.array([
    [72, 85],
    [90, 92],
    [68, 77],
    [88, 95],
    [76, 80]
])

# 1. 数学の点数（1列目）だけを抽出する
# 全行「:」の、0番目のインデックスを指定
math_scores = scores[:, 0]
print(f"数学の点数: {math_scores}")

# 2. 3人目の英語の点数（3行2列目）だけを抽出
student3_english = scores[2, 1]
print(f"3人目の英語の点数: {student3_english}")

# 3. 数学の平均点を計算する
math_mean = np.mean(scores[:, 0])
print(f"数学の平均点: {math_mean}")

# 4. 英語の最高点を計算する
english_max = np.max(scores[:, 1])
print(f"英語の最高点: {english_max}")

# 5. 数学の点数が80点以上だった生徒の、数学と英語の両方の点数を抽出する
# 数学(1列目)が80以上の行をブールインデックス参照で抽出します
high_math_students = scores[scores[:, 0] >= 80]
print("数学が80点以上の生徒の全得点:")
print(high_math_students)