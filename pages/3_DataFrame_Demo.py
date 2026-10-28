
import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(
    page_title="DataFrame Demo",
    page_icon="📊",
)

st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")

st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data
def get_UN_data():
    url = (
        "https://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        "/agri.csv.gz"
    )
    df = pd.read_csv(url)
    return df.set_index("Region")


try:
    df = get_UN_data()

    countries = st.multiselect(
        "Choose countries",
        list(df.index),
        ["China", "United States of America"],
    )

    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries].copy()
        data = data / 1000000.0

        st.write(
            "### Gross Agricultural Production ($B)",
            data.sort_index(),
        )

        data = data.T.reset_index()

        data = pd.melt(
            data,
            id_vars=["index"],
            var_name="Region",
            value_name="Gross Agricultural Product ($B)",
        ).rename(columns={"index": "year"})

        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X("year:T", title="Year"),
                y=alt.Y(
                    "Gross Agricultural Product ($B):Q",
                    stack=None,
                    title="Gross Agricultural Production ($B)",
                ),
                color=alt.Color("Region:N", title="Country"),
                tooltip=[
                    "year:T",
                    "Region:N",
                    "Gross Agricultural Product ($B):Q",
                ],
            )
        )

        st.altair_chart(chart, width="stretch")

except (URLError, OSError, ValueError) as e:
    st.error(
        "The agricultural data could not be loaded. "
        "Check your internet connection and try again."
    )
    st.caption(str(e))
