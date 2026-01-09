# 【演習6】

def check_calculation(description, func):
    try:
        result = func()
        print(description, "=>", result)
    except Exception as e:
        print(description, "=> エラー")

# 1. “Hello”と”World”の足し算
check_calculation(
    "“Hello” + “World”",
    lambda: "Hello" + "World"
)

# 2. “Hello”と”World”の引き算
check_calculation(
    "“Hello” - “World”",
    lambda: "Hello" - "World"
)

# 3. “Hello”に3を足した時の結果
check_calculation(
    "“Hello” + 3",
    lambda: "Hello" + 3
)

# 4. “Hello”に3をかけた時の結果
check_calculation(
    "“Hello” * 3",
    lambda: "Hello" * 3
)

# 5. 数値型を0で割った時の結果
check_calculation(
    "10 / 0",
    lambda: 10 / 0
)

# 6. 1 == True、0 == False の結果
check_calculation(
    "1 == True, 0 == False",
    lambda: (1 == True, 0 == False)
)
