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
    page_title="DataPilot AI | Enterprise Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM UNIFIED ENTERPRISE GLASS-MORPHISM THEME CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background: 
        radial-gradient(circle at 10% 10%, rgba(99, 102, 241, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.12) 0%, transparent 40%),
        linear-gradient(180deg, #090d16 0%, #05070c 100%);
    color: #f1f5f9;
}

/* Glassmorphism Navigation Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(10, 15, 28, 0.8) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Professional Input Controls UI Fix */
div[data-baseweb="input"] {
    background-color: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
}

/* Premium Gradient Button Customizations */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
}

/* Top Branding Strip */
.brand-strip {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 30px;
    background: rgba(255, 255, 255, 0.01);
    border-radius: 12px;
}
.brand-strip .brand-mark {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #ffffff;
}
.brand-strip .brand-mark span {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.brand-strip .brand-links {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 500;
}

/* Hero Section */
.hero {
    padding: 60px 40px;
    border-radius: 24px;
    text-align: center;
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-bottom: 35px;
}
.hero-title {
    font-size: 48px;
    font-weight: 800;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #ffffff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Metric / Dashboard Premium Cards */
[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.6) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

/* Multi-column Custom Grid */
.corporate-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 20px;
    margin: 25px 0;
}
.corporate-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 24px;
    transition: all 0.3s ease;
}
.corporate-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99, 102, 241, 0.4);
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.1);
}
.corporate-card .icon {
    font-size: 28px;
    margin-bottom: 12px;
}
.corporate-card h4 {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    margin: 4px 0;
}
.corporate-card p {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.6;
    margin: 0;
}

