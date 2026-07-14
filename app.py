import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import hashlib
import time
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="DataPilot AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# THUNDER DARK THEME CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 0%, #0d1117 0%, #05070d 60%);
    color: #e6e6e6;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e17, #05070d);
    border-right: 1px solid rgba(250, 204, 21, 0.15);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #facc15, #f59e0b);
    color: #0a0a0a;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    transition: 0.2s ease;
    box-shadow: 0 0 15px rgba(250, 204, 21, 0.25);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 25px rgba(250, 204, 21, 0.5);
}

/* Hero */
.hero {
    padding: 70px 40px;
    border-radius: 22px;
    text-align: center;
    background: linear-gradient(135deg, #05070d, #0d1117 60%, #111827);
    border: 1px solid rgba(250, 204, 21, 0.15);
    margin-bottom: 25px;
    box-shadow: 0 0 40px rgba(250, 204, 21, 0.06);
}
.hero-title {
    font-size: 58px;
    font-weight: 900;
    background: linear-gradient(90deg, #facc15, #fde047, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #cbd5e1;
    font-size: 20px;
    margin-top: 8px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(250, 204, 21, 0.12);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: 0.2s ease;
}
.card:hover {
    border-color: rgba(250, 204, 21, 0.4);
    transform: translateY(-3px);
}

/* Plan card */
.plan-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(250, 204, 21, 0.15);
    border-radius: 18px;
    padding: 30px 20px;
    text-align: center;
}
.plan-price {
    font-size: 36px;
    font-weight: 900;
    color: #facc15;
    margin: 10px 0;
}
.plan-popular {
    border: 2px solid #facc15;
    box-shadow: 0 0 25px rgba(250, 204, 21, 0.25);
}
.badge {
    background: #facc15;
    color: #0a0a0a;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 60px;
    padding: 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
}

/* Metric tweak */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(250, 204, 21, 0.12);
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE SETUP
# =========================================================
DB_PATH = "datapilot.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'Free',
            created_at TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            subject TEXT,
            message TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password):
    conn = get_conn()
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, email, password_hash, plan, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, email, hash_password(password), "Free", datetime.now().isoformat())
        )
        conn.commit()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."
    finally:
        conn.close()

def verify_user(username, password):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT password_hash, plan FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        return True, row[1]
    return False, None

def update_plan(username, plan):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE users SET plan = ? WHERE username = ?", (plan, username))
    conn.commit()
    conn.close()

