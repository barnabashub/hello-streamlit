import pandas as pd
from ipyvizzu import Chart, Data, Config, DisplayTarget
from streamlit_vizzu import VizzuChart

df = pd.read_csv(
    "https://ipyvizzu.vizzuhq.com/0.16/assets/data/music_data.csv"
)
data1 = Data()
data1.add_df(df)

chart = VizzuChart(height=380)

chart.animate(data1)

chart.animate(
    Config(
        {
            "channels": {
                "y": {"set": ["Popularity", "Kinds"]},
                "x": {"set": ["Genres"]},
                "color": {"set": ["Kinds"]},
                "label": {"set": ["Popularity"]},
            },
        }
    )
)
filter1 = Data.filter(
    "record['Genres'] == 'Pop' || record['Genres'] == 'Metal'"
)

chart.animate(filter1)

chart.show()