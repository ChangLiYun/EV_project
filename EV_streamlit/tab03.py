import streamlit as st
import pandas as pd

def Policy_timeline (policy):
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

