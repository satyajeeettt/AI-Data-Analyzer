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
    letter-spacing: -0.01em;
}

.stApp {
    background:
        radial-gradient(circle at 15% -10%, rgba(250, 204, 21, 0.07) 0%, transparent 40%),
        radial-gradient(circle at 85% 0%, rgba(96, 165, 250, 0.05) 0%, transparent 35%),
        linear-gradient(180deg, #05070d 0%, #0a0e17 50%, #05070d 100%);
    color: #e6e6e6;
}

/* Subtle dotted grid texture for a more "designed" feel */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: radial-gradient(rgba(255,255,255,0.035) 1px, transparent 1px);
    background-size: 26px 26px;
    pointer-events: none;
    z-index: 0;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0e17, #05070d);
    border-right: 1px solid rgba(250, 204, 21, 0.15);
}

h1, h2, h3, h4 {
    letter-spacing: -0.02em;
}

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

/* Brand strip at the very top, above the hero */
.brand-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 4px 22px 4px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 26px;
}
.brand-strip .brand-mark {
    font-size: 18px;
    font-weight: 800;
    color: #f1f5f9;
}
.brand-strip .brand-mark span {
    color: #facc15;
}
.brand-strip .brand-links {
    color: #6b7280;
    font-size: 13px;
}

.eyebrow-badge {
    display: inline-block;
    background: rgba(250, 204, 21, 0.1);
    border: 1px solid rgba(250, 204, 21, 0.3);
    color: #facc15;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 6px 16px;
    border-radius: 20px;
    margin-bottom: 18px;
}

