# 【演習4】

scores = [88, 92, 75, 88, 95, 68, 88, 70, 65, 96, 72, 85]

# scoresの要素数（長さ）を表示
print(len(scores))

# 左から2番目から右から2番目までを取り出したリストを表示
print(scores[1:-1])

# 一番左から一つ飛ばしで格納したリストを表示
print(scores[::2])

# 逆順に並べ替えたリストを表示
print(scores[::-1])

# 88がいくつ含まれているかを表示
print(scores.count(88))

# 点数が低い順（昇順）に並び替えたリストを表示
# 新しい昇順リストを返す
print(sorted(scores))
