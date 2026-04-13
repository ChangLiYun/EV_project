import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tab01 import render_market_overview
from tab02 import oil_vs_EVsales
from tab03 import Policy_timeline
from tab04 import trendline
from tab05 import test

# # 全球歷史銷售量

st.set_page_config(page_title="全球EV市場分析", layout="wide")

@st.cache_data
def load_data():
    ev = pd.read_excel(
        r"D:\Users\User\Desktop\專題\EV_project\EVDataExplorer2025.xlsx",
        sheet_name="GEVO_EV_2025"
    )
    oil = pd.read_excel(r"D:\Users\User\Desktop\專題\EV_project\2010_2026國際原油價格.xlsx")
    oil["日期"] = pd.to_datetime(oil["日期"])
    oil["year"] = oil["日期"].dt.year
    oil_yearly = oil[oil["year"] <= 2024].groupby("year")["北海布蘭特"].mean().round(2).reset_index()
    oil_yearly.columns = ["year", "brent"]

    policy = pd.read_excel(r"D:\Users\User\Desktop\專題\EV_project\EV關鍵政策時間軸.xlsx")
    return ev, oil_yearly, policy

ev, oil, policy = load_data()

@st.cache_data
def get_world_sales(_ev):
    return _ev[
        (_ev["parameter"] == "EV sales") &
        (_ev["category"] == "Historical") &
        (_ev["region_country"] == "World") &
        (_ev["mode"] == "Cars") &
        (_ev["powertrain"].isin(["BEV", "PHEV"]))
    ].groupby("year")["value"].sum().reset_index()

sales = get_world_sales(ev)

# ── 頁首 ──────────────────────────────────────
st.title("能源價格與地緣政治對電動車市場發展之影響分析")
st.caption("資料來源：IEA Global EV Data Explorer 2025 ｜ 台灣能源署國際原油價格")
st.success(f"資料載入成功！EV資料共 {len(ev):,} 筆，油價資料共 {len(oil)} 年")

# ── 分頁 ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "市場總覽",
    "油價與EV關係",
    "政策時間軸",
    "趨勢預測",
    "測試"
])

# ── Tab1：市場總覽 ─────────────────────────────
with tab1:
    render_market_overview(sales)

# ── Tab2：油價與EV關係 ─────────────────────────
with tab2:
    oil_vs_EVsales(sales, oil)

# ── Tab3：政策時間軸 ───────────────────────────
with tab3:
    Policy_timeline(policy)
# ── Tab4：趨勢預測 & 迴歸分析 ─────────────────
with tab4:
   trendline(ev, oil)
    
with tab5:
    test()


# @st.cache_data 是 Streamlit 的快取機制，讓每次重新整理頁面不用重新讀檔，速度更快。
# **第一步：建立專案結構**

# 在你的桌面新建一個資料夾 `EV_streamlit`，裡面建這幾個檔案：
# ```
# EV_streamlit/
#   ├── app.py          ← 主程式
#   ├── data/
#   │   ├── EVDataExplorer2025.xlsx
#   │   ├── 油價.csv
#   │   └── EV關鍵政策時間軸.xlsx
#   └── requirements.txt