import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['font.family'] = 'Microsoft JhengHei'
matplotlib.rcParams['axes.unicode_minus'] = False

df = pd.read_excel(r'D:\Users\User\Desktop\專題\EV_project\EVDataExplorer2025.xlsx', sheet_name='GEVO_EV_2025')

# 整理數據（和上面一樣）
charger = df[
    (df['parameter']=='EV charging points') &
    (df['region_country']=='China') &
    (df['category']=='Historical')
].groupby(['year','powertrain'])['value'].sum().unstack(fill_value=0).reset_index()
charger.columns = ['year','fast','slow']
charger['total'] = charger['fast'] + charger['slow']

stock = df[
    (df['parameter']=='EV stock') & (df['region_country']=='China') &
    (df['mode']=='Cars') & (df['category']=='Historical') &
    (df['powertrain'].isin(['BEV','PHEV']))
].groupby('year')['value'].sum().reset_index()
stock.columns = ['year','ev_stock']

sales = df[
    (df['parameter']=='EV sales') & (df['region_country']=='China') &
    (df['mode']=='Cars') & (df['category']=='Historical') &
    (df['powertrain'].isin(['BEV','PHEV']))
].groupby('year')['value'].sum().reset_index()
sales.columns = ['year','ev_sales']

share = df[
    (df['parameter']=='EV sales share') & (df['region_country']=='China') &
    (df['mode']=='Cars') & (df['powertrain']=='EV') &
    (df['category']=='Historical')
][['year','value']].rename(columns={'value':'penetration'})

base = charger.merge(stock,on='year').merge(sales,on='year').merge(share,on='year')
base = base[base['year']>=2018].sort_values('year').reset_index(drop=True)

# 計算指標
base['charger_per_ev']     = base['total'] / base['ev_stock']
base['new_charger']        = base['total'].diff().fillna(base['total'])
base['incremental_ratio']  = base['new_charger'] / base['ev_sales']
base['fast_ratio']         = base['fast'] / base['total'] * 100

# ── 圖一：三線圖（增量樁車比 + 滲透率 + 快充比例）
fig, ax1 = plt.subplots(figsize=(12,6))

ax2 = ax1.twinx()

ax1.bar(base['year'], base['incremental_ratio'],
        color='#B5D4F4', alpha=0.7, label='增量樁車比（左軸）')
ax1.set_ylabel('增量樁車比（新增樁數/新增EV數）', fontsize=11)
ax1.set_ylim(0, 0.35)

ax2.plot(base['year'], base['penetration'],
         color='#1D9E75', linewidth=2.5, marker='o', label='EV滲透率（右軸）')
ax2.plot(base['year'], base['fast_ratio'],
         color='#EF9F27', linewidth=2, marker='s', linestyle='--', label='快充比例%（右軸）')
ax2.set_ylabel('比率（%）', fontsize=11)

# 標注關鍵點
ax1.annotate('增量比開始\n持續下降', xy=(2021, 0.105), xytext=(2019.5, 0.18),
             arrowprops=dict(arrowstyle='->', color='red'), color='red', fontsize=10)
ax2.annotate('滲透率仍飆升\n至48%', xy=(2024, 48), xytext=(2022.5, 42),
             arrowprops=dict(arrowstyle='->'), fontsize=10)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left')
ax1.set_title('中國充電基礎設施臨界點分析（2018-2024）', fontsize=13)
ax1.set_xlabel('年份')
ax1.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('china_charger_threshold.png', dpi=150)
plt.show()
print("成功")

# ----輸出----
print("\n=== 分析結果 ===")
print(f"2021年增量車樁比：{base[base['year']==2021]['incremental_ratio'].values[0]:.3f}")
print(f"2024年增量車樁比：{base[base['year']==2024]['incremental_ratio'].values[0]:.3f},"
      f"(1樁配幾車): {1/base[base['year']==2024]['incremental_ratio'].values[0]:.1f}")


print(f"2024年滲透率：{base[base['year']==2024]['penetration'].values[0]:.1f}%")
print(f"2024年快充比例：{base[base['year']==2024]['fast_ratio'].values[0]:.1f}%")

# 2030預測缺口
charger_2030 = 12_600_000   # IEA預測
stock_2030   = 138_000_000  # IEA預測
current_ratio = charger_2030 / stock_2030
needed_1to5  = stock_2030 / 5  # 1:5樁車比需要多少充電樁
gap = needed_1to5 - charger_2030
print(f"\n2030預測車樁比（IEA STEPS）：{current_ratio:.3f}")
print(f"若維持1:5標準需要充電樁：{needed_1to5/1e6:.1f}M")
print(f"IEA預測缺口：{gap/1e6:.1f}M 座充電樁")