def add_ticket(username, subject, message):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO support_tickets (username, subject, message, status, created_at) VALUES (?, ?, ?, 'Open', ?)",
        (username, subject, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_tickets(username):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT subject, message, status, created_at FROM support_tickets WHERE username = ? ORDER BY id DESC", (username,))
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# =========================================================
# SESSION STATE
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "plan" not in st.session_state:
    st.session_state.plan = "Free"
if "page" not in st.session_state:
    st.session_state.page = "Login"

# =========================================================
# AUTH PAGES
# =========================================================
def login_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">⚡ DataPilot AI</div>
        <div class="hero-sub">Enterprise Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    ok, plan = verify_user(username, password)
                    if ok:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.plan = plan
                        st.session_state.page = "Dashboard"
                        st.success("Login successful!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

    with tab2:
        with st.form("signup_form"):
            new_username = st.text_input("Choose a Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Choose a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)

            if submitted:
                if not new_username or not new_email or not new_password:
                    st.error("Please fill in all fields.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    ok, msg = create_user(new_username, new_email, new_password)
                    if ok:
                        st.success(msg + " Please login now.")
                    else:
                        st.error(msg)

# =========================================================
# SIDEBAR (only after login)
# =========================================================
def sidebar_nav():
    st.sidebar.markdown(f"""
    # ⚡ DataPilot AI
    ### Welcome, **{st.session_state.username}**
    Current Plan: **{st.session_state.plan}**
    ---
    """)

    nav = st.sidebar.radio(
        "📍 Navigation",
        ["Dashboard", "Insights", "Plans & Pricing", "Customer Care"],
        index=["Dashboard", "Insights", "Plans & Pricing", "Customer Care"].index(
            st.session_state.page if st.session_state.page in
            ["Dashboard", "Insights", "Plans & Pricing", "Customer Care"] else "Dashboard"
        )
    )
    st.session_state.page = nav

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### ⚡ Features
    📊 Smart Analytics  
    📈 Interactive Charts  
    🔥 Correlation Heatmaps  
    🧠 AI-Powered Insights  
    📥 Dataset Export
    """)
    st.sidebar.markdown("---")
    st.sidebar.success("System Status: Online")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = "Login"
        st.rerun()

# =========================================================
# DASHBOARD / INSIGHTS PAGE
# =========================================================
def dashboard_and_insights_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">⚡ DataPilot AI</div>
        <div class="hero-sub">Professional AI Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h3>📊 Analytics</h3>Interactive dashboards & reports</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>⚡ Fast</h3>Analyze datasets within seconds</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>🧠 Insights</h3>AI-powered business intelligence</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        rows, cols = df.shape[0], df.shape[1]
        missing = int(df.isnull().sum().sum())
        quality_score = round(((rows * cols - missing) / (rows * cols)) * 100, 2) if rows * cols > 0 else 0.0

        if st.session_state.page == "Dashboard":
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📄 Rows", rows)
            col2.metric("📊 Columns", cols)
            col3.metric("⚠ Missing Values", missing)
            col4.metric("🏆 Data Quality", f"{quality_score}%")

            st.markdown("---")
            st.subheader("📋 Dataset Preview")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Summary Statistics")
            try:
                st.dataframe(df.describe(), use_container_width=True)
            except Exception:
                st.info("No numeric columns found.")

            numeric_cols = df.select_dtypes(include="number").columns

            if len(numeric_cols) > 0:
                st.subheader("📊 Visualization Center")
                chart_type = st.selectbox("Select Chart", ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Pie Chart"])
                selected_col = st.selectbox("Select Column", numeric_cols)

                fig = None
                if chart_type == "Histogram":
                    fig = px.histogram(df, x=selected_col)
                elif chart_type == "Box Plot":
                    fig = px.box(df, y=selected_col)
                elif chart_type == "Line Chart":
                    fig = px.line(df, y=selected_col)
                elif chart_type == "Pie Chart":
                    pie_data = df[selected_col].value_counts().head(10).reset_index()
                    pie_data.columns = [selected_col, "Count"]
                    fig = px.pie(pie_data, names=selected_col, values="Count")
                elif chart_type == "Scatter Plot":
                    second_col = st.selectbox("Second Column", numeric_cols)
                    fig = px.scatter(df, x=selected_col, y=second_col)

                if fig:
                    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)

            if len(numeric_cols) > 1:
                st.subheader("🔥 Correlation Heatmap")
                corr_matrix = df[numeric_cols].corr()
                heatmap = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="YlOrBr")
                heatmap.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(heatmap, use_container_width=True)

        elif st.session_state.page == "Insights":
            st.subheader("🤖 DataPilot Insights")
            st.success("Analysis Generated Successfully")
            st.write(f"Dataset contains **{rows} rows** and **{cols} columns**.")
            st.write(f"Total missing values detected: **{missing}**")
            st.write(f"Data quality score: **{quality_score}%**")

            if quality_score > 95:
                st.success("Excellent data quality.")
            elif quality_score > 80:
                st.warning("Good quality but cleaning recommended.")
            else:
                st.error("Significant data cleaning required.")

            st.markdown("### 💡 Recommendations")
            st.write("✅ Remove missing values before modeling.")
            st.write("✅ Focus on highly correlated features.")
            st.write("✅ Investigate outliers.")
            st.write("✅ Build dashboards for business monitoring.")

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Dataset", csv, "cleaned_data.csv", "text/csv")
    else:
        st.info("Upload a CSV or Excel file to begin analysis.")

# =========================================================
# PLANS & PRICING PAGE (with mock payment)
# =========================================================
PLANS = {
    "Free": {"price": 0, "features": ["5 dataset uploads/month", "Basic charts", "Community support"]},
    "Pro": {"price": 499, "features": ["Unlimited uploads", "All chart types", "Correlation heatmaps", "Priority email support"]},
    "Enterprise": {"price": 1999, "features": ["Everything in Pro", "Dedicated account manager", "API access", "24/7 phone support"]},
}

def plans_page():
    st.markdown('<div class="hero"><div class="hero-title">💳 Plans & Pricing</div><div class="hero-sub">Choose the plan that fits your needs</div></div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (plan_name, plan_data) in enumerate(PLANS.items()):
        with cols[i]:
            popular = "plan-popular" if plan_name == "Pro" else ""
            badge = '<span class="badge">MOST POPULAR</span><br><br>' if plan_name == "Pro" else "<br><br>"
            st.markdown(f"""
            <div class="plan-card {popular}">
                {badge}
                <h3>{plan_name}</h3>
                <div class="plan-price">₹{plan_data['price']}<span style="font-size:14px;color:#94a3b8;">/mo</span></div>
            </div>
            """, unsafe_allow_html=True)

            for feat in plan_data["features"]:
                st.write(f"✅ {feat}")

            if st.session_state.plan == plan_name:
                st.button("Current Plan", disabled=True, key=f"current_{plan_name}", use_container_width=True)
            else:
                if st.button(f"Select {plan_name}", key=f"select_{plan_name}", use_container_width=True):
                    st.session_state.checkout_plan = plan_name
                    st.rerun()

    if "checkout_plan" in st.session_state:
        st.markdown("---")
        chosen = st.session_state.checkout_plan
        st.subheader(f"💳 Checkout — {chosen} Plan (₹{PLANS[chosen]['price']}/mo)")

        if PLANS[chosen]["price"] == 0:
            update_plan(st.session_state.username, chosen)
            st.session_state.plan = chosen
            st.success(f"You're now on the {chosen} plan!")
            del st.session_state.checkout_plan
            time.sleep(1)
            st.rerun()
        else:
            with st.form("payment_form"):
                st.text_input("Cardholder Name")
                st.text_input("Card Number", placeholder="4242 4242 4242 4242")
                c1, c2 = st.columns(2)
                c1.text_input("Expiry (MM/YY)", placeholder="12/28")
                c2.text_input("CVV", type="password", placeholder="123")
                st.caption("🔒 This is a demo checkout. No real payment will be processed.")
                pay = st.form_submit_button("Pay Now", use_container_width=True)

                if pay:
                    with st.spinner("Processing payment..."):
                        time.sleep(1.5)
                    update_plan(st.session_state.username, chosen)
                    st.session_state.plan = chosen
                    st.success(f"✅ Payment successful! You're now on the {chosen} plan.")
                    del st.session_state.checkout_plan
                    time.sleep(1.5)
                    st.rerun()

# =========================================================
# CUSTOMER CARE PAGE
# =========================================================
def customer_care_page():
    st.markdown('<div class="hero"><div class="hero-title">🎧 Customer Care</div><div class="hero-sub">We are here to help, 24/7</div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="card"><h3>📧 Email</h3>support@datapilot.ai</div>', unsafe_allow_html=True)
    c2.markdown('<div class="card"><h3>📞 Phone</h3>+91-1800-123-456</div>', unsafe_allow_html=True)
    c3.markdown('<div class="card"><h3>💬 Live Chat</h3>Available 9am - 9pm IST</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📝 Raise a Support Ticket")

    with st.form("ticket_form"):
        subject = st.text_input("Subject")
        message = st.text_area("Describe your issue")
        submitted = st.form_submit_button("Submit Ticket", use_container_width=True)
        if submitted:
            if subject and message:
                add_ticket(st.session_state.username, subject, message)
                st.success("Ticket submitted! Our team will get back to you soon.")
            else:
                st.error("Please fill in both fields.")

    st.markdown("---")
    st.subheader("📋 Your Previous Tickets")
    tickets = get_tickets(st.session_state.username)
    if tickets:
        for subj, msg, status, created in tickets:
            with st.expander(f"{subj} — {status}"):
                st.write(msg)
                st.caption(f"Submitted: {created}")
    else:
        st.info("No tickets raised yet.")

# =========================================================
# MAIN ROUTER
# =========================================================
if not st.session_state.logged_in:
    login_page()
else:
    sidebar_nav()

    if st.session_state.page in ["Dashboard", "Insights"]:
        dashboard_and_insights_page()
    elif st.session_state.page == "Plans & Pricing":
        plans_page()
    elif st.session_state.page == "Customer Care":
        customer_care_page()

    st.markdown("---")
    st.markdown('<div class="footer">Built with ⚡ using Streamlit — DataPilot AI</div>', unsafe_allow_html=True)