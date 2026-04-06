import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'  # 微軟正黑體
matplotlib.rcParams['axes.unicode_minus'] = False #讓負號正常顯示

# ── 1. 油價資料 ──────────────────────────────
oil = pd.read_excel(r"D:\Users\User\Desktop\專題\EV_project\2010_2026國際原油價格.xlsx")
oil['日期'] = pd.to_datetime(oil['日期'])
oil['year'] = oil['日期'].dt.year
#每年的平均油價
oil_year = oil[oil['year'] <= 2024].groupby('year')['北海布蘭特'].mean().reset_index()
oil_year.rename(columns={'北海布蘭特': 'oil_price'}, inplace=True)

# ── 2. EV 銷售資料 ───────────────────────────
ev = pd.read_excel(
    r"D:\Users\User\Desktop\專題\EV_project\EVDataExplorer2025.xlsx",
    sheet_name="GEVO_EV_2025"        # ← 要指定工作表
)
# 篩選
ev_filtered = ev[
    (ev["parameter"] == "EV sales") &
    (ev["region_country"] == "World") &  # ← 正確欄位名稱
    (ev["mode"] == "Cars") &
    (ev["category"] == "Historical") &
    (ev["powertrain"].isin(["BEV", "PHEV"]))
]
#把油價表和 EV 銷售表用「year」欄位合併
ev_year = ev_filtered.groupby("year")["value"].sum().reset_index()
ev_year.rename(columns={"value": "ev_sales"}, inplace=True)

# ── 3. 合併兩份資料 ──────────────────────────
df = pd.merge(oil_year, ev_year, on="year")
print("合併後資料：")
print(df.to_string(index=False))

# ── 4. 迴歸分析 ──────────────────────────────
X = df[["oil_price"]]           # 自變數：油價
y = df["ev_sales"]              # 依變數：EV 銷售量

model = LinearRegression()
model.fit(X, y)

r2 = model.score(X, y) # 計算 R²
coef = model.coef_[0] # 斜率（每漲 1 美元，EV 變化多少輛）
intercept = model.intercept_ # 截距（油價為 0 時的理論 EV 銷售量）

print(f"\n迴歸結果：")
print(f"  R²（解釋力）: {r2:.4f}")
print(f"  係數（斜率）: {coef:,.0f}")
print(f"  截距: {intercept:,.0f}")
print(f"\n解讀：油價每上漲1美元，EV銷售量變化 {coef:,.0f} 輛")

# ── 6. 以「年份」為自變數做迴歸（時間趨勢）──
X_year = df[["year"]]
model_year = LinearRegression()
model_year.fit(X_year, y)
r2_year = model_year.score(X_year, y)
print(f"\n時間趨勢迴歸 R²: {r2_year:.4f}")
print(f"解讀：EV銷售量每年平均增加 {model_year.coef_[0]/1e6:.2f} 百萬輛")

# ── 5. 視覺化 ────────────────────────────────
fig, ax1 = plt.subplots(figsize=(12, 6))

# 散佈圖 + 迴歸線
ax1.scatter(df["oil_price"], df["ev_sales"] / 1e6,
            color="#1D9E75", s=80, zorder=5, label="實際數據")

x_range = np.linspace(df["oil_price"].min(), df["oil_price"].max(), 100)
y_pred = model.predict(x_range.reshape(-1, 1)) / 1e6
ax1.plot(x_range, y_pred, color="#E24B4A", linewidth=2,
         linestyle="--", label=f"迴歸線 (R²={r2:.3f})")

# 標注年份
for _, row in df.iterrows():
    ax1.annotate(str(int(row["year"])),
                 (row["oil_price"], row["ev_sales"] / 1e6),
                 textcoords="offset points", xytext=(5, 5), fontsize=8)

ax1.set_xlabel("布蘭特原油年均價（USD/桶）", fontsize=11)
ax1.set_ylabel("EV 銷售量（百萬輛）", fontsize=11)
ax1.set_title("油價 vs 全球EV銷售量 線性迴歸分析（2010–2024）", fontsize=13)
ax1.legend()
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("oil_ev_regression.png", dpi=150)
plt.show()
print("\n圖表已儲存為 oil_ev_regression.png")

'''
可以觀察幾個現象：
2012、2013 年：油價很高（110美元），但 EV 銷售接近 0
2015、2016 年：油價崩跌到 44美元，EV 銷售反而繼續成長
2022 年：油價回升到 100美元，EV 是 1,020萬輛
2023、2024 年：油價下降到 80美元，EV 卻繼續創新高
這些點散落在圖的各個角落，迴歸線幾乎是水平的（斜率接近 0），代表不管油價高低，EV 銷售量都在成長，但成長的原因不是油價。

研究問題：油價是否影響EV銷售？

量化結果：
  油價迴歸  R² = 0.002  →  油價解釋力不到0.2%
  時間迴歸  R² = 0.704  →  結構性成長解釋70%

結論：
  EV市場成長主要由政策補貼、技術成熟、
  消費習慣改變等長期結構因素驅動，
  而非短期油價波動。
  
  2022年俄烏戰爭（油價飆升）同年EV爆發，
  進一步說明能源安全意識才是關鍵觸媒，
  而非價格訊號本身。
'''