import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
from streamlit_vizzu import VizzuChart, Config, Data

LOGGER = get_logger(__name__)


# Create a VizzuChart object with the default height and width
chart = VizzuChart()

# Generate some data and add it to the chart
df = pd.DataFrame({"a": ["x", "y", "z"], "b": [1, 2, 3]})
data = Data()
data.add_data_frame(df)
chart.animate(data)

# Add some configuration to tell Vizzu how to display the data
chart.animate(Config({"x": "a", "y": "b", "title": "Look at my plot!"}))
#chart.animate(Config({"x": "b", "y": "a", "title": "Look at my plot!"}))

if st.checkbox("Swap"):
    chart.animate(Config({"y": "a", "x": "b", "title": "Swapped!"}))

if st.toggle("Order"): 
    chart.animate(
    Config(
        {
            "sort": "none",
            "reverse": True,
        }
    )
    )    
else:
    chart.animate(
    Config(
        {
            "sort": "byValue",
            "reverse": False,
        }
    )
    )

if st.button("Aggregate"):
    chart.animate(
    Config(
        {
            "channels": {
                "x": {"set": None},
            }
        }
        )
    )
    chart.animate(
    Config(
        {
            "channels": {
                "x": "a", "y": "b"
            }
        }
        )
    )

if "marker" in data:
    st.write("value of clicked bar:", data["marker"]["values"]["b"])


# Show the chart in the app!
#chart.show()
data = chart.show()
st.write(data)