import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# @st.cache_data
# def load_data():
#     ev = pd.read_excel("C:\\Users\\FM_pc\\Desktop\\專\\EVDataExplorer2025.xlsx", sheet_name="GEVO_EV_2025" )
   
#     # 油價資料
#     oil = pd.read_excel("C:\\Users\\FM_pc\\Desktop\\專\\2010_2026國際原油價格.xlsx")
#     oil["日期"] = pd.to_datetime(oil["日期"])
#     oil["year"] = oil["日期"].dt.year
#     oil_yearly = oil[oil["year"]<=2024].groupby("year")["北海布蘭特"].mean().round(2).reset_index()
#     oil_yearly.coums = ["year","brent"]

#     # 政策時間軸
#     policy = pd.read_excel("C:\\Users\\FM_pc\\Desktop\\專\\EV關鍵政策時間軸.xlsx")
#     return ev, oil_yearly, policy
# ev, oil, policy = load_data()


# # 全球歷史銷售量



st.set_page_config(page_title="全球EV市場分析", layout="wide")

@st.cache_data
def load_data():
    ev = pd.read_excel(
        r"C:\Users\FM_pc\Desktop\專\EVDataExplorer2025.xlsx",
        sheet_name="GEVO_EV_2025"
    )
    oil = pd.read_excel(r"C:\Users\FM_pc\Desktop\專\2010_2026國際原油價格.xlsx")
    oil["日期"] = pd.to_datetime(oil["日期"])
    oil["year"] = oil["日期"].dt.year
    oil_yearly = oil[oil["year"] <= 2024].groupby("year")["北海布蘭特"].mean().round(2).reset_index()
    oil_yearly.columns = ["year", "brent"]

    policy = pd.read_excel(r"C:\Users\FM_pc\Desktop\專\EV關鍵政策時間軸.xlsx")
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
    st.subheader("全球EV銷售趨勢（2010–2024）")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("2024全球銷售量", "1,750萬輛", "+28%")
    col2.metric("全球滲透率", "22%", "+4pp")
    col3.metric("石油替代量", "132萬桶/天", "+30%")
    col4.metric("2024 BEV佔比", "63%", "-6pp")

    sales["YoY"] = sales["value"].pct_change() * 100
    fig = px.bar(
        sales, x="year", y="value",
        labels={"year": "年份", "value": "銷售量（輛）"},
        color_discrete_sequence=["#00B4D8"]
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**分析結論**：2021年是關鍵爆發點（YoY +122%），"
                "2022-2024年成長率雖趨緩，但絕對銷量仍持續創高。"
                "市場正從爆發期進入穩定成長期。")

