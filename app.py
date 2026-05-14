import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ChurnGuard · Telecom Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root tokens ── */
:root {
    --bg-base:      #080d14;
    --bg-surface:   #0d1520;
    --bg-card:      #111c2d;
    --bg-card2:     #0f1a28;
    --border:       rgba(56,139,253,0.18);
    --border-glow:  rgba(56,139,253,0.45);
    --accent:       #38a6fa;
    --accent2:      #00f5c4;
    --accent3:      #f07aff;
    --danger:       #ff4d72;
    --warn:         #ffb830;
    --success:      #00e5a0;
    --text-primary: #e8f0fe;
    --text-muted:   #6b8299;
    --text-dim:     #3d5068;
    --font-display: 'Syne', sans-serif;
    --font-body:    'DM Sans', sans-serif;
    --radius:       14px;
    --radius-sm:    8px;
    --glow:         0 0 30px rgba(56,166,250,0.15);
    --glow-strong:  0 0 50px rgba(56,166,250,0.30);
}

/* ── Global resets ── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
}

.stApp { background: var(--bg-base); }

/* Remove default streamlit padding */
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 1400px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }

/* ── Typography ── */
h1, h2, h3 { font-family: var(--font-display) !important; }

/* ── Header hero ── */
.hero-wrap {
    background: linear-gradient(135deg, #0d1a2d 0%, #091320 50%, #06101b 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2.4rem 2.8rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--glow);
}
.hero-wrap::before {
    content:'';
    position:absolute; inset:0;
    background: radial-gradient(ellipse at 10% 50%, rgba(56,166,250,0.08) 0%, transparent 60%),
                radial-gradient(ellipse at 90% 20%, rgba(0,245,196,0.06) 0%, transparent 50%);
    pointer-events:none;
}
.hero-badge {
    display:inline-block;
    font-family:var(--font-display);
    font-size:0.68rem;
    font-weight:700;
    letter-spacing:0.18em;
    text-transform:uppercase;
    color:var(--accent);
    background:rgba(56,166,250,0.1);
    border:1px solid rgba(56,166,250,0.3);
    border-radius:40px;
    padding:0.28rem 0.85rem;
    margin-bottom:0.9rem;
}
.hero-title {
    font-family:var(--font-display);
    font-size:2.4rem;
    font-weight:800;
    color:var(--text-primary);
    line-height:1.1;
    margin:0;
    letter-spacing:-0.02em;
}
.hero-title span { color:var(--accent); }
.hero-sub {
    font-family:var(--font-body);
    font-size:0.95rem;
    color:var(--text-muted);
    margin-top:0.6rem;
    font-weight:300;
}
.hero-dots {
    display:flex; gap:0.5rem; margin-top:1.4rem;
}
.dot {
    width:7px; height:7px; border-radius:50%;
}
.dot-1 { background:var(--accent); box-shadow:0 0 8px var(--accent); }
.dot-2 { background:var(--accent2); box-shadow:0 0 8px var(--accent2); }
.dot-3 { background:var(--accent3); box-shadow:0 0 8px var(--accent3); }

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.25s;
}
.card:hover { border-color: var(--border-glow); box-shadow: var(--glow); }

.card-title {
    font-family:var(--font-display);
    font-size:0.72rem;
    font-weight:700;
    letter-spacing:0.14em;
    text-transform:uppercase;
    color:var(--text-muted);
    margin-bottom:1rem;
    display:flex; align-items:center; gap:0.5rem;
}
.card-title::before {
    content:''; display:inline-block;
    width:3px; height:14px;
    background:var(--accent);
    border-radius:2px;
}

