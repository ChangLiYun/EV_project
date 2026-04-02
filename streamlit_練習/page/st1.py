import streamlit as st
import pandas as pd

st.title("streamlit button 展示")
click1 = st.button("這是button-1",key="btn1",type="primary",icon="🧛")
click2 = st.button("這是button-2",key="btn2",type="secondary",icon ="🧠" )

if click1 :
    st.write("William 我是不會屈服的!!!")
if click2:
    st.header("button2 !!")

def open_excel():
    st.write("開啟 油價與EV銷售_年均 檔案")
    df = pd.read_excel("C:\\Users\\FM_pc\\Desktop\\專\\油價與EV銷售_年均.xlsx")
    st.dataframe(df)
def open_excel2():
    st.write("各國政策已達成項目")
    df1 = pd.read_excel("C:\\Users\\FM_pc\\Desktop\\專\\IEA_PAMS_Export_Achieved.xlsx")
    st.dataframe(df1)

def open_pdf():
    st.write("GlobalEVOutlook2025PolicyExplorer")
    df2 = st.pdf("file:///C:/Users/FM_pc/Desktop/%E5%B0%88/GlobalEVOutlook2025PolicyExplorer.pdf")
st.button("IEA_PAMS_Export_Achieved",on_click=open_excel2, icon="📑", type="tertiary")
st.button("IEA_pfda",on_click= open_pdf,type="tertiary" )