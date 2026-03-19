"""
EarthMender AI — Main Application (v4 Final)
=============================================
Run: streamlit run app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from PIL import Image
from streamlit_folium import st_folium

from phase1_detection.detector  import PlasticDetector, confidence_band
from phase2_reporting.reporter  import (
    load_reports, save_report, resolve_report, reopen_report,
    get_open_reports, get_resolved_reports, get_report_stats,
    render_gps_capture, get_gps_coords_from_inputs, get_manual_location,
)
from phase3_map.mapper          import build_map, get_hotspots
from phase4_dashboard.dashboard import render_full_dashboard
from phase5_education.educator  import render_education_tab

st.set_page_config(
    page_title="EarthMender AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

for k, v in {
    "logged_in": False, "user_name": "", "user_role": "Citizen",
    "user_initials": "?", "active_tab": 0, "last_tab": 0,
    "captured_image": None, "detection_done": False,
    "annotated_img": None, "detections": [], "quality": None,
    "show_all_reports": False, "detect_mode": "📷 Camera",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

#MainMenu,header,footer,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"],
[data-testid="collapsedControl"],section[data-testid="stSidebar"]{display:none!important}

*,*::before,*::after{box-sizing:border-box}

html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],
.main,[data-testid="stMainBlockContainer"]{
  font-family:'Inter',sans-serif!important;
  background:#0a1410!important;color:#f0f0f0!important;
  padding:0!important;margin:0!important}

.block-container{padding:0!important;max-width:480px!important;margin:0 auto!important}

.em-topbar{background:#1a7a4a;padding:14px 18px 12px;display:flex;
  align-items:center;justify-content:space-between;
  position:sticky;top:0;z-index:100}
.em-avatar{width:40px;height:40px;border-radius:50%;
  background:rgba(255,255,255,0.2);display:flex;align-items:center;
  justify-content:center;font-size:14px;font-weight:700;color:#fff}
.em-greeting{color:rgba(255,255,255,0.7);font-size:11px}
.em-username{color:#fff;font-size:15px;font-weight:700}
.em-topbar-icons{display:flex;gap:8px}
.em-icon-btn{width:36px;height:36px;border-radius:50%;
  background:rgba(255,255,255,0.15);display:flex;
  align-items:center;justify-content:center}

.em-hero{background:linear-gradient(160deg,#1a7a4a 0%,#145c38 100%);padding:0 18px 22px}
.em-balance-card{background:rgba(255,255,255,0.1);border-radius:16px;
  padding:16px 18px 14px;border:0.5px solid rgba(255,255,255,0.18);margin-bottom:14px}
.em-balance-label{color:rgba(255,255,255,0.65);font-size:11px;margin-bottom:6px}
.em-balance-val{color:#fff;font-size:26px;font-weight:800}
.em-hero-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.em-hstat{background:rgba(255,255,255,0.1);border-radius:10px;padding:10px 6px;text-align:center}
.em-hstat-val{color:#fff;font-size:17px;font-weight:700}
.em-hstat-label{color:rgba(255,255,255,0.6);font-size:9px;margin-top:2px}

.em-page{background:#0a1410;padding:0 16px 20px}
.em-section{padding:20px 0 8px}
.em-section-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.em-section-title{font-size:15px;font-weight:700;color:#f0f0f0}
.em-see-all{font-size:12px;color:#4caf80;cursor:pointer;font-weight:600}

.em-qa-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.em-qa-card{background:#1a2e20;border-radius:14px;padding:14px 8px 10px;
  display:flex;flex-direction:column;align-items:center;gap:8px;
  border:0.5px solid rgba(255,255,255,0.08);cursor:pointer}
.em-qa-icon{width:44px;height:44px;border-radius:12px;display:flex;
  align-items:center;justify-content:center}
.em-qa-label{font-size:10px;color:#aaa;font-weight:600;text-align:center}

.em-alert{background:rgba(255,152,0,0.12);border-radius:12px;padding:11px 14px;
  display:flex;align-items:center;gap:10px;border:0.5px solid rgba(255,152,0,0.3);margin:8px 0 16px}
.em-alert-dot{width:8px;height:8px;border-radius:50%;background:#ff9800;flex-shrink:0}
.em-alert-text{font-size:12px;color:#ffcc80;flex:1}
.em-alert-cta{font-size:12px;color:#81c784;font-weight:700}

.em-case-card{background:#1a2e20;border-radius:14px;padding:14px 16px;
  border:0.5px solid rgba(255,255,255,0.07);display:flex;
  align-items:flex-start;gap:12px;margin-bottom:10px}
.em-case-dot{width:9px;height:9px;border-radius:50%;margin-top:5px;flex-shrink:0}
.em-case-type{font-size:13px;font-weight:600;color:#eee}
.em-case-loc{font-size:11px;color:#888;margin-top:3px}
.em-case-meta{display:flex;align-items:center;gap:6px;margin-top:8px;flex-wrap:wrap}
.em-pill{font-size:10px;padding:3px 9px;border-radius:20px;font-weight:700}
.em-case-time{font-size:10px;color:#666;margin-left:auto}

.em-capture-zone{border:2px dashed rgba(76,175,80,0.4);border-radius:18px;
  padding:40px 20px;text-align:center;background:#1a2e20;
  cursor:pointer;margin:12px 0}
.em-capture-title{font-size:15px;font-weight:600;color:#ccc;margin-top:10px}
.em-capture-sub{font-size:12px;color:#666;margin-top:4px}

.em-detect-success{background:rgba(76,175,80,0.12);border-left:4px solid #4caf50;
  padding:14px 16px;border-radius:12px;margin:12px 0;color:#a5d6a7}
.em-detect-warn{background:rgba(255,152,0,0.12);border-left:4px solid #ff9800;
  padding:14px 16px;border-radius:12px;margin:12px 0;color:#ffcc80}
.em-tip-box{background:rgba(33,150,243,0.1);border-left:4px solid #2196f3;
  padding:12px 14px;border-radius:12px;font-size:13px;color:#ccc;margin:8px 0}

.conf-Certain{background:rgba(76,175,80,0.2);color:#81c784}
.conf-Likely{background:rgba(255,193,7,0.2);color:#ffd54f}
.conf-Possible{background:rgba(158,158,158,0.2);color:#aaa}

.stTabs [data-baseweb="tab-list"]{background:#1a2e20!important;
  border-bottom:1px solid rgba(255,255,255,0.08)!important;gap:0!important;padding:0 16px!important}
.stTabs [data-baseweb="tab"]{padding:12px 14px!important;font-size:12px!important;
  font-weight:600!important;color:#666!important;border-bottom:2px solid transparent!important;
  font-family:'Inter',sans-serif!important}
.stTabs [aria-selected="true"]{color:#4caf50!important;
  border-bottom:2px solid #4caf50!important;background:transparent!important}
.stTabs [data-baseweb="tab-panel"]{background:#0a1410!important;padding:0!important}

.stButton>button{font-family:'Inter',sans-serif!important;font-weight:700!important;
  border-radius:28px!important;transition:all 0.2s!important;border:none!important}
.stButton>button[kind="primary"]{background:#1a7a4a!important;color:#fff!important}
.stButton>button:not([kind="primary"]){background:#1a2e20!important;color:#ccc!important;
  border:0.5px solid rgba(255,255,255,0.12)!important}

div[data-testid="stMetric"]{background:#1a2e20!important;border-radius:12px!important;
  padding:12px!important;border:0.5px solid rgba(255,255,255,0.07)!important}
div[data-testid="stMetricLabel"] p{color:#888!important;font-size:11px!important}
div[data-testid="stMetricValue"]{color:#eee!important}

.stTextInput input,.stTextArea textarea,.stNumberInput input{
  background:#1a2e20!important;border:0.5px solid rgba(255,255,255,0.12)!important;
  border-radius:10px!important;color:#eee!important;font-family:'Inter',sans-serif!important}
.stSelectbox>div>div{background:#1a2e20!important;
  border:0.5px solid rgba(255,255,255,0.12)!important;color:#eee!important}
label,.stRadio label p,.stSelectbox label{color:#aaa!important;
  font-family:'Inter',sans-serif!important;font-size:13px!important}
.stRadio [data-testid="stMarkdownContainer"] p{color:#aaa!important}

details,summary{background:#1a2e20!important;border-radius:12px!important;
  border:0.5px solid rgba(255,255,255,0.07)!important;color:#eee!important}
hr{border-color:rgba(255,255,255,0.08)!important}
.stProgress>div>div>div{background:#1a7a4a!important}
.stCaption,[data-testid="stCaptionContainer"] p{color:#666!important}
.stTable{background:#1a2e20!important}
thead tr th{background:#243828!important;color:#aaa!important}
tbody tr td{color:#ccc!important;border-color:rgba(255,255,255,0.06)!important}

.em-bottomnav{position:fixed;bottom:0;left:50%;transform:translateX(-50%);
  width:100%;max-width:480px;background:#0a1410;
  border-top:0.5px solid rgba(255,255,255,0.1);display:flex;z-index:9999;
  padding:0 0 env(safe-area-inset-bottom)}
.em-nav-item{flex:1;display:flex;flex-direction:column;align-items:center;
  gap:4px;padding:10px 4px 12px;cursor:pointer}
.em-nav-icon{width:24px;height:24px;opacity:0.4}
.em-nav-label{font-size:10px;color:#666;font-weight:600;font-family:'Inter',sans-serif}
.em-nav-item.active .em-nav-icon{opacity:1}
.em-nav-item.active .em-nav-label{color:#4caf50}
.em-nav-fab-wrap{flex:1;display:flex;flex-direction:column;align-items:center;
  gap:4px;padding:6px 4px 12px;cursor:pointer}
.em-nav-fab{width:50px;height:50px;border-radius:50%;background:#1a7a4a;
  display:flex;align-items:center;justify-content:center;margin-top:-14px;
  border:3px solid #0d1a12;box-shadow:0 4px 16px rgba(26,122,74,0.5)}
.em-nav-fab-label{font-size:10px;color:#4caf50;font-weight:700}

@media(max-width:360px){
  .em-hero-stats,.em-qa-grid{grid-template-columns:repeat(2,1fr)}
}

/* ── Mobile bottom nav — show only on small screens ── */
@media(max-width:640px){
  .em-bottomnav-mobile { display: flex !important; }
  .stTabs [data-baseweb="tab-list"] { display: none !important; }
}
@media(min-width:641px){
  .em-bottomnav-mobile { display: none !important; }
}

.em-qa-card { cursor: pointer; transition: transform 0.15s, opacity 0.15s; }
.em-qa-card:active { transform: scale(0.95); opacity: 0.8; }
</style>
<script>
// Attach click handlers to quick action cards and buttons
document.addEventListener('DOMContentLoaded', function(){
  setTimeout(function(){
    // Detect button (index 1)
    var detectBtns = document.querySelectorAll('[data-testid="stButton"] button[aria-label*="qa_detect"], [data-testid="stButton"] button[aria-label*="nav_detect"]');
    detectBtns.forEach(b => b.onclick = () => document.querySelectorAll('[data-baseweb="tab"]')[1].click());
    
    // Map button (index 2)
    var mapBtns = document.querySelectorAll('[data-testid="stButton"] button[aria-label*="nav_map"]');
    mapBtns.forEach(b => b.onclick = () => document.querySelectorAll('[data-baseweb="tab"]')[2].click());
    
    // Stats button (index 4)
    var statsBtns = document.querySelectorAll('[data-testid="stButton"] button[aria-label*="qa_stats"], [data-testid="stButton"] button[aria-label*="nav_stats"]');
    statsBtns.forEach(b => b.onclick = () => document.querySelectorAll('[data-baseweb="tab"]')[4].click());
    
    // Learn button (index 3)
    var learnBtns = document.querySelectorAll('[data-testid="stButton"] button[aria-label*="qa_learn"], [data-testid="stButton"] button[aria-label*="nav_learn"]');
    learnBtns.forEach(b => b.onclick = () => document.querySelectorAll('[data-baseweb="tab"]')[3].click());
    
    // Home button (index 0)
    var homeBtns = document.querySelectorAll('[data-testid="stButton"] button[aria-label*="nav_home"]');
    homeBtns.forEach(b => b.onclick = () => document.querySelectorAll('[data-baseweb="tab"]')[0].click());
  }, 300);
});
</script>
""", unsafe_allow_html=True)

