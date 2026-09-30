import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Anime Analytics",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */

.stApp {
    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(99, 102, 241, 0.12),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(168, 85, 247, 0.10),
            transparent 28%
        ),
        #080b12;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ================================
   SIDEBAR
================================ */

section[data-testid="stSidebar"] {
    background: #0b0f17;
    border-right: 1px solid rgba(255,255,255,0.07);
}

section[data-testid="stSidebar"] h1 {
    color: #f8fafc;
}

section[data-testid="stSidebar"] p {
    color: #8f99aa;
}


/* ================================
   TITLE
================================ */

h1 {
    font-size: 46px !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px !important;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #c4b5fd,
            #93c5fd
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2 {
    color: #f8fafc !important;
    font-weight: 750 !important;
}

h3 {
    color: #e5e7eb !important;
}


/* ================================
   METRIC CARDS
================================ */

div[data-testid="stMetric"] {

    background:
        linear-gradient(
            145deg,
            #151b27,
            #0f141e
        );

    border: 1px solid rgba(255,255,255,0.07);

    border-radius: 18px;

    padding: 20px 22px;

    min-height: 125px;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.25);

    transition:
        transform 0.2s ease,
        border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {

    transform: translateY(-3px);

    border-color:
        rgba(129,140,248,0.45);
}

div[data-testid="stMetricLabel"] {

    color: #929aaa !important;

    font-size: 13px !important;

    font-weight: 650 !important;
}

div[data-testid="stMetricValue"] {

    color: #f8fafc !important;

    font-size: 31px !important;

    font-weight: 750 !important;
}


/* ================================
   BUTTONS
================================ */

.stButton button,
.stDownloadButton button {

    border-radius: 10px !important;

    border: 1px solid rgba(129,140,248,0.25) !important;

    background: #151a25 !important;

    color: #e5e7eb !important;

    transition: all 0.2s ease;
}

.stButton button:hover,
.stDownloadButton button:hover {

    border-color:
        rgba(129,140,248,0.7) !important;

    background: #1b2231 !important;

    color: white !important;
}


/* ================================
   SELECT BOXES
================================ */

div[data-baseweb="select"] > div {

    background: #111722 !important;

    border-color:
        rgba(255,255,255,0.08) !important;

    border-radius: 10px !important;
}


/* ================================
   MULTISELECT
================================ */

div[data-baseweb="select"] span {

    color: #e5e7eb !important;
}


/* ================================
   DATAFRAME
================================ */

div[data-testid="stDataFrame"] {

    border-radius: 14px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.06);
}


/* ================================
   DIVIDERS
================================ */

hr {

    border-color:
        rgba(255,255,255,0.07) !important;
}


/* ================================
   TABS
================================ */

button[data-baseweb="tab"] {

    color: #8f99aa !important;

    font-weight: 600 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {

    color: #c4b5fd !important;
}


/* ================================
   EXPANDER
================================ */

details {

    background: #111722 !important;

    border:
        1px solid rgba(255,255,255,0.07) !important;

    border-radius: 12px !important;
}


/* ================================
   SCROLLBAR
================================ */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #080b12;
}

