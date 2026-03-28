"""
All CSS styles for the Nagpur Sustainable Area Planner
FIXED: Force black text on all inputs
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
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2b1f 0%, #0a3b25 100%);
    border-right: none;
    padding: 1rem;
}

/* Sidebar Headings - White */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #ffffff !important;
}

/* Sidebar Labels - White */
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* ============================================================
   FIX: ALL INPUT FIELDS - BLACK TEXT ON WHITE BACKGROUND
   ============================================================ */
/* Number Input */
[data-testid="stSidebar"] .stNumberInput input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* Text Input */
[data-testid="stSidebar"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* Selectbox (Dropdown) */
[data-testid="stSidebar"] select {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* Streamlit's custom selectbox */
[data-testid="stSidebar"] [data-baseweb="select"] div {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cccccc !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] div div {
    color: #000000 !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] input {
    color: #000000 !important;
}

/* Radio button text - White */
[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}

/* Slider text */
[data-testid="stSidebar"] .stSlider {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #51cf66 !important;
}

/* Caption text */
[data-testid="stSidebar"] .stCaption {
    color: #cccccc !important;
}

/* Generate Button */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #51cf66 0%, #2b8c4a 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 16px;
    width: 100%;
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
   MAIN CONTENT AREA - Black text on light background
   ============================================================ */
/* All main content text should be dark */
.main .stMarkdown,
.main .stMarkdown p,
.main .stMarkdown div,
.main div[data-testid="stMarkdownContainer"] p,
.main div[data-testid="stMarkdownContainer"] div {
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
[data-testid="stTabs"] {
    background: transparent;
}

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

/* Streamlit default metrics */
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

/* Dropdown popup options */
div[data-baseweb="popover"] div {
    background-color: #ffffff !important;
    color: #000000 !important;
}

div[data-baseweb="popover"] ul li {
    color: #000000 !important;
}

div[data-baseweb="popover"] ul li:hover {
    background-color: #e8f5e9 !important;
}
"""
