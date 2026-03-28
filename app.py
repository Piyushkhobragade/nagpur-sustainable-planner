"""
Nagpur Sustainable Area Planner - EXTREME SIMPLE
Just what's needed - no overcomplication
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time
import json

from planner_logic import SustainablePlanner
from ml_model import DensityPredictor
from map_generator import MapGenerator
from data_loader import DataLoader
from streamlit_folium import st_folium
from utils.helpers import format_number, area_label, sustainability_grade
from utils.styles import PROFESSIONAL_CSS
from components.sidebar import render_sidebar

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nagpur Sustainable Planner",
    page_icon="🌿",
    layout="wide",
)

# ── FIX: Correct text colors (dark where dark should be, light where light should be) ──
st.markdown("""
<style>
    /* Main content area - Dark text on light background */
    .main .stMarkdown p,
    .main .stMarkdown div,
    .main [data-testid="stMarkdownContainer"] p,
    .main [data-testid="stMarkdownContainer"] div {
        color: #1e2a1e !important;
    }
    
    /* Tab headers - Dark when inactive */
    [data-testid="stTabs"] [role="tab"] {
        color: #2c3e2c !important;
        background: #eef2f5 !important;
    }
    
    /* Tab headers - White when active/selected */
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: white !important;
        background: #1e4a3a !important;
    }
    
    /* Tab content area - All text dark */
    .stTabs [data-testid="stMarkdownContainer"],
    .stTabs .stMarkdown,
    .stTabs p,
    .stTabs div {
        color: #1e2a1e !important;
    }
    
    /* Metric cards - Dark text */
    .stMetric {
        background: #ffffff;
        border-radius: 12px;
        padding: 10px;
    }
    
    .stMetric label {
        color: #5a6e5a !important;
    }
    
    .stMetric .stMetricValue {
        color: #1e4a3a !important;
    }
    
    /* Dataframe - Dark text */
    .dataframe,
    .dataframe td,
    .dataframe th {
        color: #1e2a1e !important;
        background: #ffffff !important;
    }
    
    /* Plotly charts - Dark text */
    .js-plotly-plot .plotly .main-svg text {
        fill: #1e2a1e !important;
    }
    
    /* Section headings */
    .section-head {
        color: #1e4a3a !important;
    }
    
    /* Info/warning boxes - Dark text */
    .stAlert p {
        color: #1e2a1e !important;
    }
    
    /* Sidebar - Keep as is (dark background, white text) */
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        color: #e8f0e8 !important;
    }
    
    /* Sidebar inputs - White background, dark text */
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select,
    [data-testid="stSidebar"] [data-baseweb="select"] div {
        color: #1e2a1e !important;
        background: #ffffff !important;
    }
    
</style>
""", unsafe_allow_html=True)

# ── Apply CSS ──────────────────────────────────────────────────────────────
st.markdown(f"<style>{PROFESSIONAL_CSS}</style>", unsafe_allow_html=True)

# ── Cached initialisations ──────────────────────────────────────────────────
@st.cache_resource
def get_planner():
    return SustainablePlanner()

@st.cache_resource
def get_ml():
    predictor = DensityPredictor()
    if predictor.model is None:
        with st.spinner("🤖 Training ML model..."):
            predictor.train_model()
    return predictor

@st.cache_resource
def get_loader():
    return DataLoader()

@st.cache_resource
def get_map_gen():
    return MapGenerator()

planner = get_planner()
loader = get_loader()
map_gen = get_map_gen()

# ── Session state ────────────────────────────────────────────────────────────
if "plan" not in st.session_state:
    st.session_state.plan = None
if "ml_result" not in st.session_state:
    st.session_state.ml_result = None
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = None

# ── Sidebar Inputs ──────────────────────────────────────────────────────────
current_location = st.session_state.plan.location if st.session_state.plan else None
area_sqft, location, dev_type, priority, generate = render_sidebar(loader, current_location)

# ── Hero Banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #0a2b1f, #1e4a3a); border-radius: 16px; padding: 20px; margin-bottom: 20px;">
    <h1 style="color: white; font-size: 24px; margin: 0;">🌇 Nagpur Sustainable Area Planner</h1>
    <p style="color: rgba(255,255,255,0.8); margin: 8px 0 0 0;">Enter area → Generate plan → See map</p>
</div>
""", unsafe_allow_html=True)

