"""
MapGenerator – creates realistic Folium maps for the proposed layout.

Layout design:
  Red rectangles   = Residential blocks  (count + size driven by plan.houses / plan.residential_area)
  Green rectangle  = Park / Green space  (size driven by plan.green_space ratio)
  Blue zone        = Facility zone       (size driven by plan.facility_area ratio)
  Yellow lines     = Road grid
  Orange/Purple    = Petrol pumps / Community halls
  Black border     = Total site boundary

KEY FIX: Every visual element is now proportional to the plan values so the
map actually changes when priority changes.
"""

import math
import folium
from folium.plugins import HeatMap
import pandas as pd
from utils.constants import COLORS


class MapGenerator:

    def create_base_map(self, center: list, zoom: int = 15) -> folium.Map:
        return folium.Map(location=center, zoom_start=zoom,
                          tiles="CartoDB positron", control_scale=True)

    # ------------------------------------------------------------------
    def generate_proposed_layout(self, plan) -> folium.Map:
        lat, lon = plan.lat, plan.lon
        m = self.create_base_map([lat, lon], zoom=16)

        # ── Site boundary in metres / degrees ──────────────────────────
        side_m   = math.sqrt(plan.total_area * 0.0929)   # sq ft → sq m → side length
        half_lat = (side_m / 2) / 111_320
        half_lon = (side_m / 2) / (111_320 * math.cos(math.radians(lat)))

        s_lat = lat - half_lat;  n_lat = lat + half_lat
        w_lon = lon - half_lon;  e_lon = lon + half_lon
        dlat  = n_lat - s_lat
        dlon  = e_lon - w_lon

        # ── Compute proportional column widths from actual plan ratios ──
        # The site is split into 3 vertical columns:
        #   col_res  = residential  (left)
        #   col_grn  = green space  (middle-right, scales with green_space_pct)
        #   col_fac  = facilities   (right)
        total = plan.total_area
        res_ratio = plan.residential_area / total   # e.g. 0.45 – 0.55
        grn_ratio = plan.green_space      / total   # e.g. 0.15 – 0.20
        fac_ratio = plan.facility_area    / total   # 0.10 fixed
        # Road + open space fills the remainder; we don't draw separate road columns
        # but show them as yellow grid lines.

        # Normalise the three drawing zones to sum to 1.0 longitude span
        draw_total = res_ratio + grn_ratio + fac_ratio
        c_res = res_ratio  / draw_total   # fraction of dlon for residential
        c_grn = grn_ratio  / draw_total   # fraction of dlon for green
        c_fac = fac_ratio  / draw_total   # fraction of dlon for facilities

        # Absolute lon boundaries for each zone (with 2% padding on each side)
        PAD = 0.02
        res_w = w_lon + PAD * dlon
        res_e = w_lon + (PAD + c_res) * dlon

        grn_w = res_e + 0.01 * dlon
        grn_e = grn_w + c_grn * dlon

        fac_w = grn_e + 0.01 * dlon
        fac_e = w_lon + (1 - PAD) * dlon

        top_lat    = n_lat - PAD * dlat
        bottom_lat = s_lat + PAD * dlat

        # ── Feature groups ─────────────────────────────────────────────
        boundary_grp = folium.FeatureGroup(name="Site Boundary",        show=True)
        road_grp     = folium.FeatureGroup(name="Roads (Yellow)",       show=True)
        res_grp      = folium.FeatureGroup(name="Residential (Red)",    show=True)
        green_grp    = folium.FeatureGroup(name="Green Space (Green)",  show=True)
        facility_grp = folium.FeatureGroup(name="Facilities",           show=True)

        # ── 1. SITE BOUNDARY ──────────────────────────────────────────
        folium.Rectangle(
            bounds=[[s_lat, w_lon], [n_lat, e_lon]],
            color="#1a1a1a", weight=3, fill=False,
            tooltip=f"Total Site: {plan.total_area:,.0f} sq ft | {plan.location} | Priority: {plan.priority}",
        ).add_to(boundary_grp)

        # ── 2. ROAD GRID (yellow lines) ───────────────────────────────
        # Horizontal roads — number scales with plan.road_pct (more road → more lines)
        num_h_roads = max(2, min(5, round(plan.road_pct / 4)))
        for i in range(1, num_h_roads):
            f = i / num_h_roads
            folium.PolyLine(
                [(s_lat + f * dlat, w_lon), (s_lat + f * dlat, e_lon)],
                color="#FFD43B", weight=4, opacity=0.9, tooltip="Internal Road"
            ).add_to(road_grp)
        # Vertical dividers between zones
        for xlon in [res_e, grn_w, grn_e, fac_w]:
            folium.PolyLine(
                [(s_lat, xlon), (n_lat, xlon)],
                color="#FFD43B", weight=4, opacity=0.9, tooltip="Zone Road"
            ).add_to(road_grp)
        # Perimeter road
        perimeter = [[s_lat,w_lon],[n_lat,w_lon],[n_lat,e_lon],[s_lat,e_lon],[s_lat,w_lon]]
        folium.PolyLine(perimeter, color="#FFD43B", weight=5, opacity=0.95,
                        tooltip="Perimeter Road").add_to(road_grp)

        # ── 3. RESIDENTIAL BLOCKS ────────────────────────────────────
        # Number of rows scales with plan.houses so more housing = more visible blocks.
        # Formula: 1 row per every ~50 units, minimum 2, maximum 8.
        num_rows = max(2, min(8, math.ceil(plan.houses / 50)))
        row_h    = (top_lat - bottom_lat) / num_rows
        units_per_block = max(1, plan.houses // num_rows)
        pop_per_block   = max(1, plan.population // num_rows)

        for r in range(num_rows):
            blk_s = bottom_lat + r * row_h + 0.005 * dlat
            blk_n = bottom_lat + (r + 1) * row_h - 0.005 * dlat
            folium.Rectangle(
                bounds=[[blk_s, res_w], [blk_n, res_e - 0.002 * dlon]],
                color="#c0392b", weight=1,
                fill=True, fill_color="#FF6B6B",
                fill_opacity=0.55 + min(0.25, res_ratio * 0.5),  # deeper red = more housing
                tooltip=f"Residential Block {r+1}/{num_rows} | ~{units_per_block} units",
                popup=folium.Popup(
                    f"<b>Residential Block {r+1}</b><br>"
                    f"Units: ~{units_per_block}<br>"
                    f"Population: ~{pop_per_block}<br>"
                    f"Priority: {plan.priority}", max_width=220),
            ).add_to(res_grp)

        # Residential zone label
        res_centre_lon = (res_w + res_e) / 2
        res_centre_lat = (top_lat + bottom_lat) / 2
        folium.Marker(
            location=[res_centre_lat, res_centre_lon],
            icon=folium.DivIcon(html=(
                f'<div style="font-size:10px;font-weight:700;text-align:center;'
                f'background:rgba(192,57,43,0.85);color:#fff;padding:3px 7px;'
                f'border-radius:5px;white-space:nowrap;">'
                f'🏠 Residential<br>{plan.houses:,} units'
                f'</div>'
            )),
        ).add_to(res_grp)

        # ── 4. GREEN SPACE ────────────────────────────────────────────
        # Height of green rectangle scales with green_space_pct so it
        # visibly grows when priority = Max Green Space.
        grn_height_frac = min(0.96, grn_ratio * 5)   # scale 15%→0.75, 20%→1.0
        grn_s = bottom_lat + (1 - grn_height_frac) * (top_lat - bottom_lat) * 0.5
        grn_n = top_lat - (1 - grn_height_frac) * (top_lat - bottom_lat) * 0.5

        folium.Rectangle(
            bounds=[[grn_s, grn_w], [grn_n, grn_e]],
            color="#1e8449", weight=1,
            fill=True, fill_color="#51CF66",
            fill_opacity=0.55 + min(0.3, grn_ratio * 2),  # deeper green = more green space
            tooltip=f"Green Space | {plan.green_space:,.0f} sq ft ({plan.green_space_pct:.1f}%)",
            popup=folium.Popup(
                f"<b>Green Space / Park</b><br>"
                f"{plan.green_space:,.0f} sq ft<br>"
                f"{plan.green_space_pct:.1f}% of total<br>"
                f"Priority: {plan.priority}", max_width=220),
        ).add_to(green_grp)

        # Park label + tree icon
        grn_centre_lon = (grn_w + grn_e) / 2
        grn_centre_lat = (grn_s + grn_n) / 2
        folium.Marker(
            location=[grn_centre_lat, grn_centre_lon],
            icon=folium.DivIcon(html=(
                f'<div style="font-size:22px;text-align:center;">&#x1F333;</div>'
                f'<div style="font-size:9px;text-align:center;background:rgba(30,132,73,0.85);'
                f'color:#fff;border-radius:4px;padding:2px 5px;font-weight:700;">'
                f'{plan.green_space_pct:.1f}% Green</div>'
            )),
        ).add_to(green_grp)

        # ── 5. FACILITY ZONE ──────────────────────────────────────────
        folium.Rectangle(
            bounds=[[bottom_lat, fac_w], [top_lat, fac_e]],
            color="#1a5276", weight=1,
            fill=True, fill_color="#AED6F1", fill_opacity=0.45,
            tooltip=f"Facility Zone | {plan.facility_area:,.0f} sq ft",
        ).add_to(facility_grp)

        # ── 6. FACILITY MARKERS — evenly spaced grid inside facility zone ──
        # Build full facility list (all required, not capped at 2-3)
        facilities = []
        for i in range(plan.schools):
            facilities.append(("&#x1F3EB;", "School",
                f"School {i+1}/{plan.schools}",
                f"Required: {plan.schools} | 1 per 5,000 people"))
        for i in range(plan.hospitals):
            facilities.append(("&#x1F3E5;", "Hospital",
                f"Hospital {i+1}/{plan.hospitals}",
                f"Required: {plan.hospitals} | 1 per 15,000 people"))
        for i in range(plan.petrol_pumps):
            facilities.append(("&#x26FD;", "Petrol Pump",
                f"Pump {i+1}/{plan.petrol_pumps}",
                f"Required: {plan.petrol_pumps} | 1 per 25,000 people"))
        for i in range(plan.community_halls):
            facilities.append(("&#x1F3DB;", "Community Hall",
                f"Hall {i+1}/{plan.community_halls}",
                f"Required: {plan.community_halls} | 1 per 10,000 people"))

        if facilities:
            n = len(facilities)
            # Grid: 2 columns, ceil(n/2) rows — evenly spaced inside facility zone
            cols    = 2
            rows_f  = math.ceil(n / cols)
            fac_lat_span = top_lat - bottom_lat
            fac_lon_span = fac_e - fac_w

            for idx, (emoji, ftype, label, detail) in enumerate(facilities):
                col_i = idx % cols
                row_i = idx // cols
                # Centre each marker in its grid cell
                mlat = top_lat - fac_lat_span * (row_i + 0.5) / rows_f
                mlon = fac_w  + fac_lon_span * (col_i + 0.5) / cols

                folium.Marker(
                    location=[mlat, mlon],
                    popup=folium.Popup(f"<b>{label}</b><br>{detail}", max_width=220),
                    tooltip=label,
                    icon=folium.DivIcon(
                        html=(
                            f'<div style="text-align:center;line-height:1;">'
                            f'<div style="font-size:20px;">{emoji}</div>'
                            f'<div style="font-size:8px;background:rgba(26,82,118,0.85);'
                            f'color:#fff;border-radius:3px;padding:1px 4px;'
                            f'margin-top:1px;font-weight:700;white-space:nowrap;">'
                            f'{ftype}</div>'
                            f'</div>'
                        ),
                        icon_size=(60, 36),
                        icon_anchor=(30, 18),
                    ),
                ).add_to(facility_grp)

        # Facility zone label
        folium.Marker(
            location=[top_lat - 0.03 * dlat, (fac_w + fac_e) / 2],
            icon=folium.DivIcon(html=(
                f'<div style="font-size:9px;font-weight:700;text-align:center;'
                f'background:rgba(26,82,118,0.85);color:#fff;padding:2px 6px;'
                f'border-radius:4px;white-space:nowrap;">'
                f'🏗 Facilities ({len(facilities)})'
                f'</div>'
            )),
        ).add_to(facility_grp)

        # ── 7. SITE LABEL ─────────────────────────────────────────────
        folium.Marker(
            location=[n_lat + half_lat * 0.2, lon],
            icon=folium.DivIcon(html=(
                f'<div style="font-size:12px;font-weight:700;font-family:sans-serif;'
                f'background:rgba(10,35,66,0.88);color:#fff;padding:5px 12px;'
                f'border-radius:6px;white-space:nowrap;'
                f'box-shadow:0 2px 6px rgba(0,0,0,0.3);">'
                f'&#x1F4CD; {plan.location} &nbsp;|&nbsp; {plan.total_area:,.0f} sq ft'
                f' &nbsp;|&nbsp; {plan.priority}'
                f'</div>'
            )),
        ).add_to(m)

        # Add all feature groups
        for grp in [boundary_grp, road_grp, res_grp, green_grp, facility_grp]:
            grp.add_to(m)
        
        # LayerControl - With custom close button and mobile friendly
        layer_control_html = """
        <div id="layer-control-container" style="position:fixed;bottom:20px;right:10px;z-index:1000;">
            <style>
                .leaflet-control-layers {
                    margin-bottom: 0 !important;
                }
                #layer-control-toggle {
                    background: white;
                    border-radius: 4px;
                    padding: 8px 12px;
                    cursor: pointer;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
                    font-size: 14px;
                    font-weight: bold;
                    margin-bottom: 5px;
                    display: inline-block;
                }
                #layer-control-toggle:hover {
                    background: #f0f0f0;
                }
                @media (max-width: 768px) {
                    .leaflet-control-layers {
                        max-width: 140px !important;
                        font-size: 11px !important;
                    }
                    .leaflet-control-layers-expanded {
                        padding: 6px 8px !important;
                    }
                }
            </style>
            <div id="layer-control-toggle" onclick="toggleLayerControl()">🗺️ Layers ✕</div>
            <div id="layer-control-wrapper" style="display:block;"></div>
        </div>
        <script>
            function toggleLayerControl() {
                var wrapper = document.getElementById('layer-control-wrapper');
                if (wrapper.style.display === 'none') {
                    wrapper.style.display = 'block';
                } else {
                    wrapper.style.display = 'none';
                }
            }
        </script>
        """
        m.get_root().html.add_child(folium.Element(layer_control_html))
        
        # Add LayerControl but hide it initially in the wrapper
        layer_control = folium.LayerControl(collapsed=False)
        layer_control.add_to(m)
        
        # Move LayerControl into our wrapper div
        move_control_script = """
        <script>
            setTimeout(function() {
                var layerControl = document.querySelector('.leaflet-control-layers');
                var wrapper = document.getElementById('layer-control-wrapper');
                if (layerControl && wrapper) {
                    wrapper.appendChild(layerControl);
                    layerControl.style.position = 'relative';
                    layerControl.style.bottom = 'auto';
                    layerControl.style.right = 'auto';
                }
            }, 100);
        </script>
        """
        m.get_root().html.add_child(folium.Element(move_control_script))
        
        return m

    # ------------------------------------------------------------------
    def create_heatmap(self, density_df: pd.DataFrame) -> folium.Map:
        from utils.constants import NAGPUR_CENTER
        m = self.create_base_map(NAGPUR_CENTER, zoom=12)
        heat_data = [
            [r["center_latitude"], r["center_longitude"], r["population_density"] * 5000]
            for _, r in density_df.iterrows()
        ]
        HeatMap(heat_data, radius=40, blur=25, min_opacity=0.4).add_to(m)
        for _, row in density_df.iterrows():
            folium.Marker(
                location=[row["center_latitude"], row["center_longitude"]],
                icon=folium.DivIcon(html=(
                    f'<div style="font-size:9px;font-weight:600;color:#222;'
                    f'background:rgba(255,255,255,0.8);padding:1px 4px;'
                    f'border-radius:3px;">{row["ward_name"]}</div>'
                )),
                tooltip=(
                    f"{row['ward_name']}: {row['population_density']:.4f} ppsf | "
                    f"Pop: {int(row['population']):,}"
                ),
            ).add_to(m)
        return m

    # ------------------------------------------------------------------
    def add_existing_amenities(self, m, amenities_df, zone=None):
        df = amenities_df if zone is None else amenities_df[amenities_df["ward"] == zone]
        icon_map = {
            "School":      ("graduation-cap", "blue"),
            "Hospital":    ("plus-sign",      "red"),
            "Petrol Pump": ("tint",           "orange"),
            "Park":        ("leaf",           "green"),
        }
        grp = folium.FeatureGroup(name="Existing Amenities")
        for _, row in df.iterrows():
            icon_name, color = icon_map.get(row["type"], ("info-sign", "gray"))
            cap = f" (Capacity: {row['capacity']})" if row.get("capacity", 0) > 0 else ""
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=folium.Popup(
                    f"<b>{row['name']}</b><br>{row['type']}{cap}<br>Ward: {row['ward']}",
                    max_width=220),
                tooltip=f"{row['type']}: {row['name']}",
                icon=folium.Icon(color=color, icon=icon_name, prefix="glyphicon"),
            ).add_to(grp)
        grp.add_to(m)
        return m