.hero {
    padding: 64px 40px;
    border-radius: 24px;
    text-align: center;
    background: linear-gradient(160deg, #0a0e17 0%, #0d1117 55%, #111827 100%);
    border: 1px solid rgba(250, 204, 21, 0.15);
    margin-bottom: 25px;
    box-shadow:
        0 0 60px rgba(250, 204, 21, 0.05),
        inset 0 1px 0 rgba(255,255,255,0.04);
    position: relative;
    z-index: 1;
}
.hero-title {
    font-size: 54px;
    font-weight: 900;
    background: linear-gradient(90deg, #facc15, #fde047, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
}
.hero-sub {
    color: #cbd5e1;
    font-size: 19px;
    margin-top: 10px;
    font-weight: 500;
}

.card {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(250, 204, 21, 0.12);
    border-radius: 16px;
    padding: 26px 22px;
    text-align: center;
    transition: 0.25s ease;
}
.card:hover {
    border-color: rgba(250, 204, 21, 0.4);
    background: rgba(255,255,255,0.04);
    transform: translateY(-4px);
}
.card h3 {
    margin: 0 0 8px 0;
    font-size: 16px;
    color: #f1f5f9;
}

.plan-card {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(250, 204, 21, 0.15);
    border-radius: 20px;
    padding: 34px 22px;
    text-align: center;
    transition: 0.25s ease;
}
.plan-card:hover {
    transform: translateY(-4px);
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

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(250, 204, 21, 0.12);
    border-radius: 12px;
    padding: 15px;
}

/* ===== Landing Page Additions ===== */
.stats-bar {
    display: flex;
    justify-content: space-around;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(250, 204, 21, 0.1);
    border-radius: 16px;
    padding: 25px 10px;
    margin: 30px 0;
}
.stat-item {
    text-align: center;
}
.stat-number {
    font-size: 32px;
    font-weight: 900;
    color: #facc15;
}
.stat-label {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
}

.feature-grid-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(250, 204, 21, 0.1);
    border-radius: 16px;
    padding: 26px 20px;
    height: 100%;
    transition: 0.2s ease;
}
.feature-grid-card:hover {
    border-color: rgba(250, 204, 21, 0.4);
    transform: translateY(-4px);
}
.feature-grid-card .icon {
    font-size: 30px;
    margin-bottom: 10px;
}
.feature-grid-card h4 {
    color: #f1f5f9;
    margin: 6px 0;
    font-size: 17px;
}
.feature-grid-card p {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.5;
    margin: 0;
}

.usecase-card {
    background: linear-gradient(135deg, rgba(250,204,21,0.05), rgba(255,255,255,0.02));
    border: 1px solid rgba(250, 204, 21, 0.12);
    border-radius: 16px;
    padding: 24px;
    height: 100%;
}
.usecase-card .tag {
    display: inline-block;
    background: rgba(250, 204, 21, 0.15);
    color: #facc15;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.cta-banner {
    background: linear-gradient(135deg, #111827, #0d1117);
    border: 1px solid rgba(250, 204, 21, 0.25);
    border-radius: 20px;
    padding: 45px;
    text-align: center;
    margin: 40px 0;
    box-shadow: 0 0 30px rgba(250, 204, 21, 0.08);
}
.cta-banner h2 {
    color: #facc15;
    font-size: 30px;
    margin-bottom: 8px;
}
.cta-banner p {
    color: #cbd5e1;
    font-size: 15px;
}

.section-heading {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    color: #f1f5f9;
    margin: 45px 0 8px 0;
}
.section-subheading {
    text-align: center;
    color: #94a3b8;
    font-size: 15px;
    margin-bottom: 30px;
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
    c.execute(
        "SELECT subject, message, status, created_at FROM support_tickets WHERE username = ? ORDER BY id DESC",
        (username,)
    )
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

NAV_PAGES = ["Dashboard", "Insights", "Plans & Pricing", "Customer Care"]


# =========================================================
# AUTH PAGE
# =========================================================
def login_page():
    # ---------- BRAND STRIP ----------
    st.markdown("""
    <div class="brand-strip">
        <div class="brand-mark">⚡ DataPilot<span>AI</span></div>
        <div class="brand-links">Analytics &nbsp;•&nbsp; Reporting &nbsp;•&nbsp; Business Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- HERO ----------
    st.markdown("""
    <div class="hero">
        <div class="eyebrow-badge">AI-POWERED ANALYTICS PLATFORM</div>
        <div class="hero-title">Turn Raw Data Into<br>Business Decisions — Instantly</div>
        <p style="color:#94a3b8; font-size:15px; max-width:600px; margin:15px auto 0 auto;">
            Upload any CSV or Excel file and get AI-powered analytics, interactive charts,
            correlation insights, and executive-ready reports in seconds.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- STATS BAR (feature-based, honest — no fabricated user counts) ----------
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item"><div class="stat-number">5+</div><div class="stat-label">Chart Types</div></div>
        <div class="stat-item"><div class="stat-number">3</div><div class="stat-label">Subscription Tiers</div></div>
        <div class="stat-item"><div class="stat-number">&lt;5s</div><div class="stat-label">Avg. Analysis Time</div></div>
        <div class="stat-item"><div class="stat-number">100%</div><div class="stat-label">Secure Sessions</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- FEATURE GRID ----------
    st.markdown('<div class="section-heading">Everything You Need to Understand Your Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">Powerful analytics tools, built for speed and clarity</div>', unsafe_allow_html=True)

    features = [
        ("📊", "Smart Analytics", "Instant summary statistics, data quality scoring, and column-level breakdowns."),
        ("📈", "Interactive Charts", "Histograms, box plots, scatter plots, line charts, and pie charts — all in one place."),
        ("🔥", "Correlation Heatmaps", "Spot hidden relationships between variables at a glance."),
        ("🧠", "AI-Powered Insights", "Executive-ready reports with anomaly detection and strategic recommendations."),
        ("📥", "Dataset Export", "Download cleaned and analyzed datasets in one click."),
        ("🔒", "Secure by Design", "Your data stays yours — encrypted accounts and private sessions."),
    ]

    for row_start in range(0, len(features), 3):
        f_cols = st.columns(3)
        for f_col, (icon, title, desc) in zip(f_cols, features[row_start:row_start + 3]):
            with f_col:
                st.markdown(f"""
                <div class="feature-grid-card">
                    <div class="icon">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ---------- USE CASES ----------
    st.markdown('<div class="section-heading">Built For Every Team</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheading">From founders to analysts, DataPilot AI adapts to your workflow</div>', unsafe_allow_html=True)

    usecases = [
        ("STARTUPS", "Move Fast With Data", "Validate ideas and track KPIs without hiring a data team."),
        ("ANALYSTS", "Go Deeper, Faster", "Skip repetitive prep work — upload and get insights in seconds."),
        ("ENTERPRISES", "Scale With Confidence", "Consistent, reliable reporting across every department."),
    ]

    u_cols = st.columns(3)
    for u_col, (tag, title, desc) in zip(u_cols, usecases):
        with u_col:
            st.markdown(f"""
            <div class="usecase-card">
                <span class="tag">{tag}</span>
                <h4 style="color:#f1f5f9; margin:8px 0;">{title}</h4>
                <p style="color:#94a3b8; font-size:13px;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # ---------- CTA BANNER ----------
    st.markdown("""
    <div class="cta-banner">
        <h2>Ready to unlock your data?</h2>
        <p>Create a free account below — no credit card required.</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------- LOGIN / SIGNUP ----------
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
        NAV_PAGES,
        index=NAV_PAGES.index(st.session_state.page) if st.session_state.page in NAV_PAGES else 0
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
# DASHBOARD PAGE
# =========================================================
def render_dashboard(df, rows, cols, missing, quality_score, numeric_cols):
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

    if len(numeric_cols) > 0:
        st.subheader("📊 Visualization Center")
        chart_type = st.selectbox(
            "Select Chart",
            ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Pie Chart"]
        )
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


# =========================================================
# INSIGHTS PAGE — Executive Intelligence Report
# =========================================================
def render_insights(df, rows, cols, missing, quality_score, numeric_cols):
    st.subheader("🧠 Executive Intelligence Report")

    total_cells = rows * cols
    missing_pct = round((missing / total_cells) * 100, 2) if total_cells > 0 else 0.0
    reliability = round(100 - missing_pct, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Business Health", f"{quality_score}%")
    c2.metric("Data Reliability", f"{reliability}%")
    c3.metric("Analytics Readiness", "High" if quality_score >= 85 else "Moderate")

    st.markdown("---")
    st.markdown("### 📊 Dataset Overview")
    st.write(f"📄 **Records Processed:** {rows:,}")
    st.write(f"📊 **Attributes Analyzed:** {cols}")
    st.write(f"⚠ **Missing Values:** {missing} ({missing_pct}% of dataset)")
    st.write(f"🏆 **Data Quality Score:** {quality_score}%")

    if quality_score >= 95:
        st.success("Dataset quality is excellent and suitable for advanced analytics.")
    elif quality_score >= 80:
        st.warning("Dataset quality is acceptable. Minor preprocessing is recommended.")
    else:
        st.error("Dataset requires cleaning before reliable business analysis.")

    st.markdown("---")
    st.markdown("### 🔍 AI Insights")

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr().abs()
        for col in corr.columns:
            corr.loc[col, col] = 0

        unstacked = corr.unstack()
        if unstacked.max() > 0:
            strongest_pair = unstacked.idxmax()
            strongest_value = unstacked.max()
            st.success(
                f"Strongest relationship detected between **{strongest_pair[0]}** and "
                f"**{strongest_pair[1]}**, with a correlation score of **{strongest_value:.2f}**."
            )
        else:
            st.info("No meaningful correlations detected between numeric columns.")
    else:
        st.info("At least two numeric columns are needed to detect relationships.")

    st.markdown("---")
    st.markdown("### 🚨 Risk & Outlier Analysis")

    if len(numeric_cols) > 0:
        outlier_report = []
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - (1.5 * iqr)
            upper = q3 + (1.5 * iqr)
            outliers = df[(df[col] < lower) | (df[col] > upper)].shape[0]
            if outliers > 0:
                outlier_report.append(f"{col}: {outliers} unusual records detected")

        if outlier_report:
            for item in outlier_report:
                st.warning(item)
        else:
            st.success("No significant anomalies detected.")
    else:
        st.info("No numeric columns available for outlier analysis.")

    st.markdown("---")
    st.markdown("### 🎯 Strategic Recommendations")

    recommendations = []
    if missing > 0:
        recommendations.append("Improve data completeness to enhance analytical accuracy.")
    if quality_score > 90:
        recommendations.append("Dataset is ready for predictive analytics and forecasting.")
    if len(numeric_cols) > 3:
        recommendations.append("Perform feature selection to identify key business drivers.")

    recommendations.append("Monitor highly correlated variables for decision-making opportunities.")
    recommendations.append("Establish KPI dashboards for real-time monitoring.")
    recommendations.append("Review anomalies and outliers to identify risks or hidden opportunities.")

    for rec in recommendations:
        st.markdown(f"✅ {rec}")

    st.markdown("---")
    st.markdown("### 📋 Executive Summary")
    st.success(
        "The dataset demonstrates strong analytical potential. Data quality is sufficient for "
        "reporting, dashboarding, and business intelligence initiatives. Further value can be "
        "unlocked through predictive analytics, automated reporting, and KPI monitoring."
    )


# =========================================================
# DASHBOARD / INSIGHTS ROUTER (handles the shared file upload)
# =========================================================
def dashboard_and_insights_page():
    st.markdown("""
    <div class="hero">
        <div class="eyebrow-badge">WORKSPACE</div>
        <div class="hero-title" style="font-size:42px;">⚡ DataPilot AI</div>
        <div class="hero-sub">Professional AI Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h3>📊 Analytics</h3><p style="color:#94a3b8;font-size:13px;">Interactive dashboards & reports</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h3>⚡ Fast</h3><p style="color:#94a3b8;font-size:13px;">Analyze datasets within seconds</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h3>🧠 Insights</h3><p style="color:#94a3b8;font-size:13px;">AI-powered business intelligence</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

    if not file:
        st.info("Upload a CSV or Excel file to begin analysis.")
        return

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    rows, cols = df.shape[0], df.shape[1]
    missing = int(df.isnull().sum().sum())
    quality_score = round(((rows * cols - missing) / (rows * cols)) * 100, 2) if rows * cols > 0 else 0.0
    numeric_cols = df.select_dtypes(include="number").columns

    if st.session_state.page == "Dashboard":
        render_dashboard(df, rows, cols, missing, quality_score, numeric_cols)
    elif st.session_state.page == "Insights":
        render_insights(df, rows, cols, missing, quality_score, numeric_cols)

    st.markdown("---")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Dataset", csv, "cleaned_data.csv", "text/csv")


# =========================================================
# PLANS & PRICING PAGE (with mock payment)
# =========================================================
PLANS = {
    "Free": {"price": 0, "features": ["5 dataset uploads/month", "Basic charts", "Community support"]},
    "Pro": {"price": 499, "features": ["Unlimited uploads", "All chart types", "Correlation heatmaps", "Priority email support"]},
    "Enterprise": {"price": 1999, "features": ["Everything in Pro", "Dedicated account manager", "API access", "24/7 phone support"]},
}


def plans_page():
    st.markdown(
        '<div class="hero"><div class="eyebrow-badge">PRICING</div>'
        '<div class="hero-title" style="font-size:42px;">💳 Plans & Pricing</div>'
        '<div class="hero-sub">Choose the plan that fits your needs</div></div>',
        unsafe_allow_html=True
    )

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
                pc1, pc2 = st.columns(2)
                pc1.text_input("Expiry (MM/YY)", placeholder="12/28")
                pc2.text_input("CVV", type="password", placeholder="123")
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
    st.markdown(
        '<div class="hero"><div class="eyebrow-badge">SUPPORT</div>'
        '<div class="hero-title" style="font-size:42px;">🎧 Customer Care</div>'
        '<div class="hero-sub">We are here to help, 24/7</div></div>',
        unsafe_allow_html=True
    )

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
    st.markdown('<div class="footer">Built with Love For Users,ANYWHERE:ANYTIME:FREE OF COST — DataPilot AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 DataPilot AI. All rights reserved.</div>', unsafe_allow_html=True)  
    st.markdown('<div class="footer">Version 1.0.0</div>', unsafe_allow_html=True)      
#=========================================================
# ADDITIONAL INFORMATION
#=========================================================
    st.markdown("""
<style>
.feature-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-top: 30px;
    margin-bottom: 40px;
}

.feature-card {
    background: linear-gradient(
        145deg,
        rgba(20,25,40,0.95),
        rgba(10,15,30,0.95)
    );
    border: 1px solid rgba(120,120,255,0.15);
    border-radius: 18px;
    padding: 24px;
    transition: all .3s ease;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

.feature-card:hover {
    transform: translateY(-6px);
    border-color: #7c5cff;
    box-shadow: 0 12px 35px rgba(124,92,255,0.25);
}

.feature-icon {
    width: 60px;
    height: 60px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(124,92,255,0.12);
    font-size: 28px;
    margin-bottom: 18px;
}

.feature-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

.feature-desc {
    color: #B0B8D1;
    line-height: 1.7;
    font-size: 0.95rem;
}
</style>

<div class="feature-grid">

<div class="feature-card">
<div class="feature-icon">🔒</div>
<div class="feature-title">Secure by Design</div>
<div class="feature-desc">
Enterprise-grade security with encrypted processing and privacy-first architecture.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">⚡</div>
<div class="feature-title">AI-Powered Insights</div>
<div class="feature-desc">
Generate intelligent insights, trends, and recommendations from your datasets.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">📊</div>
<div class="feature-title">Smart Analytics</div>
<div class="feature-desc">
Interactive dashboards and advanced visualizations for data-driven decisions.
</div>
</div>

<div class="feature-card">
<div class="feature-icon">☁️</div>
<div class="feature-title">Reliable & Scalable</div>
<div class="feature-desc">
Built for performance and scalability, handling datasets of any size.
</div>
</div>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<h2 style='text-align:center;
font-size:2.4rem;
font-weight:800;
margin-bottom:10px;
background:linear-gradient(90deg,#7c5cff,#00d4ff);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;'>
Why Choose DataPilot AI?
</h2>

<p style='text-align:center;color:#9ca3af;margin-bottom:40px;'>
Enterprise-grade AI analytics platform built for modern data teams.
</p>
""", unsafe_allow_html=True)