import pandas
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
    st.info(content)

content2 = """
Below you can find some of the apps I've built in Python. Feel free to contact me!
"""
st.write(content2)

col3, col4 = st.columns(2)

df = pandas.read_csv("data.csv", sep=";")
half_df = len(df) // 2

with col3:
    for index, row in df[:half_df].iterrows():
        st.header(row['title'])
        st.write(row['description'])
        st.link_button(label=f"Github:{row['title']}", url=row['url'])
        st.image(f"images/{row['image']}")

with col4:
    for index, row in df[half_df:].iterrows():
        st.header(row['title'])
        st.write(row['description'])
        st.link_button(label=f"Github:{row['title']}", url=row['url'])
        st.image(f"images/{row['image']}")
