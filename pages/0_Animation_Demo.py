from typing import List
import pandas as pd
import streamlit as st
import numpy as np
from streamlit_vizzu import Config, Data, Style, VizzuChart
from ipyvizzu.animation import Config, Data, Style
from ipyvizzustory import Slide, Step
from ipyvizzustory.env.py.story import Story
from ipyvizzustory import Story

df = pd.read_csv("sales_data_sample.csv", sep=",", encoding='Latin-1')
st.table(df[0:4])

data = Data()
data.add_data_frame(df)
story = Story(data=data)
st.session_state.story = Story(data)

if "lastanim" not in st.session_state:
    st.session_state.lastanim = []

# Make a slider
year1, year2 = st.select_slider(
    "Time range", options=map(str, np.arange(2002, 2006)), value=("2004", "2005")
)
yearFilter = "record['YEAR_ID'] >= '{yearMin}' && record['YEAR_ID'] <= '{yearMax}'".format(
    yearMin=year1, yearMax=year2)

# Make select for productline
st.write("You should select the product types to see the diagrams.")
allFormats = df["PRODUCTLINE"].unique()
defaultFormats = []
items: List[str] = st.multiselect(
    "Product line", allFormats, defaultFormats, key="multiselect"
)
format_filter = "("
for item in items:
    if format_filter != "(":
        format_filter += " || "
    format_filter += "record['PRODUCTLINE'] == '" + item + "'"
format_filter += ")"

chart2 = VizzuChart(height=380)
chart2.animate(data)
chart2.feature("tooltip", True)
filters = "{} && {}".format(yearFilter, format_filter)
bar_clicked = chart2.get("marker.categories.STATUS")

st.write("Here you can see the statistics about the actual status of the ordered items.")
st.write("If you click on a bar you can see the status distribution between the item categories.")

if bar_clicked is None:

    chart2.animate(

        Data.filter(filters),
        Config(
            {
                "channels": {
                    "y": {"set": ["STATUS"]},
                    "x": {"set": ["QUANTITYORDERED"]},
                }
            }
        )
    )
    


else:
    chart2.animate(
        Data.filter("record['STATUS'] == '{}' && {}".format(
            bar_clicked, yearFilter)),
        Config(
            {
                "channels": {
                    "y": {"set": ["PRODUCTLINE"]},
                    "x": {"set": ["QUANTITYORDERED"]},
                }
            }
        )
    )

# -- display chart --
st.session_state.lastanim = [Data.filter(filters), Config("""{
                "channels": {
                    "y": {"set": ["STATUS"]},
                    "x": {"set": ["QUANTITYORDERED"]},
                }
            }""")]
output = chart2.show()


# Make treemap chart for countries
st.write("In this treemap, you can see the distribution of the countries, who ordered the items and the size of them shows us the sum of ordered quantites.")
treemap = VizzuChart(height=380, key="treemapvizzu")
treemap.animate(data)
treemap.feature("tooltip", True)

treemap.animate(
    Data.filter(filters),
    Config(
        {
            "channels": {
                "label": "COUNTRY",
                "size": "QUANTITYORDERED",
                "color": "COUNTRY",
            },
            "title": "Treemap",
        }
    )
)
treemap.show()

# Make donut chart for dealsizes
st.write("The donut diagram shows us the distribution of the income between the size of the deals.")
donut = VizzuChart(height=380, key="donutvizzu")
donut.animate(data)
donut.feature("tooltip", True)
donut.animate(
    Data.filter(filters),
    Config(
        {
            "channels": {
                "x": "DEALSIZE",
                "y": "SALES",
#{"range": {"min": "0%"}},
                "color": "DEALSIZE"
            },
            "title": "Donut Chart",
            "coordSystem": "polar",
        }
    )
)
donut.show()


# Save vizzu story

save_all = st.checkbox("Save all", value=True)
save_button = st.button("Save animation")
print(st.session_state.lastanim)
if st.session_state.lastanim:
    if save_all:
        st.session_state.story.add_slide(
            Slide(Step(*st.session_state.lastanim)))
    else:
        if save_button:
            st.session_state.story.add_slide(
                Slide(Step(*st.session_state.lastanim)))

download_button = st.download_button(
    label="Download Story",
    data=st.session_state.story.to_html(),
    file_name="story.html",
    mime="text/html",
)

print(st.session_state.story.items)