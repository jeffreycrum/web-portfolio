from typing import Tuple

import pandas
import streamlit as st


def load_project_data(csv_path: str = "data.csv") -> pandas.DataFrame:
    """Load project data from CSV file."""
    return pandas.read_csv(csv_path)


def split_dataframe(df: pandas.DataFrame) -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    """Split dataframe into two roughly equal halves."""
    half_point = len(df) // 2
    return df[:half_point], df[half_point:]


def render_header_section() -> None:
    """Render the header section with profile image and bio."""
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


def render_intro_text() -> None:
    """Render the introductory text."""
    content = "Below you can find some of the apps I've built in Python. Feel free to contact me!"
    st.write(content)


def render_project_item(row: pandas.Series) -> None:
    """Render a single project item."""
    st.header(row['title'])
    st.write(row['description'])
    st.write(f"[Source Code: {row['title']}]({row['url']})")
    st.image(f"images/{row['image']}")


def render_projects_section(df: pandas.DataFrame) -> None:
    """Render the projects section with two columns."""
    col3, col4 = st.columns(2)
    first_half, second_half = split_dataframe(df)

    with col3:
        for index, row in first_half.iterrows():
            render_project_item(row)

    with col4:
        for index, row in second_half.iterrows():
            render_project_item(row)


def main() -> None:
    """Main function to run the Streamlit app."""
    st.set_page_config(layout="wide")

    render_header_section()
    render_intro_text()

    df = load_project_data()
    render_projects_section(df)


if __name__ == "__main__":
    main()
