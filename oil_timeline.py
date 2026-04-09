import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 讀取資料 (建議加上 error handling 以防路徑出錯)
try:
    df = pd.read_excel(r"C:\Users\FM_pc\Desktop\專\EV_project\2010_2026國際原油價格.xlsx")
    df['日期'] = pd.to_datetime(df['日期'])
except Exception as e:
    st.error(f"讀取檔案失敗: {e}")
    st.stop()

# 定義大事紀 (增加顏色區分，更有財經感)
events = [
    {"date": "2020-04-20", "desc": "WTI期貨負油價", "color": "red"},
    {"date": "2022-03-08", "desc": "俄烏戰爭爆發", "color": "orange"},
    {"date": "2023-10-07", "desc": "以巴衝突再起", "color": "green"}
]

# Slider 控制
start_date, end_date = st.sidebar.slider(
    "選擇日期範圍",
    min_value= df['日期'].min().date(),
    max_value= df['日期'].max().date(),
    value=(df['日期'].min().date(), df['日期'].max().date())
)

# 過濾資料
mask = (df['日期'].dt.date >= start_date) & (df['日期'].dt.date <= end_date)
filtered_df = df.loc[mask]

# 繪圖
fig = px.line(filtered_df, x="日期", y="西德州", 
              title="WTI 原油價格與國際大事紀",
              labels={"西德州": "價格 (USD/bbl)"})

# 動態添加大事紀
for i, ev in enumerate(events):
    ev_date = pd.to_datetime(ev["date"])
    
    # 關鍵：只在選取的日期範圍內畫線
    if start_date <= ev_date.date() <= end_date:
        # 畫垂直虛線
        fig.add_vline(x=ev_date, line_dash="dash", line_color=ev["color"], opacity=0.7)
        
        # 畫文字標籤 (使用 yref="paper" 讓文字固定在圖表頂端 0.95 的位置)
        fig.add_annotation(
            x=ev_date, 
            y=0.95 - (i * 0.05), # 稍微錯開高度避免重疊
            yref="paper", 
            text=ev["desc"],
            showarrow=True,
            arrowhead=2,
            arrowcolor=ev["color"],
            ax=40, # 文字向右偏移
            ay=0,
            font=dict(color=ev["color"], size=12),
            bgcolor="white",
            opacity=0.9
        )

# 優化佈局 (讓滑鼠移過去時顯示完整日期)
fig.update_xaxes(showspikes=True, spikecolor="gray", spikethickness=1)
fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)