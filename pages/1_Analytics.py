import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    load_data,
    filter_data,
    style_chart,
    apply_page_style
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Analytics | Anime Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# APPLY UI
# ============================================================

apply_page_style()


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("Analytics")

st.sidebar.caption(
    "Deep analysis & statistical exploration"
)

st.sidebar.divider()


# ------------------------------------------------------------
# FILTER OPTIONS
# ------------------------------------------------------------

genres = sorted(
    df["Genre"].unique()
)

studios = sorted(
    df["Studio"].unique()
)

ratings = sorted(
    df["Rating"].unique()
)

anime_names = sorted(
    df["Anime_Name"].unique()
)


# ------------------------------------------------------------
# GENRE
# ------------------------------------------------------------

selected_genres = st.sidebar.multiselect(
    "Genre",
    genres,
    default=genres
)


# ------------------------------------------------------------
# STUDIO
# ------------------------------------------------------------

selected_studios = st.sidebar.multiselect(
    "Studio",
    studios,
    default=studios
)


# ------------------------------------------------------------
# RATING
# ------------------------------------------------------------

selected_ratings = st.sidebar.multiselect(
    "Rating",
    ratings,
    default=ratings
)


# ------------------------------------------------------------
# ANIME
# ------------------------------------------------------------

selected_anime = st.sidebar.multiselect(
    "Anime",
    anime_names,
    default=anime_names
)


# ============================================================
# FILTER DATA
# ============================================================

data = filter_data(
    df,
    selected_genres,
    selected_studios,
    selected_ratings,
    selected_anime
)


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if data.empty:

    st.error(
        "No records match the selected filters."
    )

    st.info(
        "Try selecting more genres, studios, ratings or anime."
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="section-badge">ADVANCED ANALYTICS</div>',
    unsafe_allow_html=True
)

st.title("Data Intelligence")

st.caption(
    "Explore score behaviour, genre patterns, studio "
    "performance and relationships between numerical variables."
)

st.divider()


# ============================================================
# KPI SECTION
# ============================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.metric(
        "Records Analyzed",
        f"{len(data):,}"
    )


with k2:

    st.metric(
        "Average Score",
        f"{data['Score'].mean():.2f}"
    )


with k3:

    st.metric(
        "Average Episodes",
        f"{data['Episodes'].mean():.1f}"
    )


with k4:

    st.metric(
        "Average Popularity",
        f"{data['Popularity'].mean():,.0f}"
    )


st.write("")


# ============================================================
# GENRE INTELLIGENCE
# ============================================================

st.header("Genre Intelligence")

st.caption(
    "Compare score behaviour and score distribution across genres."
)


left, right = st.columns(2)


# ============================================================
# AVERAGE SCORE BY GENRE
# ============================================================

with left:

    genre_stats = (
        data
        .groupby("Genre")
        .agg(
            Average_Score=("Score", "mean"),
            Median_Score=("Score", "median"),
            Records=("Score", "count")
        )
        .reset_index()
        .sort_values(
            "Average_Score",
            ascending=True
        )
    )


    fig = px.bar(

        genre_stats,

        x="Average_Score",

        y="Genre",

        orientation="h",

        text="Average_Score",

        title="Average Score by Genre",

        hover_data=[
            "Median_Score",
            "Records"
        ]
    )


    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside",

        marker_line_width=0
    )


    fig.update_xaxes(
        range=[
            max(
                0,
                genre_stats["Average_Score"].min() - 0.5
            ),
            10.5
        ]
    )


    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True
    )


# ============================================================
# SCORE DISTRIBUTION BY GENRE
# ============================================================

with right:

    fig = px.box(

        data,

        x="Genre",

        y="Score",

        color="Genre",

        points="all",

        title="Score Distribution by Genre",

        hover_data=[
            "Anime_Name",
            "Studio"
        ]
    )


    fig.update_layout(
        showlegend=False
    )


    fig.update_traces(
        marker_size=5,
        jitter=0.25,
        opacity=0.65
    )


    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True
    )


# ============================================================
# STUDIO INTELLIGENCE
# ============================================================

st.header("Studio Intelligence")

st.caption(
    "Compare studio score performance and score variability."
)


left, right = st.columns(2)


# ============================================================
# AVERAGE SCORE BY STUDIO
# ============================================================

with left:

    studio_stats = (
        data
        .groupby("Studio")
        .agg(
            Average_Score=("Score", "mean"),
            Median_Score=("Score", "median"),
            Records=("Score", "count")
        )
        .reset_index()
        .sort_values(
            "Average_Score",
            ascending=True
        )
    )


    fig = px.bar(

        studio_stats,

        x="Average_Score",

        y="Studio",

        orientation="h",

        text="Average_Score",

        title="Average Score by Studio",

        hover_data=[
            "Median_Score",
            "Records"
        ]
    )


    fig.update_traces(

        texttemplate="%{text:.2f}",

        textposition="outside",

        marker_line_width=0
    )


    fig.update_xaxes(
        range=[
            max(
                0,
                studio_stats["Average_Score"].min() - 0.5
            ),
            10.5
        ]
    )


    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True
    )