WASTE_LABELS = {
    "plastic_bottle": "🍶 Plastic Bottle", "water_sachet": "💧 Water Sachet",
    "polythene_bag": "🛍️ Polythene Bag", "disposable": "🥤 Disposable",
    "waste_container": "🛢️ Waste Container",
}

ICON = {
    "home":   '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="CUR" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5L12 3l9 6.5V20a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9.5z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "map":    '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="CUR" stroke-width="2.2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "plus":   '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "stats":  '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="CUR" stroke-width="2.2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "learn":  '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="CUR" stroke-width="2.2" stroke-linecap="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    "bell":   '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    "search": '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
}

def get_icon(key, color="#4caf50"):
    return ICON[key].replace("CUR", color)


# ── LOGIN ─────────────────────────────────────────────────────────────────────
def show_login():
    st.markdown(f"""
    <div style="min-height:100vh;background:linear-gradient(160deg,#1a7a4a,#0a1410);
         display:flex;flex-direction:column;align-items:center;
         justify-content:center;padding:20px 16px;">
      <div style="text-align:center;">
        <div style="font-size:48px;margin-bottom:6px;">🌍</div>
        <div style="font-size:28px;font-weight:800;color:#fff;
             font-family:'Inter',sans-serif;margin-bottom:2px;">EarthMender AI</div>
        <div style="font-size:11px;color:rgba(255,255,255,0.55);
             font-family:'Inter',sans-serif;margin-bottom:28px;letter-spacing:1.5px;">
          DETECT · REPORT · LEARN · ACT
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown("""
        <div style="background:#1a2e20;border-radius:20px;padding:20px;
             border:0.5px solid rgba(255,255,255,0.08);">
          <div style="font-size:18px;font-weight:800;color:#eee;
               font-family:'Inter',sans-serif;margin-bottom:2px;">Welcome 👋</div>
          <div style="font-size:12px;color:#555;font-family:'Inter',sans-serif;
               margin-bottom:14px;">Demo mode — no account needed</div>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Your name", placeholder="e.g. Adeniji Yusuf")
        role = st.selectbox("I am a", [
            "Citizen — I want to report waste",
            "Operator — I manage waste collection",
        ])
        st.write("")
        if st.button("Enter EarthMender AI →", type="primary", use_container_width=True):
            if name.strip():
                parts = name.strip().split()
                st.session_state.update({
                    "logged_in": True,
                    "user_name": name.strip(),
                    "user_role": "Operator" if "Operator" in role else "Citizen",
                    "user_initials": ((parts[0][0]+parts[-1][0]).upper()
                                      if len(parts)>=2 else parts[0][:2].upper()),
                })
                st.rerun()
            else:
                st.warning("Please enter your name.")
        st.markdown("""
        <div style="text-align:center;margin-top:10px;font-size:11px;
             color:#444;font-family:'Inter',sans-serif;">
          🔒 Session only — no data stored permanently
        </div>
        """, unsafe_allow_html=True)

