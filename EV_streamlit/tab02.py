<<<<<<< HEAD
import streamlit as st
import plotly.graph_objects as go

def oil_vs_EVsales (sales, oil):
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
=======
import streamlit as st
import plotly.graph_objects as go

def oil_vs_EVsales (sales, oil):
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
>>>>>>> 0a028230a856525701a004dd000b3e048add00da
            st.metric("EV銷售成長", "+55%")