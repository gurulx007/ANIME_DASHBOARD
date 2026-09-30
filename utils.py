import streamlit as st
import pandas as pd


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("anime_dataset.csv")

    # Replace unknown values
    for column in ["Anime_Name", "Genre", "Studio"]:
        df[column] = df[column].replace("?", "Unknown")

    return df


# ============================================================
# FILTER DATA
# ============================================================

def filter_data(
    df,
    genres,
    studios,
    ratings,
    anime_names
):

    filtered = df[
        df["Genre"].isin(genres)
        &
        df["Studio"].isin(studios)
        &
        df["Rating"].isin(ratings)
        &
        df["Anime_Name"].isin(anime_names)
    ].copy()

    return filtered


# ============================================================
# PROFESSIONAL PLOTLY THEME
# ============================================================

def style_chart(fig, height=450):

    fig.update_layout(

        template="plotly_dark",

        height=height,

        paper_bgcolor="#0f141d",

        plot_bgcolor="#0f141d",

        font=dict(
            family="Arial",
            color="#e5e7eb",
            size=12
        ),

        margin=dict(
            l=45,
            r=30,
            t=70,
            b=45
        ),

        title=dict(
            font=dict(
                family="Arial",
                size=19,
                color="#f8fafc"
            ),
            x=0.02,
            xanchor="left"
        ),

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(
                color="#b8c0cc"
            )
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)",
            zeroline=False,
            linecolor="rgba(255,255,255,0.08)",
            tickfont=dict(
                color="#b8c0cc"
            )
        ),

        hoverlabel=dict(
            bgcolor="#171d29",
            bordercolor="#6366f1",
            font=dict(
                color="#ffffff",
                size=13
            )
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#d7dce5"
            )
        )
    )

    return fig


# ============================================================
# GLOBAL PROFESSIONAL UI
# ============================================================

def apply_page_style():

    st.markdown(
        """
        <style>

        /* ==================================================
           GLOBAL BACKGROUND
        ================================================== */

        .stApp {

            background:
                radial-gradient(
                    circle at 8% 0%,
                    rgba(99,102,241,0.13),
                    transparent 28%
                ),

                radial-gradient(
                    circle at 92% 0%,
                    rgba(168,85,247,0.10),
                    transparent 30%
                ),

                #080b12;
        }


        /* ==================================================
           MAIN CONTENT
        ================================================== */

        .main .block-container {

            max-width: 1500px;

            padding-top: 2rem;

            padding-bottom: 4rem;
        }


        /* ==================================================
           HEADINGS
        ================================================== */

        h1 {

            font-size: 44px !important;

            font-weight: 800 !important;

            letter-spacing: -1.5px !important;

            color: #f8fafc !important;

            line-height: 1.1 !important;
        }


        h2 {

            font-size: 28px !important;

            font-weight: 750 !important;

            color: #f8fafc !important;
        }


        h3 {

            color: #e5e7eb !important;

            font-weight: 700 !important;
        }


        /* ==================================================
           SIDEBAR
        ================================================== */

        section[data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #0b0f17 0%,
                    #080b12 100%
                );

            border-right:
                1px solid rgba(255,255,255,0.07);
        }


        section[data-testid="stSidebar"] h1 {

            font-size: 25px !important;

            color: #f8fafc !important;
        }


        section[data-testid="stSidebar"] hr {

            border-color:
                rgba(255,255,255,0.08) !important;
        }


        /* ==================================================
           METRIC CARDS
        ================================================== */

        div[data-testid="stMetric"] {

            background:
                linear-gradient(
                    145deg,
                    #151b27,
                    #0f141e
                );

            border:
                1px solid rgba(255,255,255,0.07);

            border-radius: 18px;

            padding: 20px 22px;

            min-height: 115px;

            box-shadow:
                0 12px 35px rgba(0,0,0,0.24);

            transition:
                transform 0.2s ease,
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }


        div[data-testid="stMetric"]:hover {

            transform: translateY(-3px);

            border-color:
                rgba(129,140,248,0.45);

            box-shadow:
                0 18px 40px rgba(0,0,0,0.32);
        }


        div[data-testid="stMetricLabel"] {

            color: #9ca6b5 !important;

            font-size: 13px !important;

            font-weight: 650 !important;
        }


        div[data-testid="stMetricValue"] {

            color: #f8fafc !important;

            font-size: 30px !important;

            font-weight: 750 !important;
        }


        /* ==================================================
           ANALYTICS BADGE
        ================================================== */

        .section-badge {

            display: inline-block;

            padding: 7px 13px;

            border-radius: 999px;

            background:
                rgba(99,102,241,0.12);

            border:
                1px solid rgba(129,140,248,0.30);

            color: #c4b5fd;

            font-size: 11px;

            font-weight: 750;

            letter-spacing: 0.8px;

            margin-bottom: 12px;

            text-transform: uppercase;
        }


        /* ==================================================
           GLASS ANALYTICS CARD
        ================================================== */

        .analytics-card {

            background:
                linear-gradient(
                    145deg,
                    rgba(20,27,39,0.96),
                    rgba(12,17,26,0.96)
                );

            border:
                1px solid rgba(255,255,255,0.07);

            border-radius: 18px;

            padding: 20px;

            box-shadow:
                0 15px 40px rgba(0,0,0,0.20);
        }


        /* ==================================================
           SELECT BOX
        ================================================== */

        div[data-baseweb="select"] > div {

            background: #111722 !important;

            border:
                1px solid rgba(255,255,255,0.08) !important;

            border-radius: 10px !important;
        }


        /* ==================================================
           MULTISELECT
        ================================================== */

        div[data-baseweb="select"] span {

            color: #f8fafc !important;
        }


        /* ==================================================
           BUTTONS
        ================================================== */

        .stButton button,
        .stDownloadButton button {

            border-radius: 10px !important;

            border:
                1px solid rgba(129,140,248,0.28) !important;

            background:
                linear-gradient(
                    145deg,
                    #151a25,
                    #10151e
                ) !important;

            color: #e5e7eb !important;

            font-weight: 600 !important;

            transition: all 0.2s ease;
        }


        .stButton button:hover,
        .stDownloadButton button:hover {

            border-color:
                rgba(129,140,248,0.75) !important;

            transform: translateY(-1px);

            box-shadow:
                0 8px 25px rgba(99,102,241,0.12);
        }


        /* ==================================================
           DATAFRAME
        ================================================== */

        div[data-testid="stDataFrame"] {

            border-radius: 14px;

            overflow: hidden;

            border:
                1px solid rgba(255,255,255,0.07);

            box-shadow:
                0 12px 30px rgba(0,0,0,0.18);
        }


        /* ==================================================
           TABS
        ================================================== */

        button[data-baseweb="tab"] {

            color: #8f99aa !important;

            font-weight: 600 !important;
        }


        button[data-baseweb="tab"][aria-selected="true"] {

            color: #c4b5fd !important;
        }


        /* ==================================================
           DIVIDERS
        ================================================== */

        hr {

            border-color:
                rgba(255,255,255,0.07) !important;
        }


        /* ==================================================
           SCROLLBAR
        ================================================== */

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
        """,
        unsafe_allow_html=True
    )