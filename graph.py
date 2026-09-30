import pandas as pd
import plotly.express as px

df = pd.read_csv("anime_dataset.csv")

# Create scatter plot
fig = px.scatter(
    df,
    x="Popularity",
    y="Score",
    title="Popularity vs Anime Score",
    hover_data=["Anime_Name", "Genre", "Studio", "Rating", "Episodes"]
)

fig.show()