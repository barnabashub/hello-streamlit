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
        Data.filter("record['STATUS'] == '{}' && {}".format(bar_clicked, yearFilter)),
        Config(
            {
                "channels": {
                    "y": {"set": ["PRODUCTLINE"]},
                    "x": {"set": ["QUANTITYORDERED"]},
                }
            }
        )
    )

chart2.show()

#Make treemap chart for countries
treemap = VizzuChart(height=380, key="treemapvizzu")
treemap.animate(data)
treemap.feature("tooltip", True)

treemap.animate(
	Config(
	    {
	        "channels": {
	            "label": "PRODUCTLINE",
	            "size": "QUANTITYORDERED",
	        },
	        "title": "Treemap",
	    }
	)
)
treemap.show()

#Make donut chart for years
donut = VizzuChart(height=380, key="donutvizzu")
donut.animate(data)
donut.feature("tooltip", True)
donut.animate(
	Config(
	    {
	        "channels": {
	            "x": "COUNTRY",
	            "y": {"range": {"min": "-60%"}},
	            #"color": "Joy factors",
	            #"label": "YEAR_ID",
	        },
	        "title": "Donut Chart",
	        "coordSystem": "polar",
	    }
	)
)
donut.show()