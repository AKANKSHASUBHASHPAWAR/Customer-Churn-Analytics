# 🏦 Customer Churn Prediction & Analytics Dashboard

An end-to-end Machine Learning and Data Analytics project that analyzes bank customer behavior, predicts potential customer churn, and presents business insights through an interactive Streamlit dashboard.

## 📌 Project Overview

Customer churn occurs when customers stop using a company's services. Retaining existing customers is important for businesses.

This project uses historical bank customer data to identify churn patterns, compare Machine Learning models, predict potential churn, and support customer-retention decisions.

## 🎯 Project Objectives

- Analyze customer behavior and churn patterns.
- Perform Exploratory Data Analysis (EDA).
- Build and evaluate multiple Machine Learning models.
- Identify important features associated with churn predictions.
- Generate customer-level churn predictions.
- Create an Excel business report.
- Develop an interactive analytics dashboard using Streamlit and Plotly.

## 🛠️ Technologies Used

| Category         | Tools                       |
| ---------------- | --------------------------- |
| Programming      | Python                      |
| Data Analysis    | Pandas, NumPy               |
| Visualization    | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn                |
| Application      | Streamlit                   |
| Model Storage    | Joblib                      |
| Excel Reporting  | OpenPyXL                    |

## 📂 Project Structure

```text
Customer_Churn_Analytics/
│
├── dataset/
│   └── Bank_Churn.csv
│
├── notebooks/
│   └── Customer_Churn_Analysis.ipynb
│
├── models/
│   ├── random_forest_churn_model.pkl
│   └── feature_columns.pkl
│
├── reports/
│   └── Customer_Churn_Business_Report.xlsx
│
├── app.py
├── README.md
└── requirements.txt
```

## 🔍 Exploratory Data Analysis

The original dataset contains 10,000 customer records and 13 columns.

Key findings:

- Overall customer churn rate: 20.37%.
- Germany had the highest churn rate at 32.44%.
- Female customers had a higher churn rate than male customers.
- Inactive members had a higher churn rate than active members.
- Customers who left had a higher average age than customers who stayed.

## 🤖 Machine Learning Models

Four classification models were trained and evaluated:

1. Logistic Regression
2. Balanced Logistic Regression
3. Decision Tree
4. Random Forest

### Model Performance

| Model                        | Accuracy | Precision | Recall | F1 Score |
| ---------------------------- | -------: | --------: | -----: | -------: |
| Logistic Regression          |   80.80% |    58.91% | 18.67% |   28.36% |
| Balanced Logistic Regression |   71.35% |    38.72% | 70.02% |   49.87% |
| Decision Tree                |   77.00% |    46.07% | 76.41% |   57.49% |
| Random Forest                |   83.35% |    58.33% | 63.64% |   60.87% |

Random Forest was selected as the primary model because it achieved the highest accuracy and F1 score among the tested models.

The Decision Tree achieved the highest recall.

## 📊 Feature Importance

The Random Forest model identified these top features:

1. Age — 31.59%
2. Number of Products — 20.22%
3. Balance — 12.02%
4. Estimated Salary — 8.39%
5. Credit Score — 8.27%

Feature importance represents the model's reliance on input features, not proof of causation.

## 📈 Business Analysis

The model was evaluated on 2,000 held-out test customers.

| Business Metric                      | Result |
| ------------------------------------ | -----: |
| Total Test Customers                 |  2,000 |
| Actual Churn Customers               |    407 |
| Predicted Churn Customers            |    444 |
| Correctly Identified Churn Customers |    259 |
| Predicted Churn Percentage           | 22.20% |

These results can help a bank prioritize customer-retention efforts.

## 🖥️ Interactive Streamlit Dashboard

The application includes four sections:

### 1. Executive Overview

- Customer KPI cards
- Actual and predicted churn distribution
- Actual vs predicted customer comparison
- Geography-based churn analysis

### 2. Customer Prediction

- Customer information input form
- Churn prediction
- Churn probability
- Risk categorization
- Retention suggestions

### 3. Model Insights

- Machine Learning model comparison
- Interactive feature-importance chart
- Confusion matrix visualization

### 4. Customer Explorer

- Customer-level prediction records
- Customer search
- Prediction filters
- CSV download functionality

## ⚙️ Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd Customer_Churn_Analytics
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
streamlit run app.py
```

## 📁 Generated Reports

The Excel business report contains three worksheets:

- Business Summary
- Model Comparison
- Test Predictions

## 💡 Business Value

This project demonstrates how data analysis and Machine Learning can help businesses:

- Understand customer churn patterns.
- Identify customers who may be at risk of leaving.
- Prioritize retention campaigns.
- Evaluate predictive model performance.
- Communicate insights through interactive dashboards.

## ⚠️ Disclaimer

This is an educational portfolio project using a public bank customer churn dataset. Predictions are estimates and should not be treated as guaranteed customer outcomes or production banking decisions.

## 👩‍💻 Author

## **Akanksha Pawar**

Aspiring Data Analyst | Python | SQL | Excel | Power BI | Machine Learning

GitHub: [https://github.com/AKANKSHASUBHASHPAWAR](https://github.com/AKANKSHASUBHASHPAWAR)
