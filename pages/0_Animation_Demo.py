from typing import List
import pandas as pd
import streamlit as st
import numpy as np
from streamlit_vizzu import Config, Data, Style, VizzuChart

df = pd.read_csv("sales_data_sample.csv", sep=",", encoding='Latin-1')
st.table(df[0:4])

data = Data()
data.add_data_frame(df)

#Make a slider
year1, year2 = st.select_slider(
    "Time range", options=map(str, np.arange(2002, 2006)), value=("2004", "2005")
)
yearFilter = "record['YEAR_ID'] >= '{yearMin}' && record['YEAR_ID'] <= '{yearMax}'".format(yearMin = year1, yearMax = year2)

# Make select for productline
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
print(bar_clicked)
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
        Data.filter("record['STATUS'] == '{}'".format(bar_clicked)),
        Config(
            {
                "channels": {
                    "y": {"set": ["PRODUCTLINE"]},
                    "x": {"set": ["YEAR_ID"]},
                }
            }
        )
    )

chart2.show()