# ============================================================
# SCORE DISTRIBUTION BY STUDIO
# ============================================================

with right:

    fig = px.box(

        data,

        x="Studio",

        y="Score",

        color="Studio",

        points="all",

        title="Score Distribution by Studio"
    )


    fig.update_layout(
        showlegend=False
    )


    fig.update_traces(
        marker_size=5,
        jitter=0.25,
        opacity=0.65
    )


    st.plotly_chart(
        style_chart(fig, 470),
        use_container_width=True
    )


# ============================================================
# CORRELATION INTELLIGENCE
# ============================================================

st.header("Correlation Intelligence")

st.caption(
    "Correlation measures the linear relationship between "
    "the numerical variables in the selected dataset."
)


numeric = data[
    [
        "Episodes",
        "Score",
        "Popularity"
    ]
]


correlation = numeric.corr()


fig = px.imshow(

    correlation,

    text_auto=".2f",

    aspect="auto",

    color_continuous_scale=[
        "#111827",
        "#312e81",
        "#4f46e5",
        "#818cf8",
        "#c4b5fd"
    ],

    title="Numerical Correlation Matrix"
)


fig.update_layout(
    coloraxis_colorbar=dict(
        title="Correlation"
    )
)


st.plotly_chart(
    style_chart(fig, 500),
    use_container_width=True
)


# ============================================================
# CORRELATION METRICS
# ============================================================

c1, c2, c3 = st.columns(3)


with c1:

    value = correlation.loc[
        "Episodes",
        "Score"
    ]

    st.metric(
        "Episodes ↔ Score",
        f"{value:.3f}"
    )


with c2:

    value = correlation.loc[
        "Popularity",
        "Score"
    ]

    st.metric(
        "Popularity ↔ Score",
        f"{value:.3f}"
    )


with c3:

    value = correlation.loc[
        "Episodes",
        "Popularity"
    ]

    st.metric(
        "Episodes ↔ Popularity",
        f"{value:.3f}"
    )


# ============================================================
# RELATIONSHIP EXPLORER
# ============================================================

st.header("Relationship Explorer")

st.caption(
    "Interactive exploration of numerical relationships."
)


left, right = st.columns(2)


# ============================================================
# EPISODES VS SCORE
# ============================================================

with left:

    fig = px.scatter(

        data,

        x="Episodes",

        y="Score",

        color="Genre",

        size="Popularity",

        size_max=18,

        opacity=0.75,

        hover_name="Anime_Name",

        hover_data=[
            "Studio",
            "Rating"
        ],

        title="Episodes vs Score"
    )


    fig.update_traces(
        marker_line_width=0
    )


    st.plotly_chart(
        style_chart(fig, 500),
        use_container_width=True
    )


# ============================================================
# POPULARITY VS SCORE
# ============================================================

with right:

    fig = px.scatter(

        data,

        x="Popularity",

        y="Score",

        color="Studio",

        size="Episodes",

        size_max=18,

        opacity=0.75,

        hover_name="Anime_Name",

        hover_data=[
            "Genre",
            "Rating"
        ],

        title="Popularity vs Score"
    )


    fig.update_traces(
        marker_line_width=0
    )


    st.plotly_chart(
        style_chart(fig, 500),
        use_container_width=True
    )


# ============================================================
# GENRE × STUDIO
# ============================================================

st.header("Genre × Studio Intelligence")

st.caption(
    "Number of anime records represented across each "
    "genre and studio combination."
)


cross_table = pd.crosstab(
    data["Genre"],
    data["Studio"]
)


fig = px.imshow(

    cross_table,

    text_auto=True,

    aspect="auto",

    color_continuous_scale=[
        "#111827",
        "#312e81",
        "#4f46e5",
        "#818cf8",
        "#c4b5fd"
    ],

    title="Records by Genre and Studio"
)


st.plotly_chart(
    style_chart(fig, 520),
    use_container_width=True
)


# ============================================================
# ANIME PERFORMANCE
# ============================================================

st.header("Anime Performance Snapshot")

st.caption(
    "Aggregated performance statistics for each anime "
    "within the current filter selection."
)


anime_stats = (
    data
    .groupby("Anime_Name")
    .agg(
        Average_Score=("Score", "mean"),
        Average_Episodes=("Episodes", "mean"),
        Average_Popularity=("Popularity", "mean"),
        Records=("Score", "count")
    )
    .reset_index()
    .sort_values(
        "Average_Score",
        ascending=False
    )
)


display_table = anime_stats.copy()


display_table["Average_Score"] = (
    display_table["Average_Score"]
    .round(2)
)


display_table["Average_Episodes"] = (
    display_table["Average_Episodes"]
    .round(1)
)


display_table["Average_Popularity"] = (
    display_table["Average_Popularity"]
    .round(0)
    .astype(int)
)


st.dataframe(

    display_table,

    use_container_width=True,

    height=420,

    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Anime Analytics • Advanced Analytics Module"
)