::-webkit-scrollbar-thumb {
    background: #272d3a;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #3b4354;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv("anime_dataset.csv")

    data["Anime_Name"] = data["Anime_Name"].replace(
        "?", "Unknown"
    )

    data["Genre"] = data["Genre"].replace(
        "?", "Unknown"
    )

    data["Studio"] = data["Studio"].replace(
        "?", "Unknown"
    )

    return data


df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎌 Anime Analytics")

st.sidebar.caption(
    "Interactive anime data exploration"
)

st.sidebar.divider()

st.sidebar.subheader("🎛️ Dashboard Filters")


# Filter options

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


selected_genres = st.sidebar.multiselect(
    "Genre",
    genres,
    default=genres
)


selected_studios = st.sidebar.multiselect(
    "Studio",
    studios,
    default=studios
)


selected_ratings = st.sidebar.multiselect(
    "Rating",
    ratings,
    default=ratings
)


selected_anime = st.sidebar.multiselect(
    "Anime",
    anime_names,
    default=anime_names
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["Genre"].isin(selected_genres)
    &
    df["Studio"].isin(selected_studios)
    &
    df["Rating"].isin(selected_ratings)
    &
    df["Anime_Name"].isin(selected_anime)
].copy()


# ============================================================
# EMPTY FILTER
# ============================================================

if filtered_df.empty:

    st.error(
        "No records match the selected filters."
    )

    st.stop()


# ============================================================
# SIDEBAR SUMMARY
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("📌 Current Selection")

st.sidebar.metric(
    "Records",
    f"{len(filtered_df):,}"
)

percentage = (
    len(filtered_df) /
    len(df)
) * 100

st.sidebar.caption(
    f"{percentage:.1f}% of original dataset"
)


if st.sidebar.button(
    "↻ Reset Filters",
    use_container_width=True
):

    st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title("🎌 Anime Analytics")

st.caption(
    "Explore ratings, studios, genres, popularity and "
    "episode patterns through interactive data analysis."
)

st.divider()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_records = len(
    filtered_df
)

average_score = filtered_df[
    "Score"
].mean()

average_episodes = filtered_df[
    "Episodes"
].mean()

total_studios = filtered_df[
    "Studio"
].nunique()

average_popularity = filtered_df[
    "Popularity"
].mean()


# ============================================================
# KPI ROW
# ============================================================

k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.metric(
        "📊 Total Records",
        f"{total_records:,}"
    )


with k2:

    st.metric(
        "⭐ Average Score",
        f"{average_score:.2f}"
    )


with k3:

    st.metric(
        "🎬 Average Episodes",
        f"{average_episodes:.1f}"
    )


with k4:

    st.metric(
        "🏢 Studios",
        total_studios
    )


with k5:

    st.metric(
        "🔥 Avg Popularity",
        f"{average_popularity:,.0f}"
    )


st.write("")


# ============================================================
# PLOTLY THEME
# ============================================================

PLOT_BG = "#111722"

GRID_COLOR = "rgba(255,255,255,0.07)"

FONT_COLOR = "#e5e7eb"


def style_chart(
    fig,
    height=430
):

    fig.update_layout(

        template="plotly_dark",

        height=height,

        paper_bgcolor=PLOT_BG,

        plot_bgcolor=PLOT_BG,

        font=dict(
            color=FONT_COLOR,
            family="Arial"
        ),

        margin=dict(
            l=30,
            r=25,
            t=65,
            b=35
        ),

        title=dict(
            font=dict(
                size=20,
                color="#f8fafc"
            )
        ),

        xaxis=dict(
            gridcolor=GRID_COLOR,
            zeroline=False
        ),

        yaxis=dict(
            gridcolor=GRID_COLOR,
            zeroline=False
        ),

        hoverlabel=dict(
            bgcolor="#161c28",
            font_color="white",
            font_size=13
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    return fig


# ============================================================
# OVERVIEW
# ============================================================

st.header("Overview")

st.caption(
    "Understand the composition of the selected dataset."
)


c1, c2 = st.columns(2)


# ============================================================
# GENRE
# ============================================================

with c1:

    genre_data = (
        filtered_df["Genre"]
        .value_counts()
        .reset_index()
    )

    genre_data.columns = [
        "Genre",
        "Count"
    ]

    fig_genre = px.pie(
        genre_data,
        names="Genre",
        values="Count",
        hole=0.60,
        title="Genre Composition"
    )

    fig_genre.update_traces(

        textposition="inside",

        textinfo="percent",

        hovertemplate=
        "<b>%{label}</b><br>"
        "Records: %{value}<br>"
        "Share: %{percent}"
        "<extra></extra>"
    )

    fig_genre = style_chart(
        fig_genre,
        430
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )


# ============================================================
# RATING
# ============================================================

with c2:

    rating_data = (
        filtered_df["Rating"]
        .value_counts()
        .reset_index()
    )

    rating_data.columns = [
        "Rating",
        "Count"
    ]

    fig_rating = px.bar(
        rating_data,
        x="Rating",
        y="Count",
        text="Count",
        title="Rating Distribution"
    )

    fig_rating.update_traces(
        textposition="outside"
    )

    fig_rating = style_chart(
        fig_rating,
        430
    )

    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


# ============================================================
# RANKINGS
# ============================================================

st.header("Rankings")

st.caption(
    "Compare average scores across anime and studios."
)


c3, c4 = st.columns(2)


# ============================================================
# ANIME RANKING
# ============================================================

with c3:

    anime_score = (
        filtered_df
        .groupby("Anime_Name")["Score"]
        .mean()
        .reset_index()
        .sort_values(
            "Score",
            ascending=True
        )
    )

    fig_anime = px.bar(
        anime_score,
        x="Score",
        y="Anime_Name",
        orientation="h",
        text="Score",
        title="Average Score by Anime"
    )

    fig_anime.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_anime = style_chart(
        fig_anime,
        max(
            430,
            len(anime_score) * 38
        )
    )

    st.plotly_chart(
        fig_anime,
        use_container_width=True
    )


# ============================================================
# STUDIO RANKING
# ============================================================

with c4:

    studio_score = (
        filtered_df
        .groupby("Studio")["Score"]
        .mean()
        .reset_index()
        .sort_values(
            "Score",
            ascending=True
        )
    )

    fig_studio = px.bar(
        studio_score,
        x="Score",
        y="Studio",
        orientation="h",
        text="Score",
        title="Average Score by Studio"
    )

    fig_studio.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_studio = style_chart(
        fig_studio,
        max(
            430,
            len(studio_score) * 55
        )
    )

    st.plotly_chart(
        fig_studio,
        use_container_width=True
    )


# ============================================================
# RELATIONSHIPS
# ============================================================

st.header("Relationships")

st.caption(
    "Explore relationships between numerical variables."
)


c5, c6 = st.columns(2)


# ============================================================
# EPISODES VS SCORE
# ============================================================

with c5:

    fig_episodes = px.scatter(
        filtered_df,
        x="Episodes",
        y="Score",
        color="Genre",

        hover_data=[
            "Anime_Name",
            "Studio",
            "Rating"
        ],

        title="Episodes vs Score"
    )

    fig_episodes.update_traces(
        marker=dict(
            size=8,
            opacity=0.75
        )
    )

    fig_episodes = style_chart(
        fig_episodes,
        480
    )

    st.plotly_chart(
        fig_episodes,
        use_container_width=True
    )


# ============================================================
# POPULARITY VS SCORE
# ============================================================

with c6:

    fig_popularity = px.scatter(
        filtered_df,
        x="Popularity",
        y="Score",
        color="Studio",

        hover_data=[
            "Anime_Name",
            "Genre",
            "Rating",
            "Episodes"
        ],

        title="Popularity vs Score"
    )

    fig_popularity.update_traces(
        marker=dict(
            size=8,
            opacity=0.75
        )
    )

    fig_popularity = style_chart(
        fig_popularity,
        480
    )

    st.plotly_chart(
        fig_popularity,
        use_container_width=True
    )


# ============================================================
# DATASET
# ============================================================

st.header("Filtered Dataset")

st.caption(
    "Records currently selected by your filters."
)


st.dataframe(
    filtered_df,
    use_container_width=True,
    height=430
)


# ============================================================
# DOWNLOAD
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "⬇️ Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_anime_dataset.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎌 Anime Analytics • "
    "Python + Pandas + Plotly + Streamlit"
)