/* ── Metric tiles ── */
.metric-tile {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-val {
    font-family:var(--font-display);
    font-size:2rem;
    font-weight:800;
    color:var(--accent);
    line-height:1;
}
.metric-label {
    font-size:0.78rem;
    color:var(--text-muted);
    margin-top:0.35rem;
    letter-spacing:0.04em;
}

/* ── Risk badges ── */
.risk-badge {
    display:inline-flex; align-items:center; gap:0.5rem;
    font-family:var(--font-display);
    font-size:0.85rem;
    font-weight:700;
    letter-spacing:0.05em;
    padding:0.5rem 1.1rem;
    border-radius:40px;
    width:100%;
    justify-content:center;
}
.risk-high {
    background:rgba(255,77,114,0.14);
    border:1px solid rgba(255,77,114,0.5);
    color:#ff4d72;
}
.risk-medium {
    background:rgba(255,184,48,0.12);
    border:1px solid rgba(255,184,48,0.5);
    color:#ffb830;
}
.risk-low {
    background:rgba(0,229,160,0.12);
    border:1px solid rgba(0,229,160,0.4);
    color:#00e5a0;
}
.pulse-dot {
    width:8px; height:8px; border-radius:50%;
    animation: pulse 1.6s infinite;
}
.pulse-high  { background:#ff4d72; }
.pulse-med   { background:#ffb830; }
.pulse-low   { background:#00e5a0; }
@keyframes pulse {
    0%,100%  { opacity:1; transform:scale(1); }
    50%       { opacity:0.5; transform:scale(0.7); }
}

/* ── Action alerts ── */
.action-box {
    border-radius:var(--radius-sm);
    padding:0.85rem 1.1rem;
    font-size:0.86rem;
    margin-top:0.5rem;
    display:flex; align-items:flex-start; gap:0.6rem;
}
.action-critical {
    background:rgba(255,77,114,0.08);
    border-left:3px solid #ff4d72;
    color:#ffb3c1;
}
.action-warning {
    background:rgba(255,184,48,0.08);
    border-left:3px solid #ffb830;
    color:#ffe0a0;
}
.action-ok {
    background:rgba(0,229,160,0.08);
    border-left:3px solid #00e5a0;
    color:#9dffd9;
}

/* ── Section divider ── */
.section-head {
    font-family:var(--font-display);
    font-size:1.15rem;
    font-weight:700;
    color:var(--text-primary);
    margin: 1.6rem 0 1rem;
    display:flex; align-items:center; gap:0.7rem;
}
.section-head::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(to right, var(--border), transparent);
}

/* ── Form labels ── */
label[data-testid="stWidgetLabel"] > div > p,
.stSelectbox label, .stSlider label,
.stNumberInput label {
    font-family: var(--font-body) !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}

/* ── Inputs ── */
.stSelectbox > div > div,
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #0d1826 !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}
.stSelectbox > div > div:hover,
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(56,166,250,0.15) !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1a6fd4 0%, #1254a8 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(26,111,212,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(26,111,212,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(0,229,160,0.1) !important;
    color: var(--accent2) !important;
    border: 1px solid rgba(0,229,160,0.4) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
}
.stDownloadButton > button:hover {
    background: rgba(0,229,160,0.18) !important;
}

/* ── Radio ── */
.stRadio > div { gap: 0.4rem; }
.stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.85rem !important;
    color: var(--text-muted) !important;
}

/* ── Sidebar model info ── */
.sidebar-model-card {
    background:rgba(56,166,250,0.06);
    border:1px solid rgba(56,166,250,0.2);
    border-radius:var(--radius-sm);
    padding:1rem 1.1rem;
    margin-bottom:1rem;
}
.sidebar-stat {
    display:flex; justify-content:space-between; align-items:center;
    padding:0.4rem 0;
    border-bottom:1px solid rgba(255,255,255,0.04);
}
.sidebar-stat:last-child { border-bottom:none; }
.sidebar-stat-key {
    font-size:0.78rem; color:var(--text-muted); font-weight:400;
}
.sidebar-stat-val {
    font-family:var(--font-display);
    font-size:0.85rem; color:var(--accent); font-weight:700;
}

/* ── Table ── */
.stDataFrame { border-radius:var(--radius) !important; overflow:hidden; }
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius:var(--radius) !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    background: var(--bg-card) !important;
    padding: 1rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background:var(--bg-card) !important;
    border-radius:var(--radius-sm) !important;
    font-family:var(--font-display) !important;
    font-weight:600 !important;
    color:var(--text-primary) !important;
    font-size:0.88rem !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:var(--bg-base); }