# ── Stale check ─────────────────────────────────────────────────────────────
_current_inputs = (area_sqft, location, dev_type, priority)
_plan_is_stale = (
    st.session_state.plan is not None
    and st.session_state.last_inputs is not None
    and _current_inputs != st.session_state.last_inputs
)

# ── Generate Plan ───────────────────────────────────────────────────────────
if generate:
    with st.spinner("Generating plan..."):
        prog = st.progress(0)
        
        plan = planner.generate_plan(area_sqft, location, dev_type, priority)
        prog.progress(40)
        
        ml = get_ml()
        zone_info = loader.get_zone_info(location)
        coords = loader.get_coordinates_for_zone(location)
        ml_result = ml.predict_density(
            lat=coords[0], lon=coords[1],
            existing_density=zone_info.get("density_factor", 0.0015),
            zone_type=zone_info.get("type", "Medium Density Residential"),
            area_sqft=area_sqft,
        )
        prog.progress(80)
        time.sleep(0.2)
        prog.progress(100)
        prog.empty()
    
    st.session_state.plan = plan
    st.session_state.ml_result = ml_result
    st.session_state.last_inputs = _current_inputs
    st.balloons()
    st.success(f"✅ Plan ready for **{location}** | {area_label(area_sqft)}")

# ── Stale warning ───────────────────────────────────────────────────────────
if _plan_is_stale:
    st.warning("⚠️ Settings changed — click Generate Plan to update")

# ── Tabs ────────────────────────────────────────────────────────────────────
plan = st.session_state.plan

tab1, tab2, tab3 = st.tabs(["📋 Report", "📊 Charts", "🗺 Map"])

# ============================================================
# TAB 1 - REPORT
# ============================================================
with tab1:
    if plan is None:
        st.info("👈 Enter area in sidebar and click Generate Plan")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(
                f'<div style="width:80px;height:80px;border-radius:50%;background:{plan.grade_color};display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:bold;color:white;margin:0 auto;">{plan.grade}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f"<p style='text-align:center;'>Score: {plan.sustainability_score:.0f}/100</p>", unsafe_allow_html=True)
        
        with col2:
            badge = "✅ COMPLIANT" if plan.compliant else "⚠️ NON-COMPLIANT"
            st.markdown(f"**Compliance:** {badge}")
            for note in plan.compliance_notes:
                st.markdown(f"- {note}")
        
        st.markdown("---")
        
        # Simple metrics in columns
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("Total Area", f"{format_number(plan.total_area)} sq ft", area_label(plan.total_area))
        with col_b:
            st.metric("Population", format_number(plan.population))
        with col_c:
            st.metric("Houses", format_number(plan.houses))
        with col_d:
            st.metric("Green Space", f"{plan.green_space_pct:.0f}%", f"{format_number(plan.green_space)} sq ft")
        
        st.markdown("---")
        
        col_a, col_b, col_c, col_d, col_e = st.columns(5)
        with col_a:
            st.metric("🏫 Schools", plan.schools)
        with col_b:
            st.metric("🏥 Hospitals", plan.hospitals)
        with col_c:
            st.metric("🌳 Parks", plan.parks)
        with col_d:
            st.metric("⛽ Petrol Pumps", plan.petrol_pumps)
        with col_e:
            st.metric("🏛 Community Halls", plan.community_halls)

# ============================================================
# TAB 2 - CHARTS
# ============================================================
with tab2:
    if plan is None:
        st.info("Generate a plan first")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart
            labels = ["Residential", "Green Space", "Roads", "Facilities"]
            values = [plan.residential_area, plan.green_space, plan.road_area, plan.facility_area]
            colors = ["#FF6B6B", "#51CF66", "#FFD43B", "#339AF0"]
            fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.4, marker_colors=colors))
            fig.update_layout(title="Land Use", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gauge - Fixed centering
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=plan.sustainability_score,
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": plan.grade_color},
                    "steps": [
                        {"range": [0, 50], "color": "#ffd6d6"},
                        {"range": [50, 75], "color": "#fff3cd"},
                        {"range": [75, 100], "color": "#d4edda"},
                    ],
                },
                title={"text": "Sustainability Score"},
                number={"suffix": "/100"},
                domain={"x": [0, 1], "y": [0, 1]}
            ))
            fig_gauge.update_layout(
                height=350, 
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=50, b=0, l=0, r=0)
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

