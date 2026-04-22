import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="ML Health Predictor", layout="wide")

# ------------------ HEADER ------------------
st.title("💓 Smart Health Prediction System")
st.markdown("Predict health status and analyze vitals interactively")

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

# ------------------ DATASET SECTION ------------------
st.subheader("📂 Dataset")

if st.toggle("Show Dataset Info"):
    st.dataframe(df.head())
    st.write("Shape:", df.shape)
    st.write("Columns:", list(df.columns))

# ------------------ SPLIT ------------------
X = df.drop("Status", axis=1)
y = df["Status"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("⚙️ Settings")

model_name = st.sidebar.selectbox(
    "Select Model",
    [
        "Logistic Regression",
        "Random Forest",
        "Gradient Boosting",
        "KNN",
        "Decision Tree",
        "Naive Bayes",
        "SVM"
    ]
)

# ------------------ MODEL FUNCTION ------------------
def get_model(name):
    if name == "Logistic Regression":
        return Pipeline([
            ('scaler', StandardScaler()),
            ('model', LogisticRegression(max_iter=5000))
        ])
    elif name == "Random Forest":
        return RandomForestClassifier(random_state=42)
    elif name == "Gradient Boosting":
        return GradientBoostingClassifier(random_state=42)
    elif name == "KNN":
        return Pipeline([
            ('scaler', StandardScaler()),
            ('model', KNeighborsClassifier())
        ])
    elif name == "Decision Tree":
        return DecisionTreeClassifier(random_state=42)
    elif name == "Naive Bayes":
        return GaussianNB()
    elif name == "SVM":
        return Pipeline([
            ('scaler', StandardScaler()),
            ('model', SVC(probability=True))
        ])

model = get_model(model_name)

# ------------------ SESSION STATE ------------------
if "model" not in st.session_state:
    st.session_state.model = None

# ------------------ TRAIN MODEL ------------------
if st.button("🚀 Train Model"):
    kfold = KFold(n_splits=10, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_train, y_train, cv=kfold)

    st.success(f"Model trained successfully | Accuracy: {scores.mean():.4f}")

    model.fit(X_train, y_train)
    st.session_state.model = model

# ------------------ INPUT FEATURES ------------------
st.subheader("🎛️ Input Features")

input_data = []
cols = st.columns(3)

for i, col in enumerate(X.columns):
    with cols[i % 3]:
        val = st.slider(
            col,
            float(X[col].min()),
            float(X[col].max()),
            float(X[col].mean())
        )
        input_data.append(val)

input_array = np.array(input_data).reshape(1, -1)

# ------------------ HEALTH FUNCTIONS ------------------
def health_temp(temp):
    if 36.5 <= temp <= 37.5:
        return 100
    elif 35 <= temp <= 39:
        return 70
    else:
        return 40

def health_oxygen(o2):
    if o2 >= 95:
        return 100
    elif o2 >= 90:
        return 70
    else:
        return 40

def health_heart(hr):
    if 60 <= hr <= 100:
        return 100
    elif 50 <= hr <= 120:
        return 70
    else:
        return 40

# ------------------ COLUMN FINDER ------------------
def find_column(possible_names):
    for col in X.columns:
        for name in possible_names:
            if name.lower() in col.lower():
                return col
    return None

# ------------------ PREDICT ------------------
if st.button("🔮 Predict"):
    if st.session_state.model is None:
        st.warning("⚠️ Please train the model first")
    else:
        prediction = st.session_state.model.predict(input_array)

        st.success(f"Prediction Result: {prediction[0]}")

        temp_col = find_column(["temp"])
        o2_col = find_column(["oxygen", "o2"])
        hr_col = find_column(["heart", "hr"])

        if temp_col and o2_col and hr_col:
            temp = input_array[0][list(X.columns).index(temp_col)]
            o2 = input_array[0][list(X.columns).index(o2_col)]
            hr = input_array[0][list(X.columns).index(hr_col)]

            temp_score = health_temp(temp)
            o2_score = health_oxygen(o2)
            hr_score = health_heart(hr)

            # Overall score
            overall_score = (temp_score + o2_score + hr_score) / 3

            # Status
            if overall_score >= 90:
                status = "🟢 Healthy"
            elif overall_score >= 70:
                status = "🟡 Mild Condition"
            else:
                status = "🔴 Risky"

            # Display status
            st.subheader("🧠 Overall Health Status")
            st.success(f"{status} ({overall_score:.1f}%)")

            # Individual metrics
            st.subheader("💡 Health Analysis")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🌡️ Temperature Health", f"{temp_score}%")

            with col2:
                st.metric("🫁 Oxygen Health", f"{o2_score}%")

            with col3:
                st.metric("❤️ Heart Rate Health", f"{hr_score}%")

        else:
            st.error("❌ Could not detect Temp / Oxygen / Heart columns")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown(
    "<center>Made with ❤️ | Smart Health ML System</center>",
    unsafe_allow_html=True
)