::-webkit-scrollbar-thumb { background:var(--border-glow); border-radius:3px; }

/* Hide streamlit branding */
#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD ARTIFACTS
# ─────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    try:
        model    = joblib.load('best_churn_model.pkl')
        scaler   = joblib.load('scaler.pkl')
        threshold= joblib.load('optimal_threshold.pkl')
        metadata = joblib.load('model_metadata.pkl')
        return model, scaler, threshold, metadata
    except FileNotFoundError:
        return None, None, None, None

model, scaler, threshold, metadata = load_artifacts()

@st.cache_resource
def get_feature_names():
    if model is not None and hasattr(model, 'feature_names_in_'):
        return list(model.feature_names_in_)
    return None

feature_names = get_feature_names()

# ─────────────────────────────────────────────
#  HELPER – ONE-HOT ENCODE
# ─────────────────────────────────────────────
def create_one_hot_features(df):
    cat_map = {
        'PaymentMethod': {
            'Electronic check':        'PaymentMethod_Electronic check',
            'Mailed check':            'PaymentMethod_Mailed check',
            'Bank transfer (automatic)':'PaymentMethod_Bank transfer (automatic)',
        },
        'OnlineSecurity':    {'No internet service':'OnlineSecurity_No internet service',  'Yes':'OnlineSecurity_Yes'},
        'OnlineBackup':      {'No internet service':'OnlineBackup_No internet service',    'Yes':'OnlineBackup_Yes'},
        'DeviceProtection':  {'No internet service':'DeviceProtection_No internet service','Yes':'DeviceProtection_Yes'},
        'TechSupport':       {'No internet service':'TechSupport_No internet service',     'Yes':'TechSupport_Yes'},
        'StreamingTV':       {'No internet service':'StreamingTV_No internet service',     'Yes':'StreamingTV_Yes'},
        'StreamingMovies':   {'No internet service':'StreamingMovies_No internet service', 'Yes':'StreamingMovies_Yes'},
    }
    for src_col, mapping in cat_map.items():
        for new_col in mapping.values():
            df[new_col] = 0
        if src_col in df.columns:
            val = df[src_col].iloc[0]
            if val in mapping:
                df[mapping[val]] = 1
    return df

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1.6rem;">
        <span style="font-size:1.4rem">🛡️</span>
        <div>
            <div style="font-family:var(--font-display);font-weight:800;font-size:1rem;color:var(--text-primary);">ChurnGuard</div>
            <div style="font-size:0.7rem;color:var(--text-muted);letter-spacing:0.08em;">TELECOM INTELLIGENCE</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model info
    st.markdown('<div class="card-title">Model Status</div>', unsafe_allow_html=True)

    status_color = "#00e5a0" if model else "#ff4d72"
    status_label = "Online" if model else "Offline"

    # Pre-format values so format specs don't appear inside ternary expressions
    m_name      = metadata["model_name"]         if metadata else "—"
    m_f1        = f'{metadata["f1_score"]:.4f}'  if metadata else "—"
    m_recall    = f'{metadata["recall"]:.4f}'    if metadata else "—"
    m_threshold = f'{metadata["threshold"]:.2f}' if metadata else "—"

    if metadata:
        meta_html = (
            f'<div class="sidebar-stat"><span class="sidebar-stat-key">Algorithm</span>'
            f'<span class="sidebar-stat-val">{m_name}</span></div>'
            f'<div class="sidebar-stat"><span class="sidebar-stat-key">F1 Score</span>'
            f'<span class="sidebar-stat-val">{m_f1}</span></div>'
            f'<div class="sidebar-stat"><span class="sidebar-stat-key">Recall</span>'
            f'<span class="sidebar-stat-val">{m_recall}</span></div>'
            f'<div class="sidebar-stat"><span class="sidebar-stat-key">Threshold</span>'
            f'<span class="sidebar-stat-val">{m_threshold}</span></div>'
        )
    else:
        meta_html = '<div style="color:var(--text-muted);font-size:0.8rem;">No model loaded</div>'

    st.markdown(f"""
    <div class="sidebar-model-card">
        <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;">
            <div style="width:8px;height:8px;border-radius:50%;background:{status_color};
                        box-shadow:0 0 8px {status_color};"></div>
            <span style="font-family:var(--font-display);font-size:0.85rem;
                         font-weight:700;color:{status_color};">Model {status_label}</span>
        </div>
        {meta_html}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card-title" style="margin-top:1.4rem;">Prediction Mode</div>', unsafe_allow_html=True)
    prediction_mode = st.radio(
        "", ["Single Customer", "Batch Upload"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="position:absolute;bottom:1.5rem;left:1.2rem;right:1.2rem;">
        <div style="font-size:0.7rem;color:var(--text-dim);text-align:center;letter-spacing:0.04em;">
            ChurnGuard v2.0 · Powered by ML
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-badge">🛡️ &nbsp;Churn Intelligence Platform</div>
    <h1 class="hero-title">Customer <span>Retention</span> Predictor</h1>
    <p class="hero-sub">ML-powered churn risk scoring · Actionable retention insights · Real-time predictions</p>
    <div class="hero-dots">
        <div class="dot dot-1"></div>
        <div class="dot dot-2"></div>
        <div class="dot dot-3"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SINGLE CUSTOMER MODE
# ─────────────────────────────────────────────
if prediction_mode == "Single Customer":

    # ── Demographics ──
    st.markdown('<div class="section-head">👤 &nbsp;Customer Profile</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card"><div class="card-title">Demographics</div>', unsafe_allow_html=True)
        gender         = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner        = st.selectbox("Partner", ["No", "Yes"])
        dependents     = st.selectbox("Dependents", ["No", "Yes"])
        tenure         = st.slider("Tenure (months)", 0, 72, 12)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-title">Services & Connectivity</div>', unsafe_allow_html=True)
        phone_service   = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines  = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
        internet_service= st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

        no_inet = internet_service == "No"
        opts_svc = ["No internet service"] if no_inet else ["No", "Yes"]

        online_security  = st.selectbox("Online Security",  opts_svc)
        online_backup    = st.selectbox("Online Backup",    opts_svc)
        device_protection= st.selectbox("Device Protection",opts_svc)
        tech_support     = st.selectbox("Tech Support",     opts_svc)
        streaming_tv     = st.selectbox("Streaming TV",     opts_svc)
        streaming_movies = st.selectbox("Streaming Movies", opts_svc)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><div class="card-title">Billing & Contract</div>', unsafe_allow_html=True)
        contract          = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
        paperless_billing = st.selectbox("Paperless Billing", ["No", "Yes"])
        payment_method    = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, max_value=150.0, value=70.0, step=0.5)
        total_charges   = st.number_input("Total Charges ($)",   min_value=0.0, max_value=10000.0, value=500.0, step=10.0)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Predict button ──
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    predict_btn = st.button("⚡  Run Churn Analysis", use_container_width=True, type="primary")

    if predict_btn:
        input_data = pd.DataFrame({
            'gender':          [1 if gender == "Male" else 0],
            'SeniorCitizen':   [1 if senior_citizen == "Yes" else 0],
            'Partner':         [1 if partner == "Yes" else 0],
            'Dependents':      [1 if dependents == "Yes" else 0],
            'tenure':          [tenure],
            'PhoneService':    [1 if phone_service == "Yes" else 0],
            'MultipleLines':   [1 if multiple_lines == "Yes" else 0],
            'InternetService': [2 if internet_service == "Fiber optic" else (1 if internet_service == "DSL" else 0)],
            'OnlineSecurity':  [online_security],
            'OnlineBackup':    [online_backup],
            'DeviceProtection':[device_protection],
            'TechSupport':     [tech_support],
            'StreamingTV':     [streaming_tv],
            'StreamingMovies': [streaming_movies],
            'Contract':        [0 if contract == "Month-to-month" else (1 if contract == "One year" else 2)],
            'PaperlessBilling':[1 if paperless_billing == "Yes" else 0],
            'PaymentMethod':   [payment_method],
            'MonthlyCharges':  [monthly_charges],
            'TotalCharges':    [total_charges],
        })

        input_encoded = create_one_hot_features(input_data)
        for col in ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport',
                    'StreamingTV','StreamingMovies','PaymentMethod']:
            if col in input_encoded.columns:
                input_encoded.drop(columns=[col], inplace=True)

        if feature_names:
            for col in feature_names:
                if col not in input_encoded.columns:
                    input_encoded[col] = 0
            input_encoded = input_encoded[feature_names]

        numeric_features = ['tenure','MonthlyCharges','TotalCharges','SeniorCitizen']
        input_scaled = input_encoded.copy()
        if scaler:
            input_scaled[numeric_features] = scaler.transform(input_encoded[numeric_features])

        if model:
            churn_prob = model.predict_proba(input_scaled)[:, 1][0]
            churn_pred = int(churn_prob >= (threshold or 0.5))
        else:
            # Demo fallback
            churn_prob = 0.72
            churn_pred = 1

        # ── Results ──
        st.markdown('<div class="section-head" style="margin-top:2rem;">📊 &nbsp;Analysis Results</div>', unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4)

        pct = churn_prob * 100
        if churn_prob > 0.6:
            risk_class = "risk-high"; risk_label = "High Risk"; pulse_cls = "pulse-high"
            action_class = "action-critical"
            action_icon  = "🚨"
            action_msg   = "Immediate retention intervention required. Consider a personalised discount, contract upgrade offer, or direct outreach within 24 hours."
        elif churn_prob > 0.3:
            risk_class = "risk-medium"; risk_label = "Medium Risk"; pulse_cls = "pulse-med"
            action_class = "action-warning"
            action_icon  = "⚠️"
            action_msg   = "Elevated churn signal detected. Schedule a proactive touchpoint and review service satisfaction within 7 days."
        else:
            risk_class = "risk-low"; risk_label = "Low Risk"; pulse_cls = "pulse-low"
            action_class = "action-ok"
            action_icon  = "✅"
            action_msg   = "Customer is stable. Standard engagement programme sufficient. Review again at next billing cycle."

        with r1:
            st.markdown(f"""
            <div class="metric-tile">
                <div class="metric-val">{pct:.1f}<span style="font-size:1rem;color:var(--text-muted);">%</span></div>
                <div class="metric-label">Churn Probability</div>
            </div>""", unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="metric-tile">
                <div class="metric-val" style="font-size:1.5rem;margin-top:0.2rem;">{risk_label}</div>
                <div class="metric-label">Risk Classification</div>
            </div>""", unsafe_allow_html=True)

        with r3:
            retention_score = round((1 - churn_prob) * 100, 1)
            st.markdown(f"""
            <div class="metric-tile">
                <div class="metric-val" style="color:var(--accent2);">{retention_score}<span style="font-size:1rem;color:var(--text-muted);">%</span></div>
                <div class="metric-label">Retention Score</div>
            </div>""", unsafe_allow_html=True)

        with r4:
            clv_est = round(monthly_charges * max(1, (72 - tenure)) * (1 - churn_prob * 0.5))
            st.markdown(f"""
            <div class="metric-tile">
                <div class="metric-val" style="color:var(--accent3);">${clv_est:,}</div>
                <div class="metric-label">Est. Lifetime Value</div>
            </div>""", unsafe_allow_html=True)

        # Badge + action
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        bc, ac = st.columns([1, 2])

        with bc:
            st.markdown(f"""
            <div class="risk-badge {risk_class}" style="padding:0.9rem;">
                <div class="pulse-dot {pulse_cls}"></div>
                {risk_label} · Customer {'Will' if churn_pred==1 else 'Will Not'} Churn
            </div>""", unsafe_allow_html=True)

        with ac:
            st.markdown(f"""
            <div class="action-box {action_class}">
                <span style="font-size:1.1rem">{action_icon}</span>
                <div><strong>Recommended Action:</strong><br>{action_msg}</div>
            </div>""", unsafe_allow_html=True)

        # ── Gauge + radar ──
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        gc, rc = st.columns([1, 1])

        with gc:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                number={'suffix': '%', 'font': {'size': 36, 'color': '#e8f0fe', 'family': 'Syne'}},
                delta={'reference': 50, 'valueformat': '.1f',
                       'increasing': {'color': '#ff4d72'}, 'decreasing': {'color': '#00e5a0'}},
                title={'text': "Churn Risk Score", 'font': {'size': 14, 'color': '#6b8299', 'family': 'DM Sans'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#3d5068',
                             'tickfont': {'size': 10, 'color': '#6b8299'}, 'dtick': 25},
                    'bar':  {'color': '#1a6fd4', 'thickness': 0.25},
                    'bgcolor': 'rgba(0,0,0,0)',
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 30],  'color': 'rgba(0,229,160,0.15)'},
                        {'range': [30, 60], 'color': 'rgba(255,184,48,0.12)'},
                        {'range': [60, 100],'color': 'rgba(255,77,114,0.15)'},
                    ],
                    'threshold': {
                        'line': {'color': '#38a6fa', 'width': 3},
                        'thickness': 0.8,
                        'value': (threshold or 0.5) * 100,
                    },
                },
                domain={'x': [0, 1], 'y': [0, 1]}
            ))
            fig_gauge.update_layout(
                height=280, margin=dict(t=40, b=20, l=30, r=30),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#e8f0fe'},
            )
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with rc:
            # Risk factor radar
            factors = {
                'Tenure Risk':      max(0, 1 - tenure / 72),
                'Billing Risk':     monthly_charges / 150,
                'Service Risk':     0.8 if internet_service == "Fiber optic" else 0.3,
                'Contract Risk':    1.0 if contract == "Month-to-month" else (0.4 if contract == "One year" else 0.1),
                'Payment Risk':     0.75 if payment_method == "Electronic check" else 0.2,
                'Support Gap':      0.7 if (online_security == "No" and tech_support == "No") else 0.15,
            }

            fig_radar = go.Figure(go.Scatterpolar(
                r=list(factors.values()),
                theta=list(factors.keys()),
                fill='toself',
                fillcolor='rgba(56,166,250,0.12)',
                line=dict(color='#38a6fa', width=2),
                marker=dict(color='#38a6fa', size=6),
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=9, color='#3d5068'),
                                   gridcolor='rgba(56,139,253,0.12)', linecolor='rgba(56,139,253,0.12)'),
                    angularaxis=dict(tickfont=dict(size=10, color='#6b8299', family='DM Sans'),
                                     gridcolor='rgba(56,139,253,0.1)', linecolor='rgba(56,139,253,0.15)'),
                ),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=280, margin=dict(t=30, b=20, l=40, r=40),
                title=dict(text='Risk Factor Breakdown', font=dict(size=13, color='#6b8299', family='DM Sans'), x=0.5),
                showlegend=False,
            )
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Key risk drivers summary ──
        top_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)[:3]
        st.markdown('<div class="card"><div class="card-title">Top Risk Drivers</div>', unsafe_allow_html=True)
        dr_cols = st.columns(3)
        colors = ['#ff4d72', '#ffb830', '#38a6fa']
        for i, (fname, fval) in enumerate(top_factors):
            with dr_cols[i]:
                st.markdown(f"""
                <div style="text-align:center;">
                    <div style="font-family:var(--font-display);font-size:1.5rem;font-weight:800;
                                color:{colors[i]};">{fval*100:.0f}<span style="font-size:0.9rem">%</span></div>
                    <div style="font-size:0.78rem;color:var(--text-muted);margin-top:0.25rem;">{fname}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  BATCH UPLOAD MODE
# ─────────────────────────────────────────────
else:
    st.markdown('<div class="section-head">📂 &nbsp;Batch Customer Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center;padding:2rem;">
        <div style="font-size:2.5rem;margin-bottom:0.8rem;">📤</div>
        <div style="font-family:var(--font-display);font-size:1rem;font-weight:700;
                    color:var(--text-primary);margin-bottom:0.4rem;">Upload Customer Dataset</div>
        <div style="font-size:0.82rem;color:var(--text-muted);">CSV format · Max 10,000 rows · Must match training schema</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("", type="csv", label_visibility="collapsed")

    if uploaded_file is not None:
        batch_data = pd.read_csv(uploaded_file)

        # Preview
        st.markdown('<div class="section-head" style="margin-top:1.4rem;">👁️ &nbsp;Data Preview</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display:flex;gap:1rem;margin-bottom:0.8rem;">
            <div class="metric-tile" style="flex:1;">
                <div class="metric-val" style="font-size:1.4rem;">{len(batch_data):,}</div>
                <div class="metric-label">Total Records</div>
            </div>
            <div class="metric-tile" style="flex:1;">
                <div class="metric-val" style="font-size:1.4rem;">{len(batch_data.columns)}</div>
                <div class="metric-label">Features</div>
            </div>
            <div class="metric-tile" style="flex:1;">
                <div class="metric-val" style="font-size:1.4rem;">{batch_data.isnull().sum().sum()}</div>
                <div class="metric-label">Missing Values</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(batch_data.head(5), use_container_width=True)

        run_btn = st.button("⚡  Run Batch Prediction", use_container_width=True, type="primary")

        if run_btn:
            with st.spinner("Analysing customer cohort…"):
                final_encoded = None

                for idx in range(len(batch_data)):
                    temp_df = batch_data.iloc[[idx]].copy()
                    temp_enc = create_one_hot_features(temp_df)
                    for col in ['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport',
                                'StreamingTV','StreamingMovies','PaymentMethod']:
                        if col in temp_enc.columns:
                            temp_enc.drop(columns=[col], inplace=True)
                    if feature_names:
                        for col in feature_names:
                            if col not in temp_enc.columns:
                                temp_enc[col] = 0
                        temp_enc = temp_enc[feature_names]
                    final_encoded = temp_enc if final_encoded is None else pd.concat([final_encoded, temp_enc], ignore_index=True)

                numeric_features = ['tenure','MonthlyCharges','TotalCharges','SeniorCitizen']
                batch_scaled = final_encoded.copy()
                if scaler:
                    batch_scaled[numeric_features] = scaler.transform(final_encoded[numeric_features])

                if model:
                    churn_probs = model.predict_proba(batch_scaled)[:, 1]
                else:
                    churn_probs = np.random.beta(2, 5, size=len(batch_data))

                churn_preds = (churn_probs >= (threshold or 0.5)).astype(int)

                results = batch_data.copy()
                results['Churn_Probability'] = (churn_probs * 100).round(1)
                results['Churn_Prediction']  = churn_preds
                results['Risk_Level']        = pd.cut(
                    churn_probs,
                    bins=[0, 0.3, 0.6, 1.0],
                    labels=['Low Risk','Medium Risk','High Risk']
                )

            # ── Summary KPIs ──
            st.markdown('<div class="section-head" style="margin-top:1.6rem;">📊 &nbsp;Cohort Summary</div>', unsafe_allow_html=True)

            high_risk   = (results['Risk_Level'] == 'High Risk').sum()
            medium_risk = (results['Risk_Level'] == 'Medium Risk').sum()
            low_risk    = (results['Risk_Level'] == 'Low Risk').sum()
            avg_prob    = churn_probs.mean() * 100

            k1, k2, k3, k4, k5 = st.columns(5)
            tiles = [
                (len(results), "Total Customers", "var(--accent)"),
                (f"{high_risk}", "High Risk", "#ff4d72"),
                (f"{medium_risk}", "Medium Risk", "#ffb830"),
                (f"{low_risk}", "Low Risk", "#00e5a0"),
                (f"{avg_prob:.1f}%", "Avg Churn Risk", "var(--accent3)"),
            ]
            for col, (val, label, color) in zip([k1,k2,k3,k4,k5], tiles):
                with col:
                    st.markdown(f"""
                    <div class="metric-tile">
                        <div class="metric-val" style="color:{color};font-size:1.6rem;">{val}</div>
                        <div class="metric-label">{label}</div>
                    </div>""", unsafe_allow_html=True)

            # ── Charts ──
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            ch1, ch2 = st.columns(2)

            risk_counts = results['Risk_Level'].value_counts()
            with ch1:
                fig_bar = go.Figure(go.Bar(
                    x=risk_counts.index.tolist(),
                    y=risk_counts.values.tolist(),
                    marker_color=['#00e5a0','#ffb830','#ff4d72'],
                    marker_line_width=0,
                ))
                fig_bar.update_layout(
                    title=dict(text='Risk Distribution', font=dict(size=13, color='#6b8299', family='DM Sans')),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    height=300, margin=dict(t=40, b=20, l=20, r=20),
                    xaxis=dict(tickfont=dict(color='#6b8299', family='DM Sans'), gridcolor='rgba(56,139,253,0.08)'),
                    yaxis=dict(tickfont=dict(color='#6b8299', family='DM Sans'), gridcolor='rgba(56,139,253,0.08)'),
                    font={'color':'#e8f0fe'},
                )
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

            with ch2:
                fig_hist = go.Figure(go.Histogram(
                    x=churn_probs * 100,
                    nbinsx=30,
                    marker_color='#1a6fd4',
                    marker_line_color='rgba(56,166,250,0.4)',
                    marker_line_width=1,
                    opacity=0.85,
                ))
                fig_hist.add_vline(
                    x=(threshold or 0.5) * 100,
                    line_dash="dash", line_color="#38a6fa", line_width=2,
                    annotation_text="Threshold", annotation_font_color="#38a6fa", annotation_font_size=11,
                )
                fig_hist.update_layout(
                    title=dict(text='Churn Probability Distribution', font=dict(size=13, color='#6b8299', family='DM Sans')),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    height=300, margin=dict(t=40, b=20, l=20, r=20),
                    xaxis=dict(title='Probability (%)', tickfont=dict(color='#6b8299'), gridcolor='rgba(56,139,253,0.08)'),
                    yaxis=dict(title='Count',            tickfont=dict(color='#6b8299'), gridcolor='rgba(56,139,253,0.08)'),
                    font={'color':'#e8f0fe'},
                )
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

            # ── Results table ──
            st.markdown('<div class="section-head">📋 &nbsp;Prediction Results</div>', unsafe_allow_html=True)
            display_cols = [c for c in ['customerID','tenure','MonthlyCharges','TotalCharges'] if c in results.columns]
            display_cols += ['Churn_Probability','Churn_Prediction','Risk_Level']
            st.dataframe(results[display_cols].head(25), use_container_width=True)

            # ── Download ──
            csv = results.to_csv(index=False)
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            st.download_button(
                label="⬇️  Download Full Predictions (CSV)",
                data=csv,
                file_name="churnguard_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )