<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def trendline(ev,oil):
    st.subheader("EV 銷售趨勢分析與預測（2010–2024）")

    # ── 準備資料 ──────────────────────────────
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # 油價年均
    oil_yearly = oil.copy()  # 已在 load_data() 裡處理好

    # EV 全球歷史銷售
    ev_world = ev[
        (ev["parameter"] == "EV sales") &
        (ev["region_country"] == "World") &
        (ev["mode"] == "Cars") &
        (ev["category"] == "Historical") &
        (ev["powertrain"].isin(["BEV", "PHEV"]))
        ].groupby("year")["value"].sum().reset_index()
    ev_world.columns = ["year", "ev_sales"]

    # 合併
    df_reg = pd.merge(oil_yearly, ev_world, on="year")

    # ── 兩個迴歸模型 ──────────────────────────
    X_oil = df_reg[["brent"]]
    X_year = df_reg[["year"]]
    y = df_reg["ev_sales"]

    model_oil = LinearRegression().fit(X_oil, y)
    model_year = LinearRegression().fit(X_year, y)

    r2_oil = model_oil.score(X_oil, y)
    r2_year = model_year.score(X_year, y)
    coef_year = model_year.coef_[0]

    # ── KPI 對比 ──────────────────────────────
    st.markdown("#### 兩個迴歸模型對比")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="油價迴歸 R²",
            value=f"{r2_oil:.4f}",
            delta="解釋力不到 0.2%",
            delta_color="inverse"
        )
        st.caption("自變數：布蘭特原油年均價")

    with col2:
        st.metric(
            label="時間趨勢迴歸 R²",
            value=f"{r2_year:.4f}",
            delta=f"每年平均成長 {coef_year / 1e6:.2f} 百萬輛"
        )
        st.caption("自變數：年份（結構性成長）")

    st.info(
        f"**結論**：油價的解釋力僅 {r2_oil:.3f}（≈0），"
        f"時間趨勢的解釋力達 {r2_year:.2f}（70%）。"
        "EV 市場成長是結構性的長期趨勢，不受短期油價波動影響。"
    )

    # ── 圖一：油價迴歸散佈圖 ──────────────────
    st.markdown("#### 圖1：油價 vs EV 銷售（線性迴歸）")

    x_line = np.linspace(df_reg["brent"].min(), df_reg["brent"].max(), 100)
    y_line = model_oil.predict(x_line.reshape(-1, 1))

    fig_reg = go.Figure()

    # 散佈點
    fig_reg.add_trace(go.Scatter(
        x=df_reg["brent"],
        y=df_reg["ev_sales"] / 1e6,
        mode="markers+text",
        text=df_reg["year"].astype(str),
        textposition="top center",
        marker=dict(color="#1D9E75", size=10),
        name="實際數據"
    ))

    # 迴歸線
    fig_reg.add_trace(go.Scatter(
        x=x_line,
        y=y_line / 1e6,
        mode="lines",
        line=dict(color="#E24B4A", dash="dash", width=2),
        name=f"迴歸線（R²={r2_oil:.3f}）"
    ))

    fig_reg.update_layout(
        xaxis_title="布蘭特原油年均價（USD/桶）",
        yaxis_title="EV 銷售量（百萬輛）",
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    # ── 圖二：時間趨勢迴歸 ────────────────────
    st.markdown("#### 圖2：時間趨勢迴歸（年份 vs EV 銷售）")

    x_year_line = np.linspace(2010, 2030, 100)
    y_year_line = model_year.predict(x_year_line.reshape(-1, 1))

    # IEA 預測點
    iea_years = [2025, 2030]
    iea_values = [20700000, 40000000]

    fig_trend = go.Figure()

    # 歷史實際值
    fig_trend.add_trace(go.Scatter(
        x=df_reg["year"],
        y=df_reg["ev_sales"] / 1e6,
        mode="markers+text",
        text=df_reg["year"].astype(str),
        textposition="top center",
        marker=dict(color="#1D9E75", size=10),
        name="歷史實際值"
    ))

    # 迴歸線（延伸到 2030）
    fig_trend.add_trace(go.Scatter(
        x=x_year_line,
        y=y_year_line / 1e6,
        mode="lines",
        line=dict(color="#185FA5", dash="dash", width=2),
        name=f"線性趨勢（R²={r2_year:.3f}）"
    ))

    # IEA 預測點
    fig_trend.add_trace(go.Scatter(
        x=iea_years,
        y=[v / 1e6 for v in iea_values],
        mode="markers+text",
        text=["IEA 2025\n預估", "IEA 2030\nSTEPS"],
        textposition="top center",
        marker=dict(color="#EF9F27", size=14, symbol="diamond"),
        name="IEA 預測"
    ))

    fig_trend.add_vline(
        x=2024, line_dash="dot", line_color="gray",
        annotation_text="← 歷史 | 預測 →"
    )

    fig_trend.update_layout(
        xaxis_title="年份",
        yaxis_title="EV 銷售量（百萬輛）",
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── 迴歸方法說明 ──────────────────────────
    with st.expander("什麼是線性迴歸？"):
        st.markdown("""
           **線性迴歸**是找一條最能代表資料趨勢的直線，公式為：

           > **y = a × x + b**

           - **y**：要預測的值（EV 銷售量）
           - **x**：用來預測的變數（油價 或 年份）
           - **a**：斜率，x 每變化 1 單位，y 變化多少
           - **b**：截距，x 為 0 時 y 的理論值

           **R²（決定係數）** 衡量這條線有多準：
           - R² = 1.0：完美預測
           - R² = 0.7：能解釋 70% 的變化
           - R² ≈ 0：幾乎沒有解釋力

           本研究用兩個自變數分別跑迴歸，對比結果直接說明
           「油價不是驅動力，時間結構性成長才是」。
=======
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def trendline(ev,oil):
    st.subheader("EV 銷售趨勢分析與預測（2010–2024）")

    # ── 準備資料 ──────────────────────────────
    from sklearn.linear_model import LinearRegression
    import numpy as np

    # 油價年均
    oil_yearly = oil.copy()  # 已在 load_data() 裡處理好

    # EV 全球歷史銷售
    ev_world = ev[
        (ev["parameter"] == "EV sales") &
        (ev["region_country"] == "World") &
        (ev["mode"] == "Cars") &
        (ev["category"] == "Historical") &
        (ev["powertrain"].isin(["BEV", "PHEV"]))
        ].groupby("year")["value"].sum().reset_index()
    ev_world.columns = ["year", "ev_sales"]

    # 合併
    df_reg = pd.merge(oil_yearly, ev_world, on="year")

    # ── 兩個迴歸模型 ──────────────────────────
    X_oil = df_reg[["brent"]]
    X_year = df_reg[["year"]]
    y = df_reg["ev_sales"]

    model_oil = LinearRegression().fit(X_oil, y)
    model_year = LinearRegression().fit(X_year, y)

    r2_oil = model_oil.score(X_oil, y)
    r2_year = model_year.score(X_year, y)
    coef_year = model_year.coef_[0]

    # ── KPI 對比 ──────────────────────────────
    st.markdown("#### 兩個迴歸模型對比")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="油價迴歸 R²",
            value=f"{r2_oil:.4f}",
            delta="解釋力不到 0.2%",
            delta_color="inverse"
        )
        st.caption("自變數：布蘭特原油年均價")

    with col2:
        st.metric(
            label="時間趨勢迴歸 R²",
            value=f"{r2_year:.4f}",
            delta=f"每年平均成長 {coef_year / 1e6:.2f} 百萬輛"
        )
        st.caption("自變數：年份（結構性成長）")

    st.info(
        f"**結論**：油價的解釋力僅 {r2_oil:.3f}（≈0），"
        f"時間趨勢的解釋力達 {r2_year:.2f}（70%）。"
        "EV 市場成長是結構性的長期趨勢，不受短期油價波動影響。"
    )

    # ── 圖一：油價迴歸散佈圖 ──────────────────
    st.markdown("#### 圖1：油價 vs EV 銷售（線性迴歸）")

    x_line = np.linspace(df_reg["brent"].min(), df_reg["brent"].max(), 100)
    y_line = model_oil.predict(x_line.reshape(-1, 1))

    fig_reg = go.Figure()

    # 散佈點
    fig_reg.add_trace(go.Scatter(
        x=df_reg["brent"],
        y=df_reg["ev_sales"] / 1e6,
        mode="markers+text",
        text=df_reg["year"].astype(str),
        textposition="top center",
        marker=dict(color="#1D9E75", size=10),
        name="實際數據"
    ))

    # 迴歸線
    fig_reg.add_trace(go.Scatter(
        x=x_line,
        y=y_line / 1e6,
        mode="lines",
        line=dict(color="#E24B4A", dash="dash", width=2),
        name=f"迴歸線（R²={r2_oil:.3f}）"
    ))

    fig_reg.update_layout(
        xaxis_title="布蘭特原油年均價（USD/桶）",
        yaxis_title="EV 銷售量（百萬輛）",
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig_reg, use_container_width=True)

    # ── 圖二：時間趨勢迴歸 ────────────────────
    st.markdown("#### 圖2：時間趨勢迴歸（年份 vs EV 銷售）")

    x_year_line = np.linspace(2010, 2030, 100)
    y_year_line = model_year.predict(x_year_line.reshape(-1, 1))

    # IEA 預測點
    iea_years = [2025, 2030]
    iea_values = [20700000, 40000000]

    fig_trend = go.Figure()

    # 歷史實際值
    fig_trend.add_trace(go.Scatter(
        x=df_reg["year"],
        y=df_reg["ev_sales"] / 1e6,
        mode="markers+text",
        text=df_reg["year"].astype(str),
        textposition="top center",
        marker=dict(color="#1D9E75", size=10),
        name="歷史實際值"
    ))

    # 迴歸線（延伸到 2030）
    fig_trend.add_trace(go.Scatter(
        x=x_year_line,
        y=y_year_line / 1e6,
        mode="lines",
        line=dict(color="#185FA5", dash="dash", width=2),
        name=f"線性趨勢（R²={r2_year:.3f}）"
    ))

    # IEA 預測點
    fig_trend.add_trace(go.Scatter(
        x=iea_years,
        y=[v / 1e6 for v in iea_values],
        mode="markers+text",
        text=["IEA 2025\n預估", "IEA 2030\nSTEPS"],
        textposition="top center",
        marker=dict(color="#EF9F27", size=14, symbol="diamond"),
        name="IEA 預測"
    ))

    fig_trend.add_vline(
        x=2024, line_dash="dot", line_color="gray",
        annotation_text="← 歷史 | 預測 →"
    )

    fig_trend.update_layout(
        xaxis_title="年份",
        yaxis_title="EV 銷售量（百萬輛）",
        legend=dict(x=0, y=1)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── 迴歸方法說明 ──────────────────────────
    with st.expander("什麼是線性迴歸？"):
        st.markdown("""
           **線性迴歸**是找一條最能代表資料趨勢的直線，公式為：

           > **y = a × x + b**

           - **y**：要預測的值（EV 銷售量）
           - **x**：用來預測的變數（油價 或 年份）
           - **a**：斜率，x 每變化 1 單位，y 變化多少
           - **b**：截距，x 為 0 時 y 的理論值

           **R²（決定係數）** 衡量這條線有多準：
           - R² = 1.0：完美預測
           - R² = 0.7：能解釋 70% 的變化
           - R² ≈ 0：幾乎沒有解釋力

           本研究用兩個自變數分別跑迴歸，對比結果直接說明
           「油價不是驅動力，時間結構性成長才是」。
>>>>>>> 0a028230a856525701a004dd000b3e048add00da
           """)