import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def test ():
    # 在 Tab2（油價與EV關係）或獨立 Tab 裡加這段

    st.subheader("能源進口依賴度 vs EV 滲透率（2024）")

    geo_data = pd.DataFrame({
        "國家": ["挪威", "美國", "中國", "英國", "瑞典", "丹麥", "芬蘭",
                 "法國", "德國", "荷蘭", "比利時", "奧地利", "葡萄牙",
                 "以色列", "日本", "韓國", "義大利", "西班牙", "印度"],
        "能源進口依賴度": [-741, -8, 18, 36, -64, -10, -35, 49, 61, 99,
                           87, 64, 73, 87, 90, 85, 84, 73, 44],
        "EV滲透率": [92, 10, 48, 28, 58, 56, 50, 24, 19, 48,
                     43, 24, 33, 21, 3, 9, 4, 5, 2],
        "地區": ["北歐", "北美", "亞洲", "歐洲", "北歐", "北歐", "北歐",
                 "歐洲", "歐洲", "歐洲", "歐洲", "歐洲", "歐洲",
                 "中東", "亞洲", "亞洲", "歐洲", "歐洲", "亞洲"],
        "主要動機": [
            "氣候生存威脅", "產業競爭力", "能源安全+工業戰略",
            "工業競爭+氣候", "氣候生存威脅", "氣候生存威脅", "氣候生存威脅",
            "氣候+工業競爭", "能源主權+工業競爭", "氣候+工業競爭",
            "氣候+工業競爭", "氣候+工業競爭", "氣候+工業競爭",
            "能源孤島生存", "能源安全", "能源安全",
            "氣候+工業競爭", "氣候+工業競爭", "能源安全"
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