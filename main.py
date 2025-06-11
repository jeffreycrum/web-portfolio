import streamlit as st


st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

with col1:
    st.image("images/IMG_2797.JPG")

with col2:
    st.title("Jeffrey Crum")
    content = """
    Hi I'm Jeff. \n
    Programmer. Real Estate Investor. Traveler. Foodie. Fun \n
    Scala, Python, PHP. 
    """
    st.write(content)
