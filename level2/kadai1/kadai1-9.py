# 【演習9】

# 1. 3人分のデータをdictで作成
people = {
    "Aさん": {"身長": 160, "体重": 60},
    "Bさん": {"身長": 120, "体重": 40},
    "Cさん": {"身長": 180, "体重": 100},
}

# 2. 条件判定（身長が120以上 かつ 体重が100未満）
for name, data in people.items():
    result = (data["身長"] >= 120) and (data["体重"] < 100)
    print(name, result)
