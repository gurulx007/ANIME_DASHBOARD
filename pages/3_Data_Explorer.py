import streamlit as st
import pandas as pd

from utils import load_data, apply_page_style


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Data Explorer | Anime Analytics",
    page_icon="🔎",
    layout="wide"
)

apply_page_style()

df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="section-badge">DATA EXPLORER</div>',
    unsafe_allow_html=True
)

st.title("Explore the Dataset")

st.caption(
    "Search, filter, inspect and download anime records."
)

st.divider()


# ============================================================
# SEARCH
# ============================================================

search = st.text_input(
    "🔍 Search Anime",
    placeholder="Search for an anime..."
)

data = df.copy()

if search:

    data = data[
        data["Anime_Name"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


# ============================================================
# FILTERS
# ============================================================

st.subheader("🎛️ Filters")

c1, c2, c3 = st.columns(3)


with c1:

    genres = st.multiselect(
        "Genre",
        sorted(df["Genre"].unique())
    )


with c2:

    studios = st.multiselect(
        "Studio",
        sorted(df["Studio"].unique())
    )


with c3:

    ratings = st.multiselect(
        "Rating",
        sorted(df["Rating"].unique())
    )


if genres:

    data = data[
        data["Genre"].isin(genres)
    ]


if studios:

    data = data[
        data["Studio"].isin(studios)
    ]


if ratings:

    data = data[
        data["Rating"].isin(ratings)
    ]


# ============================================================
# NUMERICAL FILTERS
# ============================================================

c1, c2, c3 = st.columns(3)


with c1:

    score_range = st.slider(
        "⭐ Score",
        float(df["Score"].min()),
        float(df["Score"].max()),
        (
            float(df["Score"].min()),
            float(df["Score"].max())
        ),
        step=0.1
    )


with c2:

    episode_range = st.slider(
        "🎬 Episodes",
        int(df["Episodes"].min()),
        int(df["Episodes"].max()),
        (
            int(df["Episodes"].min()),
            int(df["Episodes"].max())
        )
    )


with c3:

    popularity_range = st.slider(
        "🔥 Popularity",
        int(df["Popularity"].min()),
        int(df["Popularity"].max()),
        (
            int(df["Popularity"].min()),
            int(df["Popularity"].max())
        )
    )


data = data[
    data["Score"].between(
        score_range[0],
        score_range[1]
    )
]


data = data[
    data["Episodes"].between(
        episode_range[0],
        episode_range[1]
    )
]


data = data[
    data["Popularity"].between(
        popularity_range[0],
        popularity_range[1]
    )
]


# ============================================================
# RESULTS
# ============================================================

st.divider()

st.subheader("📊 Selection Summary")


if data.empty:

    st.warning(
        "No records match your current filters."
    )

    st.stop()


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Records",
        f"{len(data):,}"
    )


with c2:

    st.metric(
        "Average Score",
        f"{data['Score'].mean():.2f}"
    )


with c3:

    st.metric(
        "Average Episodes",
        f"{data['Episodes'].mean():.1f}"
    )


with c4:

    st.metric(
        "Studios",
        data["Studio"].nunique()
    )


# ============================================================
# DATA TABLE
# ============================================================

st.subheader("Dataset Results")

st.dataframe(
    data,
    use_container_width=True,
    height=500,
    hide_index=True
)


# ============================================================
# DOWNLOAD
# ============================================================

st.subheader("Export")

csv = data.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    "⬇️ Download Filtered Dataset",
    csv,
    "anime_filtered.csv",
    "text/csv",
    use_container_width=True
)


st.divider()

st.caption(
    "Anime Analytics • Data Explorer"
)