# ── Tab2：油價與EV關係 ─────────────────────────
with tab2:
    st.subheader("布蘭特原油價格 vs 全球EV銷售量")

    merged = sales.merge(oil, on="year")
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=merged["year"], y=merged["brent"],
        name="布蘭特油價（USD/桶）",
        marker_color="#EF9F27"
    ))
    fig2.add_trace(go.Scatter(
        x=merged["year"], y=merged["value"],
        name="EV銷售量（輛）",
        yaxis="y2", line=dict(color="#1D9E75", width=3)
    ))
    fig2.update_layout(
        yaxis=dict(title="油價（USD/桶）"),
        yaxis2=dict(title="EV銷售量", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h")
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("**核心發現**：")
    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("2015–2016 油價崩跌，EV照樣成長"):
            st.write("布蘭特從111美元跌至44美元（-60%），"
                     "但EV銷售從52萬成長至78萬輛（+50%）。"
                     "證明政策補貼是EV成長的主要驅動力，而非油價壓力。")
            st.metric("油價跌幅", "-60%")
            st.metric("EV銷售成長", "+50%")
    with col_b:
        with st.expander("2022 俄烏戰爭，EV爆發性成長"):
            st.write("俄烏戰爭導致油價突破100美元，全球能源安全意識覺醒，"
                     "各國加速EV政策佈局。當年EV銷售達1,020萬輛，YoY +55%。")
            st.metric("布蘭特油價", "101美元/桶")
            st.metric("EV銷售成長", "+55%")

# ── Tab3：政策時間軸 ───────────────────────────
with tab3:
    st.subheader("全球EV關鍵政策時間軸")
    st.subheader("石油進口依賴度 vs EV 滲透率")

    dependency_data = pd.DataFrame({
        "國家": ["中國", "歐盟", "美國"],
        "石油進口依賴度": ["74%", "~97%", "淨出口國"],
        "2024 EV滲透率": ["48%", "22%", "10%"],
        "推動EV核心動機": [
            "能源安全：降低馬六甲海峽封鎖風險",
            "能源主權：脫離對威權國家能源依賴",
            "產業競爭力：非出自能源安全急迫性"
        ]
    })
    st.dataframe(dependency_data, use_container_width=True)

    st.markdown("**核心洞察**：石油進口依賴度愈高，EV滲透率愈高。"
            "中國和歐盟的電動化本質上是能源安全戰略，而非純粹的環保政策。")

    region_filter = st.multiselect(
        "篩選地區",
        options=policy["國家或地區"].unique().tolist(),
        default=policy["國家或地區"].unique().tolist()
    )
    filtered = policy[policy["國家或地區"].isin(region_filter)].sort_values("年份")

    for _, row in filtered.iterrows():
        with st.expander(f"{int(row['年份'])}｜{row['國家或地區']}｜{row['政策類型']}"):
            st.write(row["政策內容"])
            st.caption(f"影響層級：{row['影響層級']}")

# ── Tab4：趨勢預測 ─────────────────────────────
with tab4:
    st.subheader("EV銷售趨勢預測（2025–2030）")
    st.info("預測模型說明：使用 S 曲線（Logistic）和多項式回歸兩種方式，"
            "與 IEA STEPS 預測進行比較。")

    pred_data = pd.DataFrame({
        "year": list(range(2010, 2031)),
        "歷史實際值": [7450,49000,118000,201000,330000,520000,780000,
                      1200000,2050000,2080000,2970000,6600000,10200000,
                      13700000,17500000] + [None]*6,
        "IEA STEPS": [None]*10 + [2970000,6600000,10200000,13700000,
                                   17500000,None,None,None,None,None,40000000],
        "S曲線預測": [None]*15 + [34340000,47480000,62010000,76300000,
                                   88840000,98780000],
    })

    fig4 = px.line(
        pred_data, x="year",
        y=["歷史實際值", "IEA STEPS", "S曲線預測"],
        labels={"year": "年份", "value": "銷售量（輛）"},
        color_discrete_map={
            "歷史實際值": "#1D9E75",
            "IEA STEPS": "#185FA5",
            "S曲線預測": "#EF9F27"
        }
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**模型比較**：IEA STEPS 基於「已宣告政策延伸」，"
                "預測2030年達4,000萬輛（滲透率約40%）。"
                "S曲線模型基於歷史趨勢外推，預測9,878萬輛，"
                "差距反映了政策假設與市場動能之間的分歧。")
    
with tab5:
    # 在 Tab2（油價與EV關係）或獨立 Tab 裡加這段

    st.subheader("能源進口依賴度 vs EV 滲透率（2024）")

    geo_data = pd.DataFrame({
        "國家": ["挪威","美國","中國","英國","瑞典","丹麥","芬蘭",
                "法國","德國","荷蘭","比利時","奧地利","葡萄牙",
                "以色列","日本","韓國","義大利","西班牙","印度"],
        "能源進口依賴度": [-741,-8,18,36,-64,-10,-35,49,61,99,
                        87,64,73,87,90,85,84,73,44],
        "EV滲透率": [92,10,48,28,58,56,50,24,19,48,
                    43,24,33,21,3,9,4,5,2],
        "地區": ["北歐","北美","亞洲","歐洲","北歐","北歐","北歐",
                "歐洲","歐洲","歐洲","歐洲","歐洲","歐洲",
                "中東","亞洲","亞洲","歐洲","歐洲","亞洲"],
        "主要動機": [
            "氣候生存威脅","產業競爭力","能源安全+工業戰略",
            "工業競爭+氣候","氣候生存威脅","氣候生存威脅","氣候生存威脅",
            "氣候+工業競爭","能源主權+工業競爭","氣候+工業競爭",
            "氣候+工業競爭","氣候+工業競爭","氣候+工業競爭",
            "能源孤島生存","能源安全","能源安全",
            "氣候+工業競爭","氣候+工業競爭","能源安全"
        ]
    })

    color_map = {
        "北歐": "#1D9E75",
        "歐洲": "#185FA5",
        "亞洲": "#EF9F27",
        "北美": "#E24B4A",
        "中東": "#7F77DD"
    }

    fig_scatter = px.scatter(
        geo_data,
        x="能源進口依賴度",
        y="EV滲透率",
        color="地區",
        color_discrete_map=color_map,
        text="國家",
        hover_data=["主要動機"],
        labels={
            "能源進口依賴度": "能源淨進口依賴度（%，負值=能源出口國）",
            "EV滲透率": "EV 銷售滲透率 2024（%）"
        },
        size_max=15
    )
    fig_scatter.update_traces(textposition="top center", marker=dict(size=10))
    fig_scatter.add_vline(x=0, line_dash="dash", line_color="gray",
                        annotation_text="← 能源出口國 | 能源進口國 →")
    fig_scatter.add_hline(y=22, line_dash="dot", line_color="gray",
                        annotation_text="全球平均 22%")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.info("""
    **📊 數據來源**：能源進口依賴度 — World Bank / TheGlobalEconomy.com（2022-2023）
    EV 滲透率 — IEA Global EV Data Explorer 2025

    **🔍 關鍵洞察**：
    - **挪威** 是最特殊的反例——它是能源出口大國（-741%），但 EV 滲透率全球最高（92%）
    → 說明挪威的 EV 普及純粹由**氣候意識 + 長達 20 年的稅收豁免政策**驅動
    - **北歐四國**（挪威、瑞典、丹麥、芬蘭）都在左上角：能源相對自給，但滲透率最高
    → 氣候生存威脅是北歐的核心動機
    - **日本、韓國、以色列**能源進口依賴度高（85-90%），但 EV 滲透率低（3-21%）
    → 光有能源依賴還不夠，缺乏強力補貼政策就難以推動
    - **結論**：能源安全是動機之一，但政策補貼才是決定 EV 滲透率的關鍵變數
    """)



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