.footer-section {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 80px;
    padding: 24px 0;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE OPERATIONS
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
        return True, "Account successfully registered."
    except sqlite3.IntegrityError:
        return False, "Username or Email identity already exists."
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
# SESSION STATE MANAGEMENT
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
# AUTH / ENTERPRISE LANDING PAGE
# =========================================================
def login_page():
    st.markdown("""
    <div class="brand-strip">
        <div class="brand-mark">⚡ DataPilot<span>AI</span></div>
        <div class="brand-links">Automated Analytics &nbsp;•&nbsp; Intelligence Panels</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-title">Automate Data Insights Engine</div>
        <p style="color:#94a3b8; font-size:16px; max-width:650px; margin:15px auto 0 auto;">
            Upload enterprise records instantly. Run advanced correlation algorithms, predictive breakdowns, 
            and generate production-ready summaries with zero manual mapping layers.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Clean Component Layout Over RAW Grid Strings
    st.markdown('<h3 style="text-align:center; margin-bottom: 25px;">Core Architecture Capabilities</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="corporate-grid">
        <div class="corporate-card">
            <div class="icon">📊</div>
            <h4>Smart Analytics</h4>
            <p>Instant matrix profiling, automated variance detection, and granular field structural scoring.</p>
        </div>
        <div class="corporate-card">
            <div class="icon">📈</div>
            <h4>Advanced Plotting</h4>
            <p>High-fidelity responsive Plotly dashboards rendering interactive dataset distribution spreads.</p>
        </div>
        <div class="corporate-card">
            <div class="icon">🧠</div>
            <h4>Statistical AI Reports</h4>
            <p>Automated anomaly extraction modules generating immediate operational risk reviews.</p>
        </div>
        <div class="corporate-card">
            <div class="icon">🔒</div>
            <h4>Protected Layers</h4>
            <p>Sessions run under private transaction threads ensuring persistent cloud database isolation.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.8, 1])
    with auth_col2:
        tab1, tab2 = st.tabs(["🔑 Access Dashboard", "📝 Register System Identity"])
        
        with tab1:
            with st.form("login_form"):
                user_input = st.text_input("Username / UID")
                pass_input = st.text_input("Security Key", type="password")
                submit_login = st.form_submit_button("Authenticate Session", use_container_width=True)

                if submit_login:
                    if not user_input or not pass_input:
                        st.error("Authentication parameters cannot be blank.")
                    else:
                        valid, assigned_plan = verify_user(user_input, pass_input)
                        if valid:
                            st.session_state.logged_in = True
                            st.session_state.username = user_input
                            st.session_state.plan = assigned_plan
                            st.session_state.page = "Dashboard"
                            st.success("Identity verified. Thread routing initiated...")
                            time.sleep(0.4)
                            st.rerun()
                        else:
                            st.error("Invalid workspace tokens or invalid authorization key.")

        with tab2:
            with st.form("signup_form"):
                reg_user = st.text_input("Configure Username")
                reg_email = st.text_input("Corporate Email Address")
                reg_pass = st.text_input("System Key Sequence", type="password")
                confirm_pass = st.text_input("Verify Key Sequence", type="password")
                submit_register = st.form_submit_button("Provision Environment Space", use_container_width=True)

                if submit_register:
                    if not reg_user or not reg_email or not reg_pass:
                        st.error("All workspace field descriptors are compulsory.")
                    elif reg_pass != confirm_pass:
                        st.error("Key strings mismatch. Verify sequence validation inputs.")
                    elif len(reg_pass) < 6:
                        st.error("Key sequences must match a minimal architecture threshold of 6 chars.")
                    else:
                        success, feedback = create_user(reg_user, reg_email, reg_pass)
                        if success:
                            st.success(f"{feedback} Proceed to the access tab.")
                        else:
                            st.error(feedback)

# =========================================================
# SYSTEM PANEL STRUCTURE
# =========================================================
def sidebar_nav():
    st.sidebar.markdown(f"""
    <div style='padding: 10px 0px;'>
        <h2 style='color:#ffffff; margin-bottom:5px;'>⚡ DataPilot <span style='color:#6366f1;'>AI</span></h2>
        <p style='color:#64748b; font-size:13px; margin:0;'>OPERATIONAL ENVIRONMENT</p>
    </div>
    <hr style='border-color: rgba(255,255,255,0.08); margin: 10px 0;'>
    <p style='font-size:14px; color:#cbd5e1;'>Operator: <b>{st.session_state.username}</b></p>
    <p style='font-size:14px; color:#cbd5e1;'>Access Tier: <span style='color:#06b6d4; font-weight:600;'>{st.session_state.plan}</span></p>
    """, unsafe_allow_html=True)

    nav = st.sidebar.radio(
        "📍 Platform Workspace Modules",
        NAV_PAGES,
        index=NAV_PAGES.index(st.session_state.page) if st.session_state.page in NAV_PAGES else 0
    )
    st.session_state.page = nav

    st.sidebar.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    st.sidebar.caption("System Diagnostics: Operational Cluster Normal")
    
    if st.sidebar.button("🚪 Relinquish Session Token", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.page = "Login"
        st.rerun()

# =========================================================
# CORE MODULE PANELS
# =========================================================
def render_dashboard(df, rows, cols, missing, quality_score, numeric_cols):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Processed Matrix Rows", f"{rows:,}")
    col2.metric("Configured Attributes", cols)
    col3.metric("Null Fields Extracted", missing)
    col4.metric("Dataset Quality Vector", f"{quality_score}%")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Primary Record Matrix Grid View")
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Descriptive Metric Summary Spread")
    try:
        st.dataframe(df.describe(), use_container_width=True)
    except Exception:
        st.info("No explicit numeric distributions isolated to perform mathematical operations.")

    if len(numeric_cols) > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📈 Dynamic Analytical Visualization Pipeline")
        
        vc1, vc2 = st.columns(2)
        with vc1:
            chart_type = st.selectbox("Render System Output Format", ["Histogram", "Box Distribution", "Scatter Configuration", "Sequential Line Chart", "Distribution Map Pie"])
        with vc2:
            selected_col = st.selectbox("Primary Evaluated Matrix Variable", numeric_cols)

        fig = None
        if chart_type == "Histogram":
            fig = px.histogram(df, x=selected_col)
        elif chart_type == "Box Distribution":
            fig = px.box(df, y=selected_col)
        elif chart_type == "Sequential Line Chart":
            fig = px.line(df, y=selected_col)
        elif chart_type == "Distribution Map Pie":
            pie_data = df[selected_col].value_counts().head(10).reset_index()
            pie_data.columns = [selected_col, "Occurrences"]
            fig = px.pie(pie_data, names=selected_col, values="Occurrences")
        elif chart_type == "Scatter Configuration":
            second_col = st.selectbox("Secondary Intersecting Metric Column", numeric_cols)
            fig = px.scatter(df, x=selected_col, y=second_col)

        if fig:
            fig.update_layout(
                template="plotly_dark", 
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)",
                colorway=["#6366f1", "#06b6d4", "#a855f7"]
            )
            st.plotly_chart(fig, use_container_width=True)

    if len(numeric_cols) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🔥 Covariance Matrix & Correlation Structural Maps")
        corr_matrix = df[numeric_cols].corr()
        heatmap = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="Purples")
        heatmap.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(heatmap, use_container_width=True)

def render_insights(df, rows, cols, missing, quality_score, numeric_cols):
    st.subheader("🧠 Automated Machine Intelligence & Diagnostics Summary")

    cells = rows * cols
    missing_pct = round((missing / cells) * 100, 2) if cells > 0 else 0.0
    reliability = round(100 - missing_pct, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Operational Profiling Score", f"{quality_score}%")
    c2.metric("Matrix Data Integrity Factor", f"{reliability}%")
    c3.metric("Deployment Readiness Level", "Production Safe" if quality_score >= 85 else "Caution Advised")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    
    ins_col1, ins_col2 = st.columns(2)
    with ins_col1:
        st.markdown("### 📊 Dataset Integrity Summary")
        st.write(f"• **System Records Processed:** {rows:,} lines")
        st.write(f"• **Isolated Headers Checked:** {cols} metrics")
        st.write(f"• **Null/Empty Value Nodes:** {missing} records ({missing_pct}%)")
        
        if quality_score >= 90:
            st.success("Analysis complete: Architecture indicates stable variance levels. Deployment recommended.")
        else:
            st.warning("Analysis complete: High missingness ratios discovered. Review collection layers before processing.")

    with ins_col2:
        st.markdown("### 🚨 Statistical Deviation & Extreme Metrics")
        if len(numeric_cols) > 0:
            anomalies = 0
            for col in numeric_cols:
                q1 = df[col].quantile(0.25)
                q3 = df[col].quantile(0.75)
                iqr = q3 - q1
                outliers = df[(df[col] < (q1 - 1.5 * iqr)) | (df[col] > (q3 + 1.5 * iqr))].shape[0]
                anomalies += outliers
            if anomalies > 0:
                st.error(f"Attention Required: Discovered {anomalies} out-of-bounds variations across operational columns.")
            else:
                st.success("Variance checks successful: Data contains normal deviation patterns across elements.")
        else:
            st.info("Vector evaluations require continuous distribution ranges.")

def dashboard_and_insights_page():
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.02); padding: 20px; border-radius:16px; border: 1px solid rgba(255,255,255,0.05); margin-bottom: 25px;'>
        <h2 style='margin:0; font-size:28px;'>⚡ Operations Dashboard Panel</h2>
        <p style='color:#94a3b8; margin:5px 0 0 0;'>Active Context Module: {st.session_state.page}</p>
    </div>
    """, unsafe_allow_html=True)

    file = st.file_uploader("Provide Matrix Source Records (Supports CSV, XLSX types)", type=["csv", "xlsx"])

    if not file:
        st.info("System awaiting dynamic dataset input sequence stream. Drop operational source records above.")
        return

    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

    rows, cols = df.shape[0], df.shape[1]
    missing = int(df.isnull().sum().sum())
    quality_score = round(((rows * cols - missing) / (rows * cols)) * 100, 2) if rows * cols > 0 else 0.0
    numeric_cols = df.select_dtypes(include="number").columns

    if st.session_state.page == "Dashboard":
        render_dashboard(df, rows, cols, missing, quality_score, numeric_cols)
    elif st.session_state.page == "Insights":
        render_insights(df, rows, cols, missing, quality_score, numeric_cols)

    st.markdown("<br><hr>", unsafe_allow_html=True)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Dispatch Cleaned Matrix Records", csv, "processed_matrix.csv", "text/csv")

# =========================================================
# MANAGEMENT BILLING SYSTEMS
# =========================================================
PLANS = {
    "Free Tier": {"price": 0, "features": ["5 source file pipelines monthly", "Standard chart outputs", "Self-service docs"]},
    "Pro Enterprise": {"price": 499, "features": ["Unlimited record imports", "All analytical visualizations", "Covariance engines", "Dedicated support queues"]},
    "Scale Tier": {"price": 1999, "features": ["All Enterprise configurations", "Cluster access allocations", "Full programmatic REST API", "Immediate priority nodes"]},
}

def plans_page():
    st.markdown("<h2 style='text-align:center;'>💳 Global Transaction Tiers & Cloud Subscriptions</h2><br>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, (p_name, p_data) in enumerate(PLANS.items()):
        with cols[idx]:
            is_active = st.session_state.plan == p_name or (st.session_state.plan == "Free" and p_name == "Free Tier")
            st.markdown(f"""
            <div class="corporate-card" style="text-align:center; {'border-color:#6366f1;' if is_active else ''}">
                <h3 style='color:#ffffff;margin:0;'>{p_name}</h3>
                <h1 style='color:#06b6d4; margin:15px 0;'>₹{p_data['price']}<span style='font-size:14px;color:#64748b;'>/mo</span></h1>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for f in p_data["features"]:
                st.write(f"✓ {f}")
            
            if is_active:
                st.button("Active Profile Identity", disabled=True, key=f"act_{p_name}", use_container_width=True)
            else:
                if st.button(f"Upgrade to {p_name}", key=f"up_{p_name}", use_container_width=True):
                    st.session_state.checkout_plan = p_name
                    st.rerun()

    if "checkout_plan" in st.session_state:
        target_plan = st.session_state.checkout_plan
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.subheader(f"Secure Vault Transaction Gateway — Account Destination: {target_plan}")
        
        if PLANS[target_plan]["price"] == 0:
            update_plan(st.session_state.username, target_plan)
            st.session_state.plan = target_plan
            st.success("Licensing status structural adjustments finalized successfully.")
            del st.session_state.checkout_plan
            time.sleep(0.5)
            st.rerun()
        else:
            with st.form("billing_form"):
                st.text_input("Account Owner Name")
                st.text_input("Identity Token String (Card Number)", placeholder="0000 0000 0000 0000")
                b_c1, b_c2 = st.columns(2)
                b_c1.text_input("Term Limit Validation (MM/YY)", placeholder="12/30")
                b_c2.text_input("Security Key Verification Vector (CVV)", type="password")
                execute_pay = st.form_submit_button("Authorize Platform Payment Sequence", use_container_width=True)

                if execute_pay:
                    with st.spinner("Authorizing vault payment clearance..."):
                        time.sleep(1.2)
                    update_plan(st.session_state.username, target_plan)
                    st.session_state.plan = target_plan
                    st.success(f"System Authorization Succeeded. Access profile elevated to {target_plan}.")
                    del st.session_state.checkout_plan
                    time.sleep(1)
                    st.rerun()

# =========================================================
# SUPPORT MODULE
# =========================================================
def customer_care_page():
    st.markdown("<h2 style='text-align:center;'>🎧 Corporate Operations Helpdesk</h2><br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.markdown('<div class="corporate-card" style="text-align:center;"><h4>📧 Communication Gateway</h4>ops@datapilot.ai</div>', unsafe_allow_html=True)
    c2.markdown('<div class="corporate-card" style="text-align:center;"><h4>📞 Instant Voice Routing</h4>+91-1800-123-456</div>', unsafe_allow_html=True)
    c3.markdown('<div class="corporate-card" style="text-align:center;"><h4>💬 Virtual Desk Routing</h4>Operational 24/7/365</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📝 Dispatch Engineering Support Ticket")

    with st.form("ticket_submission"):
        head = st.text_input("Issue Classification Header")
        body = st.text_area("Provide functional logs or behavior description")
        dispatch = st.form_submit_button("Transmit Ticket to Escalation Queue", use_container_width=True)
        if dispatch:
            if head and body:
                add_ticket(st.session_state.username, head, body)
                st.success("Ticket buffered down inside engineering task databases successfully.")
            else:
                st.error("Fields must be complete to evaluate routing priorities correctly.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Context Account Logs & Historical Submissions")
    records = get_tickets(st.session_state.username)
    if records:
        for t_head, t_body, t_stat, t_time in records:
            with st.expander(f"📌 {t_head} — State Check: [{t_stat}]"):
                st.write(t_body)
                st.caption(f"Buffered Timestamp: {t_time}")
    else:
        st.info("No reported functional operational blocks linked with this profile identity.")

# =========================================================
# SYSTEM DISPATCH MAIN APPLICATION ROUTER
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

    st.markdown(f"""
    <div class="footer-section">
        <p>© 2026 DataPilot AI. Enterprise Analytic Platform Systems. All Rights Reserved.</p>
        <p style="color:#475569; font-size:11px; margin-top:5px;">System Node Environment Matrix v1.0.0 • Deployment Framework: Streamlit Production</p>
    </div>
    """, unsafe_allow_html=True)