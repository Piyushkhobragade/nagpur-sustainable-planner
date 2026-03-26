"""
Sidebar components - EXTREME SIMPLE VERSION
"""

import streamlit as st


def render_sidebar(loader, current_location):
    """
    Super simple sidebar - just what's needed
    """
    with st.sidebar:
        # Title
        st.markdown("## 🌿 Nagpur Planner")
        st.markdown("---")
        
        # ============================================================
        # ONLY ONE AREA INPUT - Simple number box
        # ============================================================
        st.markdown("**📐 Plot Area**")
        
        # Simple: Just one number input with unit toggle
        area_unit = st.radio(
            "Unit",
            ["Sq Ft", "Acres"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if area_unit == "Sq Ft":
            area_sqft = st.number_input(
                "Area (sq ft)",
                min_value=5_000,
                max_value=50_000_000,
                value=500_000,
                step=10_000,
                format="%d",
                help="Total land area in square feet"
            )
        else:
            area_acres = st.number_input(
                "Area (acres)",
                min_value=0.5,
                max_value=1000.0,
                value=11.5,
                step=0.5,
                help="Total land area in acres (1 acre = 43,560 sq ft)"
            )
            area_sqft = area_acres * 43560
        
        st.markdown("---")
        
        # ============================================================
        # LOCATION - Simple dropdown (no emoji, just name)
        # ============================================================
        st.markdown("**📍 Location**")
        zones = loader.get_nagpur_zones()
        location = st.selectbox(
            "Select zone",
            zones,
            index=zones.index("Dharampeth") if "Dharampeth" in zones else 0,
            help="Where is your land in Nagpur?"
        )
        
        st.markdown("---")
        
        # ============================================================
        # DEVELOPMENT TYPE - Simple radio
        # ============================================================
        st.markdown("**🏗 Development Type**")
        dev_type = st.selectbox(
            "Type",
            ["Residential", "Commercial", "Mixed"],
            help="What will be the main use?"
        )
        
        st.markdown("---")
        
        # ============================================================
        # PRIORITY - Simple slider
        # ============================================================
        st.markdown("**🎯 Priority**")
        st.caption("Houses ← → Green Space")
        priority = st.select_slider(
            "",
            options=["Max Housing", "Balanced", "Max Green Space"],
            value="Balanced",
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # ============================================================
        # GENERATE BUTTON
        # ============================================================
        generate = st.button("🚀 Generate Plan", use_container_width=True, type="primary")
        
        st.markdown("---")
        
        # ============================================================
        # ZONE INFO (small)
        # ============================================================
        zone_to_show = current_location if current_location else location
        zone_info = loader.get_zone_info(zone_to_show)
        if zone_info:
            st.caption(f"ℹ️ {zone_to_show}")
            st.caption(f"Type: {zone_info.get('type', '–')}")
            st.caption(f"Density: {zone_info.get('density_factor', 0):.4f} ppsf")
    
    return area_sqft, location, dev_type, priority, generate