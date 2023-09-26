import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, Style, VizzuChart
#import streamlit_elements as elements

df = pd.read_csv("sales_data_sample.csv", sep=",", encoding='Latin-1')
st.table(df[0:4])

data = Data()
data.add_data_frame(df)

#Make a slider
yearValue = st.slider("Pick a year", min_value=2002, max_value=2005, value=2003)

#Make checkbox for years

#Make checkbox for quaerter year

chart2 = VizzuChart(height=380)
chart2.animate(data)
chart2.feature("tooltip", True)
yearFilter = "record['YEAR_ID'] == '{year}'".format(year = yearValue)
chart2.animate(
    Data.filter(yearFilter),
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