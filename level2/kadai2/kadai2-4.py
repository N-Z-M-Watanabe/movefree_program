# 元データ
students_scores = [
    {"name": "鈴木", "score": 92},
    {"name": "田中", "score": 68},
    {"name": "佐藤", "score": 88},
    {"name": "山田", "score": 75},
    {"name": "高橋", "score": 95},
]

# 空のリストを作成
pass_list = []   # 合格者リスト
retry_list = []  # 追試者リスト

# 各リストに名前の追加
for student in students_scores:
    if student["score"] >= 80:
        pass_list.append(student["name"])
    else:
        retry_list.append(student["name"])

# リスト表示
print("合格者リスト:", pass_list)
print("追試者リスト:", retry_list)