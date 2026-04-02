import streamlit as st


# lang = st.selectbox("請選擇: ", ("Java", "Python", "C#", "JavaScript"))



# st.write(f"挑選了 {lang}")

# def selectOption():
#     st.write(f"改變了選項2的內容 {st.session_state.o2item}")

# st.selectbox("選項2", 
#              ("Power BI", "DAX", "Power Query") , 
#              #觸發時間: 當 使用者改變選項時 會觸發 selectOption執行
#              on_change=selectOption,
#              #綁定 獨一值, 系統有一個特殊的儲存庫(st.session_state)會存放這些 key(變數)的值
#              key="o2item"
#              )
# ----------------------------------------------------------
#tab
tab1, tab2, tab3 = st.tabs(["圖1","圖2","圖3"])

with tab1:
    st.header("no.001")
    st.image("https://va-education-project.weebly.com/uploads/3/9/4/9/39491395/5764590_orig.jpg?292")

with tab2:
    st.header("no.002")
    st.image("https://static.wixstatic.com/media/9db320_6382e4e94b9041cfb4abb50b3925b19a~mv2.jpg/v1/fill/w_792,h_1000,al_c,q_85,usm_0.66_1.00_0.01/9db320_6382e4e94b9041cfb4abb50b3925b19a~mv2.jpg")

with tab3:
    st.header("no.003")
    st.image("https://tse1.mm.bing.net/th/id/OIP.NIv7piumtstG5CcBbauH8QHaF8?rs=1&pid=ImgDetMain&o=7&rm=3")
