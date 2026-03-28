"""
All CSS styles for the Nagpur Sustainable Area Planner
FIXED: Streamlit Cloud Compatible - Force all text colors
"""

PROFESSIONAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #eef2f5 100%);
}

/* ============================================================
   SIDEBAR - Dark Background
   ============================================================ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    background: linear-gradient(180deg, #0a2b1f 0%, #0a3b25 100%) !important;
    border-right: none !important;
}

/* ============================================================
   CRITICAL FIX: FORCE BLACK TEXT ON ALL INPUTS
   Using highest specificity with !important
   ============================================================ */
/* Number Input - Black text */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] input[type="number"],
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stNumberInput input[type="number"],
div[data-testid="stSidebar"] input,
div[data-testid="stSidebar"] .stNumberInput input {
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

/* Selectbox (Dropdown) */
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] .stSelectbox select,
div[data-testid="stSidebar"] select {
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* Streamlit's custom selectbox */
[data-baseweb="select"] > div,
[data-baseweb="select"] div[data-testid="stSelectbox"],
[data-testid="stSidebar"] [data-baseweb="select"] div {
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
}

[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p,
[data-baseweb="select"] span {
    color: #000000 !important;
}

/* Dropdown selected value */
[data-baseweb="select"] [data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

[data-baseweb="select"] span[data-testid="stMarkdownContainer"] {
    color: #000000 !important;
}

/* Dropdown options popup */
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
}

div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] div[role="option"] {
    background-color: #ffffff !important;
    color: #000000 !important;
}

div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] div[role="option"]:hover {
    background-color: #e8f5e9 !important;
}

/* ============================================================
   SIDEBAR LABELS - WHITE (Keep readable)
   ============================================================ */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stMarkdown p {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Sidebar Headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #ffffff !important;
}

/* Radio buttons text */
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}

/* Caption */
[data-testid="stSidebar"] .stCaption {
    color: #cccccc !important;
}

/* Slider */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #51cf66 !important;
}

/* Generate Button */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #51cf66 0%, #2b8c4a 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    width: 100% !important;
}

/* Zone Info Card */
.zone-info-card {
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px;
    margin-top: 15px;
}

.zone-info-card p {
    color: #ffffff !important;
    margin: 2px 0;
    font-size: 12px;
}

/* ============================================================
   MAIN CONTENT AREA - Dark text on light background
   ============================================================ */
.main,
.main *,
.stMarkdown,
.stMarkdown p,
.stMarkdown div,
div[data-testid="stMarkdownContainer"],
div[data-testid="stMarkdownContainer"] p {
    color: #1e1e1e !important;
}

/* Metric Cards */
.metric-card {
    background: #ffffff !important;
    border-radius: 12px;
    padding: 12px 16px;
    border-left: 4px solid #51cf66;
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.metric-card h4 {
    color: #666666 !important;
    font-size: 11px;
    text-transform: uppercase;
    margin: 0 0 4px 0;
}

.metric-card .val {
    font-size: 20px;
    font-weight: 700;
    color: #1e4a3a !important;
}

.metric-card .sub {
    font-size: 10px;
    color: #888888 !important;
}

/* Badges */
.badge-ok {
    background: #d4edda;
    color: #155724;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.badge-err {
    background: #f8d7da;
    color: #721c24;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

/* Grade Circle */
.grade-circle {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 800;
    color: white;
    margin: 0 auto;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    background: #eef2f5;
    border-radius: 30px;
    padding: 4px;
}

[data-testid="stTabs"] [role="tab"] {
    font-weight: 600;
    font-size: 13px;
    padding: 6px 16px;
    border-radius: 30px;
    color: #1e1e1e !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1e4a3a;
    color: white !important;
}

/* Section Headings */
.section-head {
    font-size: 16px;
    font-weight: 700;
    color: #1e4a3a !important;
    border-bottom: 2px solid #51cf66;
    padding-bottom: 4px;
    margin: 15px 0 10px 0;
    display: inline-block;
}

/* Stale Warning */
.stale-warning {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    color: #856404;
    margin-bottom: 12px;
}

/* Info Box */
.custom-info {
    background: #e8f5e9;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    color: #1e1e1e !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #888888 !important;
    font-size: 11px;
    padding: 12px 0;
    border-top: 1px solid #ddd;
    margin-top: 20px;
}

/* Streamlit metrics */
.stMetric {
    background: #ffffff;
    border-radius: 12px;
    padding: 10px;
}

.stMetric label {
    color: #666666 !important;
}

.stMetric .stMetricValue {
    color: #1e4a3a !important;
}

/* Dataframe */
.dataframe {
    color: #1e1e1e !important;
}

/* Success/Info/Warning boxes */
.stAlert {
    color: #1e1e1e !important;
}

/* Hero Banner */
.hero-banner {
    background: linear-gradient(135deg, #0a2b1f 0%, #1e4a3a 50%, #2c6e4f 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
}

.hero-banner h1 {
    font-size: 24px;
    font-weight: 800;
    margin: 0;
    color: #fff;
}

.hero-banner p {
    color: rgba(255,255,255,0.85);
    margin: 8px 0 0 0;
    font-size: 14px;
}
"""
