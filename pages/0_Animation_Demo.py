from typing import List
import pandas as pd
import streamlit as st
import numpy as np
from streamlit_vizzu import Config, Data, Style, VizzuChart
#import streamlit_elements as elements

df = pd.read_csv("sales_data_sample.csv", sep=",", encoding='Latin-1')
st.table(df[0:4])

data = Data()
data.add_data_frame(df)

#Make a slider
#yearValue = st.slider("Pick a year", min_value=2002, max_value=2005, value=2003)
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
filter_format = (
    "(" + " || ".join([f"record['Format'] == '{item}'" for item in items]) + ")"
)
formatFilter = "record['PRODUCTLINE'] in items"

chart2 = VizzuChart(height=380)
chart2.animate(data)
chart2.feature("tooltip", True)
filters = "{} and {}".format(yearFilter, formatFilter)
chart2.animate(
    Data.filter(filters),
    Config(
        {
            "channels": {
                "y": {"set": ["STATUS"]},
                "x": {"set": ["ORDERNUMBER"]},
            }
        }
    )
)

chart2.show()