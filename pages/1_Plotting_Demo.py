import pandas as pd
import streamlit as st
from streamlit_vizzu import Config, Data, Style, VizzuChart

df = pd.read_csv("music_data.csv", sep=",", encoding='Latin-1')
st.table(df[0:4])

data = Data()
data.add_data_frame(df)

chart = VizzuChart(key="vizzu", height=380)
chart.animate(data)
chart.feature("tooltip", True)

chart.animate(
    Config(
        {
            "channels": {
                "y": {"set": ["Popularity"]},
                "x": {"set": ["Genres"]},
            }
        }
    )
)
chart.animate(
    Config({"channels": {"label": {"attach": ["Popularity"]}}})
)

chart.show()