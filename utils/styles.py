"""
All CSS styles for the Nagpur Sustainable Area Planner
Mobile Friendly + Simple UI - FIXED VERSION
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
   SIDEBAR - Clean & Simple
   ============================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a2b1f 0%, #0a3b25 100%);
    border-right: none;
    padding: 0.5rem;
}

/* Sidebar text colors - Keep white for labels, but inputs need dark text */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #e8f0e8 !important;
}

/* Sidebar Title */
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
}

/* ============================================================
   FIXED: NUMBER INPUT - Clean & Readable
   ============================================================ */
[data-testid="stSidebar"] .stNumberInput input {
    background: #ffffff !important;
    color: #1a2a1a !important;
    border: 1px solid #cbd5e0 !important;
    border-radius: 8px !important;
    padding: 10px 12px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: #51cf66 !important;
    box-shadow: 0 0 0 2px rgba(81, 207, 102, 0.2) !important;
    outline: none !important;
}

/* ============================================================
   FIXED: SELECTBOX/DROPDOWN - Clean, No Nested Div Clutter
   ============================================================ */
/* Target the main select container */
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #cbd5e0 !important;
}

/* Target the select input area */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #ffffff !important;
    border: none !important;
    min-height: 42px !important;
}

/* Target the text inside select */
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] [role="combobox"] {
    color: #1a2a1a !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    background: #ffffff !important;
    padding: 8px 12px !important;
}

/* Remove extra nested div backgrounds */
[data-testid="stSidebar"] [data-baseweb="select"] div[data-testid="stSelectbox"] {
    background: transparent !important;
}

/* Dropdown arrow styling */
[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #5a6e5a !important;
    stroke: #5a6e5a !important;
}

[data-testid="stSidebar"] .stRadio label span {
    color: #ffffff !important;
}

[data-testid="stSidebar"] .stRadio label p,
[data-testid="stSidebar"] .stRadio label span,
[data-testid="stSidebar"] .stRadio label div {
    color: #ffffff !important;
}

/* Dropdown menu styling (when opened) */
[data-baseweb="popover"] {
    background: #ffffff !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    border: 1px solid #e2e8f0 !important;
}

[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {
    color: #1a2a1a !important;
    background: #ffffff !important;
    padding: 10px 12px !important;
    font-size: 13px !important;
}

[data-baseweb="popover"] li:hover,
[data-baseweb="popover"] [role="option"]:hover {
    background: #f0fdf4 !important;
    color: #166534 !important;
}

/* ============================================================
   FIXED: RADIO BUTTONS - Clean & Simple
   ============================================================ */
[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: rgba(255, 255, 255, 0.08);
    padding: 8px;
    border-radius: 12px;
}

[data-testid="stSidebar"] .stRadio label {
    margin-right: 0;
    padding: 6px 16px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    cursor: pointer;
    color: #ffffff !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    background: transparent;
}

[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
    background: #51cf66 !important;
    color: #ffffff !important;
}

/* ============================================================
   SELECT SLIDER (Priority) - Clean
   ============================================================ */
[data-testid="stSidebar"] .stSelectSlider label {
    color: #e8f0e8 !important;
}

[data-testid="stSidebar"] .stSelectSlider div[data-baseweb="select"] {
    background: #ffffff !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stSelectSlider input {
    color: #1a2a1a !important;
    background: #ffffff !important;
}

/* ============================================================
   GENERATE BUTTON - Big and Clear
   ============================================================ */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #51cf66 0%, #2b8c4a 100%);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 14px 20px;
    font-weight: 700;
    font-size: 18px;
    width: 100%;
    transition: all 0.3s ease;
    margin-top: 10px;
    cursor: pointer;
}

[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(81, 207, 102, 0.4);
}

/* ============================================================
   ZONE INFO CARD - Simple
   ============================================================ */
.zone-info-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 12px;
    margin-top: 15px;
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.zone-info-card p {
    margin: 2px 0;
    font-size: 11px;
    color: #e8f0e8;
}

/* ============================================================
   HERO BANNER - Mobile Friendly
   ============================================================ */
.hero-banner {
    background: linear-gradient(135deg, #0a2b1f 0%, #1e4a3a 50%, #2c6e4f 100%);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    text-align: center;
}

.hero-banner h1 {
    font-size: 22px;
    font-weight: 800;
    margin: 0;
    color: #fff;
}

.hero-banner p {
    color: rgba(255, 255, 255, 0.85);
    margin: 8px 0 0 0;
    font-size: 13px;
}

/* ============================================================
   METRIC CARDS - Responsive Grid
   ============================================================ */
.metric-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 12px 16px;
    border: 1px solid rgba(81, 207, 102, 0.2);
    margin-bottom: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.metric-card h4 {
    color: #5a6e5a;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0 0 4px 0;
}

.metric-card .val {
    font-size: 20px;
    font-weight: 800;
    color: #1e4a3a;
}

.metric-card .sub {
    font-size: 10px;
    color: #8b9a8b;
    margin-top: 2px;
}

/* ============================================================
   BADGES - Simple
   ============================================================ */
.badge-ok {
    background: #d4edda;
    color: #155724;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}

.badge-err {
    background: #f8d7da;
    color: #721c24;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    display: inline-block;
}

/* Grade Circle */
.grade-circle {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: 800;
    color: white;
    margin: 0 auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Tabs - Mobile Friendly */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 30px;
    padding: 4px;
    flex-wrap: wrap;
}

[data-testid="stTabs"] [role="tab"] {
    font-weight: 600;
    font-size: 12px;
    padding: 6px 14px;
    border-radius: 30px;
}

/* Section Headings */
.section-head {
    font-size: 16px;
    font-weight: 700;
    color: #1e4a3a;
    border-bottom: 2px solid #51cf66;
    padding-bottom: 4px;
    margin: 15px 0 10px 0;
    display: inline-block;
}

/* Stale Warning */
.stale-warning {
    background: #fff8e7;
    border-left: 4px solid #ffc107;
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 12px;
    color: #856404;
    margin-bottom: 12px;
}

/* Info Box */
.custom-info {
    background: #e8f5e9;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}

/* Footer */
.footer {
    text-align: center;
    color: #8b9a8b;
    font-size: 10px;
    padding: 12px 0;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
    margin-top: 20px;
}

/* Map legend and controls mobile optimization */
.leaflet-control-layers {
    position: relative !important;
}

.leaflet-control-layers-toggle {
    cursor: pointer !important;
}

.leaflet-control-layers-expanded {
    position: relative;
}

/* Mobile map controls compact */
@media (max-width: 768px) {
    .hero-banner h1 {
        font-size: 18px;
    }
    
    .metric-card .val {
        font-size: 18px;
    }
    
    [data-testid="stTabs"] [role="tab"] {
        font-size: 11px;
        padding: 4px 10px;
    }
    
    .leaflet-control-layers {
        max-width: 130px !important;
        font-size: 10px !important;
        bottom: 10px !important;
        top: auto !important;
        right: 10px !important;
        left: auto !important;
    }
    
    .leaflet-control-layers-expanded {
        padding: 4px 6px !important;
        max-height: 200px !important;
        overflow-y: auto !important;
    }
    
    .leaflet-control-layers-toggle {
        width: 28px !important;
        height: 28px !important;
        background-size: 18px !important;
    }
}
"""
