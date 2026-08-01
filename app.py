import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder

st.set_page_config(page_title="Workforce Attrition & Bench Analytics", layout="wide")

# ---------- Load & prepare data (cached so it only runs once) ----------
@st.cache_data
def load_data():
    employee = pd.read_csv('data/employee_master.csv')
    bench = pd.read_csv('data/bench_allocation.csv')
    finance = pd.read_csv('data/finance_cost.csv')
    df = employee.merge(bench, on='employee_id').merge(finance, on='employee_id')
    return df

@st.cache_resource
def train_model(df):
    le_dept = LabelEncoder()
    le_perf = LabelEncoder()
    df = df.copy()
    df['department_enc'] = le_dept.fit_transform(df['department'])
    df['performance_enc'] = le_perf.fit_transform(df['performance_rating'])

    features = ['bench_days', 'tenure_years', 'salary', 'department_enc', 'performance_enc']
    X = df[features]
    y = df['attrition_flag']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    model = LogisticRegression(random_state=42, class_weight='balanced')
    model.fit(X_train_scaled, y_train)

    return model, scaler, le_dept, le_perf, features

df = load_data()
model, scaler, le_dept, le_perf, features = train_model(df)

# ---------- Header ----------
st.title("Workforce Attrition & Bench Utilization Analytics")
st.caption("Interactive companion to the full analysis — predicts attrition risk, quantifies rupee impact, and recommends action.")

tab1, tab2, tab3 = st.tabs(["Department Overview", "Live Risk Predictor", "Decision Layer"])

# ---------- Tab 1: Department Overview ----------
with tab1:
    st.subheader("Attrition & Bench Cost by Department")

    dept_summary = df.groupby('department').agg(
        total_employees=('employee_id', 'count'),
        attrition_rate_pct=('attrition_flag', lambda x: round(100 * x.mean(), 2)),
        avg_bench_days=('bench_days', lambda x: round(x.mean(), 1)),
        total_bench_cost=('bench_cost_incurred', 'sum')
    ).reset_index().sort_values('attrition_rate_pct', ascending=False)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Attrition Rate by Department**")
        st.bar_chart(dept_summary.set_index('department')['attrition_rate_pct'])
    with col2:
        st.markdown("**Total Bench Cost by Department**")
        st.bar_chart(dept_summary.set_index('department')['total_bench_cost'])

    st.markdown("**Full Summary Table**")
    st.dataframe(dept_summary, use_container_width=True)

# ---------- Tab 2: Live Risk Predictor ----------
with tab2:
    st.subheader("Predict Attrition Risk for a Hypothetical Employee")

    col1, col2, col3 = st.columns(3)
    with col1:
        dept_input = st.selectbox("Department", sorted(df['department'].unique()))
        perf_input = st.selectbox("Performance Rating", sorted(df['performance_rating'].unique()))
    with col2:
        bench_input = st.slider("Bench Days", 0, int(df['bench_days'].max()), 30)
        tenure_input = st.slider("Tenure (Years)", 0.0, float(df['tenure_years'].max()), 2.0)
    with col3:
        salary_input = st.number_input("Annual Salary (₹)", min_value=100000, max_value=5000000, value=800000, step=50000)

    if st.button("Predict Risk", type="primary"):
        dept_enc = le_dept.transform([dept_input])[0]
        perf_enc = le_perf.transform([perf_input])[0]

        input_row = pd.DataFrame([[bench_input, tenure_input, salary_input, dept_enc, perf_enc]], columns=features)
        input_scaled = scaler.transform(input_row)
        risk_prob = model.predict_proba(input_scaled)[0][1]

        replacement_cost = 0.75 * salary_input
        expected_loss = risk_prob * replacement_cost
        intervention_cost = {0: 50000, 1: 100000, 2: 150000}.get(perf_enc, 100000)
        roi = expected_loss / intervention_cost
        recommend = roi > 6

        st.metric("Predicted Attrition Risk", f"{risk_prob*100:.1f}%")
        c1, c2, c3 = st.columns(3)
        c1.metric("Expected Loss (₹)", f"{expected_loss:,.0f}")
        c2.metric("Intervention Cost (₹)", f"{intervention_cost:,.0f}")
        c3.metric("ROI", f"{roi:.1f}x")

        if recommend:
            st.success("Recommendation: Intervene — expected savings justify the retention cost.")
        else:
            st.info("Recommendation: Monitor — intervention not currently cost-justified.")

# ---------- Tab 3: Decision Layer ----------
with tab3:
    st.subheader("Ranked Decision Layer — Who to Prioritize")

    try:
        decision_table = pd.read_csv('data/decision_layer_output.csv')

        dept_filter = st.multiselect(
            "Filter by Department",
            sorted(decision_table['department'].unique()),
            default=sorted(decision_table['department'].unique())
        )
        filtered = decision_table[decision_table['department'].isin(dept_filter)].sort_values('roi', ascending=False)

        st.dataframe(filtered, use_container_width=True)
        st.caption(f"Showing {len(filtered)} of {len(decision_table)} employees. "
                   f"{filtered['recommend_intervention'].sum()} flagged for intervention.")
    except FileNotFoundError:
        st.warning("decision_layer_output.csv not found in data/ — run notebooks/03_decision_layer.ipynb first.")

st.divider()
st.caption("Built as part of a data analytics portfolio project. Full code and documentation: [GitHub repo](https://github.com/ANCHAL23-WEB/01-workforce-attrition-analytics)")