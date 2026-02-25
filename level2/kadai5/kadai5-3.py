# 演習3

import numpy as np
from numpy.typing import NDArray
# 「型ヒント用クラス」NDArray を読み込む

# ①
def main() -> None:
    # 0から9までの連続した整数を持つ1次元のNumPy配列を作成（配列1）
    array1: NDArray[np.int64] = np.arange(10)

# ②
    # 配列1のすべての要素を5倍した新しい配列を作成（配列2）
    array2: NDArray[np.int64] = array1 * 5

# ③
    # 配列2の中から、30以上の要素だけを抽出した配列を作成（配列3）
    array3: NDArray[np.int64] = array2[array2 >= 30]

# ④
    # 配列3の合計値を計算
    total: int = int(np.sum(array3))

    # 配列3の平均値を計算
    average: float = float(np.mean(array3))

    # 配列3の要素数を計算
    count: int = int(array3.size)

    # 結果を表示
    print("配列1:", array1)
    print("配列2:", array2)
    print("配列3:", array3)
    print("合計値:", total)
    print("平均値:", average)
    print("要素数:", count)


# プログラムの実行開始点(①の部分を指し示す)
if __name__ == "__main__":
    main()