if not st.session_state.logged_in:
    show_login()
    st.stop()


# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_detector():
    return PlasticDetector()

detector    = get_detector()
all_reports = load_reports()
open_r      = get_open_reports()
resolved_r  = get_resolved_reports()
stats       = get_report_stats(all_reports)
high_open   = sum(1 for r in open_r if r.get("severity")=="HIGH")
total       = stats.get("total",0)
open_c      = stats.get("open",0)
resolved    = stats.get("resolved",0)
items       = stats.get("items",0)
rate        = f"{int(resolved/total*100)}%" if total>0 else "0%"
initials    = st.session_state.user_initials
uname       = st.session_state.user_name
role        = st.session_state.user_role

# ── TOP BAR ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="em-topbar">
  <div style="display:flex;align-items:center;gap:10px;">
    <div class="em-avatar">{initials}</div>
    <div>
      <div class="em-greeting">Welcome back,</div>
      <div class="em-username">{uname}</div>
    </div>
  </div>
  <div class="em-topbar-icons">
    <div class="em-icon-btn">{ICON['bell']}</div>
    <div class="em-icon-btn">{ICON['search']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tlabels = ["🏠 Home","🔍 Detect","🗺️ Map","📚 Learn","📊 Stats"]
if role=="Operator": tlabels.append("🏢 Ops")
tabs    = st.tabs(tlabels)
t_home,t_det,t_map,t_learn,t_stats = tabs[:5]
t_ops = tabs[5] if role=="Operator" else None


# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
with t_home:
    # Clear camera state when on home tab
    if "last_tab" not in st.session_state:
        st.session_state.last_tab = 0
    if st.session_state.last_tab != 0:
        st.session_state.captured_image = None
        st.session_state.detection_done = False
    st.session_state.last_tab = 0
    st.markdown(f"""
    <div class="em-hero">
      <div class="em-balance-card">
        <div class="em-balance-label">🛡️ Community Waste Reports</div>
        <div class="em-balance-val">{total} Cases</div>
      </div>
      <div class="em-hero-stats">
        <div class="em-hstat"><div class="em-hstat-val" style="color:#ffb74d;">{open_c}</div><div class="em-hstat-label">Open</div></div>
        <div class="em-hstat"><div class="em-hstat-val" style="color:#81c784;">{resolved}</div><div class="em-hstat-label">Resolved</div></div>
        <div class="em-hstat"><div class="em-hstat-val">{rate}</div><div class="em-hstat-label">Rate</div></div>
        <div class="em-hstat"><div class="em-hstat-val">{items}</div><div class="em-hstat-label">Items</div></div>
      </div>
    </div>
    <div class="em-page">
    """, unsafe_allow_html=True)

    if high_open>0:
        st.markdown(f"""
        <div class="em-alert">
          <div class="em-alert-dot"></div>
          <div class="em-alert-text">{high_open} HIGH severity case{'s' if high_open>1 else ''} need urgent attention</div>
          <div class="em-alert-cta">View →</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="em-section">
      <div class="em-section-header"><div class="em-section-title">Quick Actions</div></div>
      <div class="em-qa-grid" style="cursor:pointer;">
        <div class="em-qa-card" onclick="document.querySelectorAll('[data-baseweb=\\\"tab\\\"]')[1].click();"><div class="em-qa-icon" style="background:rgba(76,175,80,0.15);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#4caf50" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </div><div class="em-qa-label">Detect</div></div>
        <div class="em-qa-card" onclick="document.querySelectorAll('[data-baseweb=\\\"tab\\\"]')[2].click();"><div class="em-qa-icon" style="background:rgba(33,150,243,0.15);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2196f3" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        </div><div class="em-qa-label">Map</div></div>
        <div class="em-qa-card" onclick="document.querySelectorAll('[data-baseweb=\\\"tab\\\"]')[4].click();"><div class="em-qa-icon" style="background:rgba(255,152,0,0.15);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ff9800" stroke-width="2" stroke-linecap="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
        </div><div class="em-qa-label">Stats</div></div>
        <div class="em-qa-card" onclick="document.querySelectorAll('[data-baseweb=\\\"tab\\\"]')[3].click();"><div class="em-qa-icon" style="background:rgba(156,39,176,0.15);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#9c27b0" stroke-width="2" stroke-linecap="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        </div><div class="em-qa-label">Learn</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    qa_col1, qa_col2, qa_col3, qa_col4 = st.columns(4)
    with qa_col1:
        if st.button("🔍", key="qa_detect", use_container_width=True, help="Detect waste"):
            pass
    with qa_col2:
        if st.button("🗺️", key="qa_map", use_container_width=True, help="View map"):
            pass
    with qa_col3:
        if st.button("📊", key="qa_stats", use_container_width=True, help="View stats"):
            pass
    with qa_col4:
        if st.button("📚", key="qa_learn", use_container_width=True, help="Learn"):
            pass

    if st.button("📸 Report Waste Now", type="primary", use_container_width=True):
        st.session_state.active_tab = 1
        st.rerun()

    # Recent reports section
    if "show_all_reports" not in st.session_state:
        st.session_state.show_all_reports = False

    col_title, col_action = st.columns([1, 1])
    with col_title:
        st.markdown("""
        <div class="em-section">
          <div class="em-section-title">Recent Reports</div>
        </div>
        """, unsafe_allow_html=True)
    with col_action:
        if st.button("See all" if not st.session_state.show_all_reports else "See less",
                     key="toggle_all_reports", use_container_width=True):
            st.session_state.show_all_reports = not st.session_state.show_all_reports
            st.rerun()

    num_reports = len(all_reports) if st.session_state.show_all_reports else 5
    recent = sorted(all_reports, key=lambda x: x.get("timestamp",""), reverse=True)[:num_reports]
    if not recent:
        st.info("No reports yet — be the first!")
    else:
        for r in recent:
            sev    = r.get("severity","LOW")
            status = r.get("status","OPEN")
            dot_c  = {"HIGH":"#f44336","MEDIUM":"#ff9800","LOW":"#4caf50"}.get(sev,"#4caf50")
            types  = ", ".join(WASTE_LABELS.get(t,t) for t in r.get("waste_types",[]))
            desc   = r.get("description","") or r.get("date","")
            sp_sev = {"HIGH":"background:rgba(244,67,54,0.2);color:#ef9a9a;",
                      "MEDIUM":"background:rgba(255,152,0,0.2);color:#ffcc80;",
                      "LOW":"background:rgba(76,175,80,0.2);color:#a5d6a7;"}.get(sev,"")
            sp_sta = ("background:rgba(255,152,0,0.15);color:#ffcc80;"
                      if status=="OPEN"
                      else "background:rgba(76,175,80,0.15);color:#a5d6a7;")
            st.markdown(f"""
            <div class="em-case-card">
              <div class="em-case-dot" style="background:{dot_c};"></div>
              <div style="flex:1;min-width:0;">
                <div class="em-case-type">{types}</div>
                <div class="em-case-loc">{str(desc)[:55]}</div>
                <div class="em-case-meta">
                  <span class="em-pill" style="{sp_sev}">{sev}</span>
                  <span class="em-pill" style="{sp_sta}">{status}</span>
                  <span class="em-case-time">{r.get('time','')}</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # Live mini map
    col_map_title, col_map_action = st.columns([1, 1])
    with col_map_title:
        st.markdown("""
        <div class="em-section">
          <div class="em-section-title">🗺️ Pollution Map</div>
        </div>
        """, unsafe_allow_html=True)
    with col_map_action:
        if st.button("Open full →", key="open_full_map", use_container_width=True):
            st.session_state.active_tab = 2
            st.rerun()

    mini_map = build_map(open_r[:20] if open_r else [], all_reports=all_reports)
    st_folium(mini_map, width=None, height=200, returned_objects=[], key="home_mini_map")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DETECT
# ══════════════════════════════════════════════════════════════════════════════
with t_det:
    # Track that we're on detect tab
    st.session_state.last_tab = 1
    st.markdown('<div class="em-page">', unsafe_allow_html=True)
    
    # Initialize camera session state if needed
    if "detect_mode" not in st.session_state:
        st.session_state.detect_mode = "📷 Camera"
    
    st.markdown("""
    <div class="em-section">
      <div class="em-section-title">📸 Detect Plastic Waste</div>
      <div style="font-size:12px;color:#666;margin-top:4px;">
        Upload or capture — AI identifies waste and logs a geo-tagged report
      </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Source", ["📷 Camera","📁 Upload"],
                    horizontal=True, label_visibility="collapsed",
                    key="detect_source_mode")
    if mode != st.session_state.get("detect_mode"):
        st.session_state.detect_mode = mode

    # Capture UI — only when no detection done yet
    if not st.session_state.detection_done:
        if mode == "📷 Camera":
            st.markdown("""
            <div class="em-capture-zone">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
                   stroke="#4caf50" stroke-width="1.5" stroke-linecap="round">
                <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                <circle cx="12" cy="13" r="4"/>
              </svg>
              <div class="em-capture-title">Point camera at the waste</div>
              <div class="em-capture-sub">Hold steady for best results</div>
            </div>
            """, unsafe_allow_html=True)
            cap = st.camera_input("", label_visibility="collapsed")
            if cap:
                st.session_state.captured_image = Image.open(cap).convert("RGB")
        else:
            st.markdown("""
            <div class="em-capture-zone">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
                   stroke="#4caf50" stroke-width="1.5" stroke-linecap="round">
                <polyline points="16 16 12 12 8 16"/><line x1="12" y1="12" x2="12" y2="21"/>
                <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/>
              </svg>
              <div class="em-capture-title">Tap to upload a photo</div>
              <div class="em-capture-sub">JPG, PNG, WEBP · Max 10MB</div>
            </div>
            """, unsafe_allow_html=True)
            upl = st.file_uploader("", type=["jpg","jpeg","png","webp"],
                                   label_visibility="collapsed")
            if upl:
                st.session_state.captured_image = Image.open(upl).convert("RGB")

    # Show original ONLY before detection
    if st.session_state.captured_image and not st.session_state.detection_done:
        st.image(st.session_state.captured_image,
                 caption="Ready for analysis", width=350)

    # Show annotated ONLY after detection (no duplicate)
    if st.session_state.detection_done:
        if st.session_state.annotated_img:
            st.image(st.session_state.annotated_img,
                     caption="Detection result", width=400)

        q = st.session_state.quality or {}
        if q.get("quality")=="poor":
            st.markdown(f'<div class="em-detect-warn">⚠️ {q.get("message","")}</div>',
                        unsafe_allow_html=True)

        dets = st.session_state.detections
        if dets:
            st.markdown(f'<div class="em-detect-success">✅ Detected <b>{len(dets)}</b> waste item(s)</div>',
                        unsafe_allow_html=True)
            seen = set()
            for det in dets:
                if det["label"] not in seen:
                    seen.add(det["label"])
                    lbl  = WASTE_LABELS.get(det["label"], det["label"].replace("_"," ").title())
                    band = det.get("confidence_band","Possible")
                    conf = det["confidence"]
                    st.markdown(
                        f'<div class="em-tip-box"><b style="color:#90caf9;">{lbl}</b> &nbsp;'
                        f'<span class="em-pill conf-{band}" style="font-size:10px;'
                        f'padding:2px 8px;border-radius:20px;">{band} {conf:.0%}</span><br>'
                        f'<span style="color:#888;font-size:12px;">{det["tip"]}</span></div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="em-detect-warn">⚠️ No plastic waste detected.<br>'
                '<span style="font-size:12px;color:#aaa;">Try better lighting or '
                'move closer.</span></div>', unsafe_allow_html=True)

        if st.button("🔄 Scan Another", use_container_width=True):
            for k in ["captured_image","detection_done","annotated_img","detections","quality"]:
                st.session_state[k] = None if k!="detection_done" else False
                if k in ["detections"]: st.session_state[k] = []
            st.rerun()

    # Location + submit
    if st.session_state.captured_image and not st.session_state.detection_done:
        st.markdown("---")
        st.markdown('<div style="font-size:14px;font-weight:700;color:#eee;'
                    'margin-bottom:10px;">📍 Location</div>', unsafe_allow_html=True)

        lm = st.radio("Loc", ["🌐 Auto GPS","✏️ Manual"],
                      horizontal=True, label_visibility="collapsed")
        lat, lon = 6.5244, 3.3792
        if lm=="🌐 Auto GPS":
            render_gps_capture()
            lat, lon = get_gps_coords_from_inputs()
        else:
            lat, lon = get_manual_location()

        desc = st.text_area("📝 Location description (optional)",
                            placeholder="e.g. Near Ojota bus stop, beside the drainage",
                            max_chars=200)
        st.write("")

        if st.button("🔍 Analyse & Submit Report", type="primary", use_container_width=True):
            with st.spinner("🌍 Analysing for plastic waste..."):
                ann, dets, qual = detector.detect_from_image(st.session_state.captured_image)
                st.session_state.annotated_img  = ann
                st.session_state.detections     = dets
                st.session_state.quality        = qual
                st.session_state.detection_done = True
                if dets:
                    save_report(dets, lat=lat, lon=lon, description=desc,
                                reporter_name=uname)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAP
# ══════════════════════════════════════════════════════════════════════════════
with t_map:
    # Clear camera state when on map tab
    if st.session_state.last_tab != 2:
        st.session_state.captured_image = None
        st.session_state.detection_done = False
    st.session_state.last_tab = 2
    st.markdown('<div class="em-page">', unsafe_allow_html=True)
    st.markdown("""
    <div class="em-section">
      <div class="em-section-title">🗺️ Live Pollution Map</div>
      <div style="font-size:12px;color:#666;margin-top:4px;margin-bottom:12px;">
        Heatmap weighted by severity, recurrence and time decay
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    c1.metric("Total",    len(all_reports))
    c2.metric("Open",     len(open_r))
    c3.metric("Resolved", len(resolved_r))

    mf = st.radio("Show",["All","Open Only","Resolved Only"],horizontal=True)
    md = (open_r if mf=="Open Only" else
          resolved_r if mf=="Resolved Only" else all_reports)

    pm = build_map(md, all_reports=all_reports)
    st_folium(pm, width=None, height=460, returned_objects=[], key="map_full_map")

    if open_r:
        hs = get_hotspots(open_r)
        if hs:
            st.markdown('<div style="font-size:14px;font-weight:700;color:#eee;'
                        'margin-top:16px;margin-bottom:10px;">🔥 Active Hotspots</div>',
                        unsafe_allow_html=True)
            for i,h in enumerate(hs[:3],1):
                osm = f"https://www.openstreetmap.org/?mlat={h['lat']}&mlon={h['lon']}&zoom=16"
                st.markdown(f"**#{i}** `{h['lat']:.3f},{h['lon']:.3f}` — "
                            f"{h['count']} report(s) · {h['items']} items · [📍 Map]({osm})")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LEARN
# ══════════════════════════════════════════════════════════════════════════════
with t_learn:
    # Clear camera state when on learn tab
    if st.session_state.last_tab != 3:
        st.session_state.captured_image = None
        st.session_state.detection_done = False
    st.session_state.last_tab = 3
    render_education_tab()


# ══════════════════════════════════════════════════════════════════════════════
# STATS
# ══════════════════════════════════════════════════════════════════════════════
with t_stats:
    # Clear camera state when on stats tab
    if st.session_state.last_tab != 4:
        st.session_state.captured_image = None
        st.session_state.detection_done = False
    st.session_state.last_tab = 4
    render_full_dashboard(
        get_report_stats(load_reports()),
        get_hotspots(load_reports()),
        load_reports()
    )


# ══════════════════════════════════════════════════════════════════════════════
# OPS
# ══════════════════════════════════════════════════════════════════════════════
if t_ops:
    with t_ops:
        # Clear camera state when on ops tab
        if st.session_state.last_tab != 5:
            st.session_state.captured_image = None
            st.session_state.detection_done = False
        st.session_state.last_tab = 5
        st.markdown('<div class="em-page">', unsafe_allow_html=True)
        st.markdown('<div class="em-section"><div class="em-section-title">🏢 Operator Dashboard</div></div>',
                    unsafe_allow_html=True)
        oc = get_open_reports()
        rc = get_resolved_reports()
        tc = len(oc)+len(rc)
        k1,k2,k3 = st.columns(3)
        k1.metric("Open",    len(oc))
        k2.metric("Resolved",len(rc))
        k3.metric("Rate",    f"{int(len(rc)/tc*100)}%" if tc else "0%")
        st.divider()

        sf = st.selectbox("Filter",["All","HIGH","MEDIUM","LOW"])
        so = st.radio("Sort",["Severity first","Newest first"],horizontal=True)
        fl = oc if sf=="All" else [r for r in oc if r.get("severity")==sf]
        fl = (sorted(fl,key=lambda x:{"HIGH":0,"MEDIUM":1,"LOW":2}.get(x.get("severity"),3))
              if so=="Severity first"
              else sorted(fl,key=lambda x:x.get("timestamp",""),reverse=True))

        st.markdown(f"#### 🟠 Open ({len(fl)})")
        if not fl:
            st.success("No open cases!")
        for r in fl:
            sev   = r.get("severity","LOW")
            types = ", ".join(WASTE_LABELS.get(t,t) for t in r.get("waste_types",[]))
            icon  = {"HIGH":"🔴","MEDIUM":"🟡","LOW":"🟢"}.get(sev,"🟢")
            osm   = f"https://www.openstreetmap.org/?mlat={r['latitude']}&mlon={r['longitude']}&zoom=17"
            with st.expander(f"{icon} #{r['id']} — {sev} — {types}",
                             expanded=(sev=="HIGH")):
                c1,c2 = st.columns([2,1])
                with c1:
                    st.write(f"**Waste:** {types}")
                    st.write(f"**Reporter:** {r.get('reporter','Anonymous')}")
                    if r.get("description"): st.write(f"**Location:** {r['description']}")
                with c2:
                    st.code(f"{r['latitude']:.5f}\n{r['longitude']:.5f}")
                    st.markdown(f"[📍 Map]({osm})")
                note = st.text_input(f"Note #{r['id']}",
                                     value="Area cleaned.",key=f"note_{r['id']}")
                if st.button(f"✅ Resolve #{r['id']}",
                             key=f"res_{r['id']}",type="primary"):
                    if resolve_report(r["id"],resolved_by=uname,note=note):
                        st.success("Resolved!")
                        st.rerun()

        st.divider()
        st.markdown(f"#### ✅ Resolved ({len(rc)})")
        for r in sorted(rc,key=lambda x:x.get("resolved_at",""),reverse=True)[:8]:
            types = ", ".join(WASTE_LABELS.get(t,t) for t in r.get("waste_types",[]))
            rd    = (r.get("resolved_at") or "")[:10]
            with st.expander(f"✅ #{r['id']} — {types} — {rd}"):
                st.write(f"**By:** {r.get('resolved_by','Operator')}")
                st.write(f"**Note:** {r.get('resolution_note','—')}")
                if st.button(f"↩️ Reopen #{r['id']}",key=f"reopen_{r['id']}"):
                    reopen_report(r["id"])
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# ── FIXED BOTTOM NAV — Mobile only, mapped to tab clicks ──────────────────────
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("🏠", key="nav_home", use_container_width=True):
        st.session_state.captured_image = None
        st.session_state.detection_done = False
        pass

with nav_col2:
    if st.button("🔍", key="nav_detect", use_container_width=True):
        pass

with nav_col3:
    if st.button("🗺️", key="nav_map", use_container_width=True):
        pass

with nav_col4:
    if st.button("📊", key="nav_stats", use_container_width=True):
        pass

with nav_col5:
    if st.button("📚", key="nav_learn", use_container_width=True):
        pass

st.markdown('<div class="em-bottomnav-mobile"><!-- Mobile nav --></div><div style="height:80px;"></div>', unsafe_allow_html=True)