# ============================================================
# TAB 3 - MAP
# ============================================================
with tab3:
    if plan is None:
        st.info("Generate a plan first")
    else:
        # Mobile responsive map container
        st.markdown("""
        <style>
        /* Mobile friendly map container */
        @media (max-width: 768px) {
            .map-container {
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            /* Hide folium default legend on mobile if it's cluttering */
            .folium-map .leaflet-control-attribution {
                font-size: 8px !important;
                bottom: 0 !important;
            }
            .folium-map .info.legend {
                font-size: 10px !important;
                max-width: 120px !important;
                padding: 4px 6px !important;
            }
        }
        </style>
        <div class="map-container">
        """, unsafe_allow_html=True)
        
        layout_map = map_gen.generate_proposed_layout(plan)
        
        # Make map responsive with better mobile defaults
        st_folium(
            layout_map, 
            width=None, 
            height=450 if st.session_state.get('mobile_view', False) else 500,
            returned_objects=[],
            key=f"map_{plan.location}_{plan.priority}"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Optional: Add map controls hint for mobile
        st.caption("📍 Tap + / - to zoom | Drag to pan")

# ============================================================
# TAB 4 - EXPORT
# ============================================================
# with tab4:
#     if plan is None:
#         st.info("Generate a plan first")
#     else:
#         st.markdown("### 📥 Download Plan")
        
#         # Create export data
#         export_data = {
#             "Total Area (sq ft)": plan.total_area,
#             "Location": plan.location,
#             "Development Type": plan.dev_type,
#             "Priority": plan.priority,
#             "Residential Area (sq ft)": plan.residential_area,
#             "Green Space (sq ft)": plan.green_space,
#             "Road Area (sq ft)": plan.road_area,
#             "Population": plan.population,
#             "Houses": plan.houses,
#             "Density (ppsf)": plan.density_ppsf,
#             "Schools": plan.schools,
#             "Hospitals": plan.hospitals,
#             "Parks": plan.parks,
#             "Petrol Pumps": plan.petrol_pumps,
#             "Community Halls": plan.community_halls,
#             "Green Space %": plan.green_space_pct,
#             "Sustainability Score": plan.sustainability_score,
#             "Grade": plan.grade,
#             "Compliant": "Yes" if plan.compliant else "No",
#         }
        
#         df_export = pd.DataFrame(list(export_data.items()), columns=["Metric", "Value"])
        
#         col1, col2 = st.columns(2)
#         with col1:
#             csv = df_export.to_csv(index=False).encode()
#             st.download_button("⬇️ Download CSV", csv, f"plan_{plan.location}.csv", "text/csv", use_container_width=True)
        
#         with col2:
#             json_data = json.dumps(export_data, indent=2).encode()
#             st.download_button("⬇️ Download JSON", json_data, f"plan_{plan.location}.json", "application/json", use_container_width=True)
        
#         st.markdown("---")
#         st.markdown("### 📋 Summary Text")
#         summary = f"""
# NAGPUR SUSTAINABLE AREA PLAN
# =============================
# Location     : {plan.location}
# Total Area   : {format_number(plan.total_area)} sq ft ({plan.total_area/43560:.1f} acres)
# Dev Type     : {plan.dev_type} | Priority: {plan.priority}

# LAND USE
#   Residential  : {format_number(plan.residential_area)} sq ft ({plan.residential_area/plan.total_area*100:.1f}%)
#   Green Space  : {format_number(plan.green_space)} sq ft ({plan.green_space_pct:.1f}%)
#   Roads        : {format_number(plan.road_area)} sq ft ({plan.road_pct:.1f}%)

# POPULATION
#   Estimated    : {format_number(plan.population)} people
#   Houses       : {format_number(plan.houses)}
#   Density      : {plan.density_ppsf:.4f} ppsf

# INFRASTRUCTURE
#   Schools      : {plan.schools}
#   Hospitals    : {plan.hospitals}
#   Parks        : {plan.parks}
#   Petrol Pumps : {plan.petrol_pumps}
#   Comm. Halls  : {plan.community_halls}

# SUSTAINABILITY: {plan.sustainability_score:.0f}/100 | Grade: {plan.grade}
# COMPLIANCE    : {"PASS ✅" if plan.compliant else "FAIL ⚠"}
# """
#         st.code(summary, language="text")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<p style='text-align:center;color:#888;font-size:11px;'>🌿 Nagpur Sustainable Area Planner | ML-Powered | UDPFI Guidelines</p>", unsafe_allow_html=True)
