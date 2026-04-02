import streamlit as st
import pandas as pd

st.title("練習")
#下拉選單
lang  = st.sidebar.selectbox("個人專長介紹: ",("Power BI", "Python", "SQL", "DAX"))
st.title("主要的content")

match lang:
    case "Power BI":
        st.subheader("你挑選Power BI")
    case "Python":
        st.subheader("你挑選Python")
    case "SQL":
        st.subheader("你挑選SQL")
    case "DAX":
        st.subheader("你挑選DAX")