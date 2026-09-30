import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score
)

from utils import (
    load_data,
    apply_page_style,
    style_chart
)


# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="Machine Learning | Anime Analytics",
    page_icon="🤖",
    layout="wide"
)

apply_page_style()

df = load_data()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="section-badge">MACHINE LEARNING</div>',
    unsafe_allow_html=True
)

st.title("Logistic Regression")

st.caption(
    "Classification model for identifying higher-scoring anime records."
)

st.divider()


# ============================================================
# TARGET
# ============================================================

threshold = df["Score"].median()

df["High_Score"] = (
    df["Score"] >= threshold
).astype(int)


st.info(
    f"""
    **Classification Target**

    The dataset contains `Score` as a continuous variable.

    For this project, we create a binary target:

    **0 → Score below {threshold:.2f}**

    **1 → Score at or above {threshold:.2f}**

    The median threshold is a project-design choice.
    """
)


# ============================================================
# FEATURES
# ============================================================

features = [
    "Anime_Name",
    "Genre",
    "Studio",
    "Episodes",
    "Rating",
    "Popularity"
]

X = df[features]

y = df["High_Score"]


categorical_features = [
    "Anime_Name",
    "Genre",
    "Studio",
    "Rating"
]

numeric_features = [
    "Episodes",
    "Popularity"
]


# ============================================================
# PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features
        ),

        (
            "numeric",

            StandardScaler(),

            numeric_features
        )
    ]
)


# ============================================================
# MODEL
# ============================================================

model = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "classifier",

            LogisticRegression(
                max_iter=2000
            )
        )
    ]
)


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y
)


# ============================================================
# TRAIN
# ============================================================

model.fit(
    X_train,
    y_train
)


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

auc = roc_auc_score(
    y_test,
    y_probability
)


# ============================================================
# PERFORMANCE
# ============================================================

st.header("Model Performance")

c1, c2, c3, c4, c5 = st.columns(5)


with c1:
    st.metric(
        "Accuracy",
        f"{accuracy:.1%}"
    )


with c2:
    st.metric(
        "Precision",
        f"{precision:.1%}"
    )


with c3:
    st.metric(
        "Recall",
        f"{recall:.1%}"
    )


with c4:
    st.metric(
        "F1 Score",
        f"{f1:.1%}"
    )


with c5:
    st.metric(
        "ROC AUC",
        f"{auc:.2f}"
    )


# ============================================================
# CONFUSION MATRIX
# ============================================================

st.header("Confusion Matrix")


cm = confusion_matrix(
    y_test,
    y_pred
)


fig = px.imshow(
    cm,
    text_auto=True,
    x=[
        "Predicted Low",
        "Predicted High"
    ],
    y=[
        "Actual Low",
        "Actual High"
    ],
    color_continuous_scale=[
        "#111827",
        "#4f46e5",
        "#c4b5fd"
    ],
    title="Classification Results"
)


st.plotly_chart(
    style_chart(fig, 450),
    use_container_width=True
)


# ============================================================
# COEFFICIENTS
# ============================================================

st.header("Feature Influence")

processor = model.named_steps[
    "preprocessor"
]

classifier = model.named_steps[
    "classifier"
]

feature_names = (
    processor
    .get_feature_names_out()
)

coefficients = classifier.coef_[0]


coef_df = pd.DataFrame({

    "Feature": feature_names,

    "Coefficient": coefficients
})


coef_df["Absolute Effect"] = (
    coef_df["Coefficient"]
    .abs()
)


coef_df = (
    coef_df
    .sort_values(
        "Absolute Effect",
        ascending=False
    )
    .head(20)
)


fig = px.bar(
    coef_df.sort_values(
        "Coefficient"
    ),
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="Most Influential Features"
)


st.plotly_chart(
    style_chart(fig, 600),
    use_container_width=True
)


# ============================================================
# LIVE PREDICTION
# ============================================================

st.header("🎯 Prediction Simulator")

st.caption(
    "Enter an anime profile and classify its score category."
)


c1, c2 = st.columns(2)


with c1:

    anime = st.selectbox(
        "Anime",
        sorted(
            df["Anime_Name"].unique()
        )
    )

    genre = st.selectbox(
        "Genre",
        sorted(
            df["Genre"].unique()
        )
    )

    studio = st.selectbox(
        "Studio",
        sorted(
            df["Studio"].unique()
        )
    )


with c2:

    rating = st.selectbox(
        "Rating",
        sorted(
            df["Rating"].unique()
        )
    )

    episodes = st.number_input(
        "Episodes",
        min_value=1,
        max_value=2000,
        value=500
    )

    popularity = st.number_input(
        "Popularity",
        min_value=0,
        max_value=2000000,
        value=500000
    )


if st.button(
    "🚀 Run Prediction",
    use_container_width=True
):

    input_data = pd.DataFrame({

        "Anime_Name": [anime],

        "Genre": [genre],

        "Studio": [studio],

        "Episodes": [episodes],

        "Rating": [rating],

        "Popularity": [popularity]
    })


    prediction = model.predict(
        input_data
    )[0]


    probability = model.predict_proba(
        input_data
    )[0][1]


    if prediction == 1:

        st.success(
            f"Predicted category: **HIGH SCORE**\n\n"
            f"Probability: **{probability:.1%}**"
        )

    else:

        st.warning(
            f"Predicted category: **LOWER SCORE**\n\n"
            f"High-score probability: **{probability:.1%}**"
        )


st.divider()

st.caption(
    "Anime Analytics • Machine Learning Module"
)