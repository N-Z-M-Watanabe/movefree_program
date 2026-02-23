# 演習5

import pandas as pd
import matplotlib.pyplot as plt

# 1. データの作成とDataFrameへの変換
data = {
    '月': ['1月', '2月', '3月', '4月', '5月', '6月'],
    '売上': [500000, 480000, None, 600000, 720000, 680000],
    '客数': [1200, 1150, 1300, 1500, 1800, 1650]
}
df = pd.DataFrame(data)

# 2. 3月の欠損値を平均値で埋める
mean_sales = df['売上'].mean()
df['売上'] = df['売上'].fillna(mean_sales)

# 3. 「顧客単価」の追加
df['顧客単価'] = df['売上'] / df['客数']

# 4. グラフの描画
# フォントを AppleGothic に設定
plt.rcParams['font.family'] = 'Hiragino sans'

fig, ax1 = plt.subplots(figsize=(10, 6))

# 売上の棒グラフ（第1軸：左）
ax1.bar(df['月'], df['売上'], color='skyblue', label='売上', alpha=0.7)
ax1.set_xlabel('月')
ax1.set_ylabel('売上 (円)')
ax1.set_title('カフェの売上と客数の推移（半年間）')

# 客数の折れ線グラフ（第2軸：右）
ax2 = ax1.twinx()
ax2.plot(df['月'], df['客数'], color='red', marker='o', label='客数', linewidth=2)
ax2.set_ylabel('客数 (人)')

# 凡例の設定（2つの軸のラベルを1つにまとめる）
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc='upper left')

plt.tight_layout()
plt.show()
