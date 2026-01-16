answer = 64

while True:
    number = int(input("1〜100の数字を入力してください: "))

    if number < answer:
        print("もっと大きいです")
    elif number > answer:
        print("もっと小さいです")
    else:
        print("正解です！")
        break