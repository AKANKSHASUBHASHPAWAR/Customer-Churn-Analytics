
import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Churn Intelligence | Analytics",
    page_icon="🏦",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "random_forest_churn_model.pkl"
)
FEATURE_PATH = os.path.join(
    BASE_DIR, "models", "feature_columns.pkl"
)
REPORT_PATH = os.path.join(
    BASE_DIR, "reports", "Customer_Churn_Business_Report.xlsx"
)

# =====================================================
# 2. CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}
[data-testid="stSidebar"] {
    background-color: #111c32;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    color: #f8fafc !important;
}
p, label {
    color: #cbd5e1;
}
div[data-testid="stMetric"] {
    background: #17243b;
    border: 1px solid #293c59;
    padding: 18px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] {
    color: #38bdf8;
}
.stButton > button {
    background: #0284c7;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}
.stButton > button:hover {
    background: #0369a1;
    color: white;
}
div[data-testid="stTabs"] button {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. LOAD MODEL AND REPORT DATA
# =====================================================

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURE_PATH)
    return model, features

@st.cache_data
def load_reports():
    summary = pd.read_excel(
        REPORT_PATH, sheet_name="Business Summary"
    )
    comparison = pd.read_excel(
        REPORT_PATH, sheet_name="Model Comparison"
    )
    predictions = pd.read_excel(
        REPORT_PATH, sheet_name="Test Predictions"
    )
    return summary, comparison, predictions

try:
    if not os.path.exists(MODEL_PATH):
        st.error("Random Forest model file not found.")
        st.stop()

    if not os.path.exists(FEATURE_PATH):
        st.error("Feature columns file not found.")
        st.stop()

    if not os.path.exists(REPORT_PATH):
        st.error("Business report file not found.")
        st.stop()

    model, feature_columns = load_model()
    summary, comparison, test_results = load_reports()

except Exception as e:
    st.error(f"Unable to load project files: {e}")
    st.stop()

# =====================================================
# 4. PREPARE DASHBOARD DATA
# =====================================================

total_customers = len(test_results)

actual_churn = int(test_results["Churn"].sum())

predicted_churn = int(
    test_results["Predicted_Churn"].sum()
)

actual_stay = total_customers - actual_churn
predicted_stay = total_customers - predicted_churn

actual_rate = actual_churn / total_customers * 100
predicted_rate = predicted_churn / total_customers * 100

correct_predictions = int(
    (test_results["Churn"] ==
     test_results["Predicted_Churn"]).sum()
)

accuracy = correct_predictions / total_customers * 100

# =====================================================
# 5. SIDEBAR
# =====================================================

st.sidebar.title("🏦 Churn Intelligence")
st.sidebar.caption("Customer Analytics Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Customer Prediction",
        "Model Insights",
        "Customer Explorer"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "Machine Learning: Random Forest\n\n"
    "Dataset: Bank Customer Churn\n\n"
    "Evaluation: 2,000 test customers"
)

# =====================================================
# 6. EXECUTIVE OVERVIEW
# =====================================================

if page == "Executive Overview":

    st.title("📊 Customer Churn Intelligence")
    st.caption(
        "Understand customer behavior, monitor churn "
        "and discover business opportunities."
    )

    st.divider()

    # KPI cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Customers", f"{total_customers:,}")
    c2.metric("Actual Churners", f"{actual_churn:,}")
    c3.metric("Predicted Churners", f"{predicted_churn:,}")
    c4.metric("Actual Churn Rate", f"{actual_rate:.2f}%")

    st.divider()

    # Actual and predicted churn distribution
    left, right = st.columns(2)

    with left:
        st.subheader("Actual Customer Distribution")

        actual_data = pd.DataFrame({
            "Status": ["Stayed", "Left"],
            "Customers": [actual_stay, actual_churn]
        })

        fig = px.pie(
            actual_data,
            names="Status",
            values="Customers",
            hole=0.55,
            title="Actual Churn Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Model Prediction Distribution")

        predicted_data = pd.DataFrame({
            "Status": ["Predicted Stay", "Predicted Churn"],
            "Customers": [predicted_stay, predicted_churn]
        })

        fig = px.pie(
            predicted_data,
            names="Status",
            values="Customers",
            hole=0.55,
            title="Predicted Churn Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Actual vs predicted
    st.subheader("Actual vs Predicted Customers")

    comparison_data = pd.DataFrame({
        "Customer Status": ["Stayed", "Left"],
        "Actual": [actual_stay, actual_churn],
        "Predicted": [predicted_stay, predicted_churn]
    })

    fig = px.bar(
        comparison_data,
        x="Customer Status",
        y=["Actual", "Predicted"],
        barmode="group",
        title="Actual vs Predicted Churn"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Geography analysis
    st.subheader("Churn by Geography")

    geo_data = (
        test_results.groupby("Geography")["Churn"]
        .agg(["sum", "count"])
        .reset_index()
    )

    geo_data["Churn Rate"] = (
        geo_data["sum"] / geo_data["count"] * 100
    )

    fig = px.bar(
        geo_data,
        x="Geography",
        y="Churn Rate",
        text_auto=".2f",
        title="Actual Churn Rate by Country"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120",
        yaxis_title="Churn Rate (%)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info(
        "Business insight: Use customer-level predictions "
        "to prioritize retention efforts. Dashboard metrics "
        "above describe the held-out test dataset."
    )

# =====================================================
# 7. CUSTOMER PREDICTION
# =====================================================

elif page == "Customer Prediction":

    st.title("🔮 Customer Churn Prediction")
    st.caption(
        "Enter customer information to estimate churn risk."
    )

    with st.form("prediction_form"):

        st.subheader("Customer Profile")

        c1, c2, c3 = st.columns(3)

        with c1:
            credit_score = st.number_input(
                "Credit Score", 300, 900, 650
            )

            geography = st.selectbox(
                "Geography",
                ["France", "Germany", "Spain"]
            )

            gender = st.selectbox(
                "Gender", ["Female", "Male"]
            )

            age = st.number_input(
                "Age", 18, 100, 35
            )

        with c2:
            tenure = st.number_input(
                "Tenure (Years)", 0, 10, 5
            )

            balance = st.number_input(
                "Account Balance",
                min_value=0.0,
                value=50000.0
            )

            products = st.selectbox(
                "Number of Products", [1, 2, 3, 4]
            )

        with c3:
            credit_card = st.selectbox(
                "Has Credit Card?", ["Yes", "No"]
            )

            active_member = st.selectbox(
                "Active Member?", ["Yes", "No"]
            )

            salary = st.number_input(
                "Estimated Salary",
                min_value=0.0,
                value=50000.0
            )

        submitted = st.form_submit_button(
            "🚀 Analyze Customer",
            use_container_width=True
        )

    if submitted:

        customer = pd.DataFrame([{
            "CreditScore": credit_score,
            "Geography": geography,
            "Gender": gender,
            "Age": age,
            "Tenure": tenure,
            "Balance": balance,
            "Num Of Products": products,
            "Has Credit Card": 1 if credit_card == "Yes" else 0,
            "Is Active Member": 1 if active_member == "Yes" else 0,
            "Estimated Salary": salary
        }])

        customer = pd.get_dummies(
            customer,
            columns=["Geography", "Gender"],
            drop_first=True,
            dtype=int
        )

        customer = customer.reindex(
            columns=feature_columns,
            fill_value=0
        )

        prediction = int(model.predict(customer)[0])
        probability = float(
            model.predict_proba(customer)[0][1]
        )

        st.divider()
        st.subheader("Prediction Results")

        r1, r2 = st.columns(2)

        with r1:
            if prediction == 1:
                st.error("⚠️ Customer is predicted to leave")
            else:
                st.success("✅ Customer is predicted to stay")

        with r2:
            st.metric(
                "Churn Probability",
                f"{probability * 100:.2f}%"
            )

        st.progress(probability)

        # Risk bands are descriptive business segments,
        # not separately trained model classes.
        if probability < 0.30:
            risk = "Low"
            recommendation = (
                "Continue regular customer engagement "
                "and monitor account activity."
            )
        elif probability < 0.60:
            risk = "Medium"
            recommendation = (
                "Review customer satisfaction and consider "
                "a personalized engagement campaign."
            )
        else:
            risk = "High"
            recommendation = (
                "Prioritize a retention review and investigate "
                "possible reasons for dissatisfaction."
            )

        st.subheader("Customer Risk Assessment")
        st.write(f"**Risk Category: {risk}**")
        st.info(recommendation)

        st.caption(
            "Risk bands are illustrative thresholds. "
            "Predicted class uses the model's own classification threshold."
        )

# =====================================================
# 8. MODEL INSIGHTS
# =====================================================

elif page == "Model Insights":

    st.title("🧠 Machine Learning Model Insights")

    st.caption(
        "Explore model performance and the features "
        "used by the Random Forest classifier."
    )

    # Model comparison
    st.subheader("Model Performance Comparison")

    metric_options = [
        "Accuracy", "Precision", "Recall", "F1 Score"
    ]

    selected_metric = st.selectbox(
        "Choose performance metric",
        metric_options
    )

    fig = px.bar(
        comparison,
        x="Model",
        y=selected_metric,
        color="Model",
        title=f"Model Comparison - {selected_metric}",
        text_auto=".3f"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120",
        showlegend=False,
        yaxis_range=[0, 1]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        comparison.style.format({
            "Accuracy": "{:.2%}",
            "Precision": "{:.2%}",
            "Recall": "{:.2%}",
            "F1 Score": "{:.2%}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Feature importance
    st.subheader("Random Forest Feature Importance")

    importance = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": model.feature_importances_
    }).sort_values(
        "Importance", ascending=True
    )

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Features Influencing Model Predictions"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Confusion matrix
    st.subheader("Random Forest Confusion Matrix")

    cm = pd.crosstab(
        test_results["Churn"],
        test_results["Predicted_Churn"]
    ).reindex(
        index=[0, 1],
        columns=[0, 1],
        fill_value=0
    )

    fig = px.imshow(
        cm.values,
        x=["Predicted Stay", "Predicted Churn"],
        y=["Actual Stay", "Actual Churn"],
        text_auto=True,
        color_continuous_scale="Blues",
        title="Confusion Matrix"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Feature importance indicates model reliance, "
        "not causation."
    )

# =====================================================
# 9. CUSTOMER EXPLORER
# =====================================================

elif page == "Customer Explorer":

    st.title("👥 Customer Explorer")

    st.caption(
        "Explore customer-level churn predictions "
        "from the held-out test dataset."
    )

    filter_option = st.selectbox(
        "Filter customers",
        [
            "All Customers",
            "Predicted Churn",
            "Predicted Stay",
            "Actual Churn"
        ]
    )

    search_id = st.text_input(
        "Search Customer ID"
    )

    filtered = test_results.copy()

    if filter_option == "Predicted Churn":
        filtered = filtered[
            filtered["Predicted_Churn"] == 1
        ]

    elif filter_option == "Predicted Stay":
        filtered = filtered[
            filtered["Predicted_Churn"] == 0
        ]

    elif filter_option == "Actual Churn":
        filtered = filtered[
            filtered["Churn"] == 1
        ]

    if search_id.strip():
        filtered = filtered[
            filtered["CustomerId"].astype(str).str.contains(
                search_id.strip(), na=False
            )
        ]

    display_data = filtered.copy()

    display_data["Churn_Probability"] = (
        display_data["Churn_Probability"] * 100
    ).round(2)

    st.metric(
        "Customers displayed",
        f"{len(display_data):,}"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    csv = display_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Customer Data",
        data=csv,
        file_name="customer_churn_predictions.csv",
        mime="text/csv"
    )

# =====================================================
# 10. FOOTER
# =====================================================

st.divider()

st.caption(
    "Customer Churn Intelligence Dashboard | "
    "Python | SQL | Machine Learning | Streamlit | Plotly"
)
