<<<<<<< HEAD
# tab01.py
import streamlit as st
import plotly.express as px

def render_market_overview(sales):
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

    st.markdown("**分析結論**：2021年是關鍵爆發點...")
=======
# tab01.py
import streamlit as st
import plotly.express as px

def render_market_overview(sales):
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

    st.markdown("**分析結論**：2021年是關鍵爆發點...")
>>>>>>> 0a028230a856525701a004dd000b3e048add00da
