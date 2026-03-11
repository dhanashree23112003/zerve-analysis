import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Zerve User Success Analysis",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS that actually works on Streamlit Cloud
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Mono&display=swap');

.main { background-color: #080810; }
.stApp { background-color: #080810; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: #f0f0fa !important; }
p, li, label { color: #9999bb !important; }

#MainMenu, footer, header { visibility: hidden; }

.metric-box {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 24px 20px;
    text-align: center;
    margin-bottom: 8px;
}
.metric-box .val {
    font-family: 'Syne', sans-serif;
    font-size: 42px;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-box .lbl {
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b6b8a;
}
.metric-box .sub {
    font-size: 12px;
    margin-top: 4px;
    color: #6b6b8a;
}

.seg-card {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 24px;
    height: 100%;
}
.seg-card .seg-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 4px;
}
.seg-card .seg-sub {
    font-size: 11px;
    color: #6b6b8a;
    margin-bottom: 16px;
    letter-spacing: 0.08em;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    padding: 7px 0;
    border-bottom: 1px solid #1a1a2e;
    font-size: 12px;
}
.stat-row .sk { color: #6b6b8a; }
.stat-row .sv { font-weight: 600; }

.finding-card {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 28px;
    margin-bottom: 12px;
}
.finding-card .fn { font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 8px; }
.finding-card .ft { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; color: #f0f0fa; margin-bottom: 10px; }
.finding-card .fb { font-size: 13px; color: #9999bb; line-height: 1.7; }
.finding-card .fb strong { color: #f0f0fa; }

.score-box {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 32px;
    text-align: center;
    margin-top: 16px;
}
.score-val {
    font-family: 'Syne', sans-serif;
    font-size: 80px;
    font-weight: 800;
    line-height: 1;
}
.score-seg {
    display: inline-block;
    padding: 8px 20px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 600;
    margin-top: 16px;
}

.divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 36px 0;
}
.section-label {
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────
st.markdown("""
<div style="padding: 40px 0 32px;">
  <div style="font-size:10px; letter-spacing:0.25em; text-transform:uppercase; 
              color:#6366f1; border:1px solid rgba(99,102,241,0.3); 
              display:inline-block; padding:5px 14px; border-radius:3px; margin-bottom:20px;">
    Zerve · $10,000 Data Challenge
  </div>
  <h1 style="font-size:52px; font-weight:800; line-height:1.1; margin:0 0 12px;">
    What Drives<br><span style="color:#6366f1;">Successful Usage?</span>
  </h1>
  <p style="font-size:13px; color:#6b6b8a; margin:0;">
    409,287 events &nbsp;·&nbsp; 4,774 users &nbsp;·&nbsp; by Dhanashree Bansode &nbsp;·&nbsp; March 2026
  </p>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── METRICS ───────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (c1, "4,774", "Total Users", "409K events analyzed", "#6366f1"),
    (c2, "0.8%",  "Upgrade Rate", "38 of 4,774 users", "#22d3ee"),
    (c3, "87",    "Revenue Leak", "engaged users lost at wall", "#f43f5e"),
    (c4, "0.998", "Model AUC", "GBM Classifier", "#a3e635"),
]
for col, val, lbl, sub, color in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-box">
          <div class="val" style="color:{color};">{val}</div>
          <div class="lbl">{lbl}</div>
          <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── SEGMENTS ──────────────────────────────────────────────
st.markdown('<div class="section-label">01 — User Segments</div>', unsafe_allow_html=True)
st.markdown("## Three Types of Users Emerged")

c1, c2, c3 = st.columns(3)
segments = [
    (c1, "🔴", "Wall Churners", "87 users · hit limit, left", "#f43f5e",
     [("Avg Events","1,027"),("Agent Completions","14"),
      ("Fullscreen Usage","13%"),("Median hrs to wall","1.3 hrs"),("Outcome","89.7% churned")]),
    (c2, "🟡", "Wall Upgraders", "10 users · hit limit, paid", "#f59e0b",
     [("Avg Events","5,644"),("Agent Completions","105"),
      ("Fullscreen Usage","40%"),("Median hrs to wall","3.4 hrs"),("Outcome","70% in <24hrs")]),
    (c3, "🟢", "Value Upgraders", "28 users · never hit wall", "#22d3ee",
     [("Avg Events","1,041"),("Agent Completions","35"),
      ("Fullscreen Usage","36%"),("Upgraded proactively","Yes"),("Outcome","73% of upgrades")]),
]
for col, icon, name, sub, color, stats in segments:
    with col:
        stats_html = "".join([
            f'<div class="stat-row"><span class="sk">{k}</span><span class="sv" style="color:{color};">{v}</span></div>'
            for k, v in stats
        ])
        st.markdown(f"""
        <div class="seg-card" style="border-top: 3px solid {color};">
          <div style="font-size:28px; margin-bottom:10px;">{icon}</div>
          <div class="seg-title" style="color:{color};">{name}</div>
          <div class="seg-sub">{sub}</div>
          {stats_html}
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── FUNNEL (Plotly) ───────────────────────────────────────
st.markdown('<div class="section-label">02 — Credit Exhaustion Funnel</div>', unsafe_allow_html=True)
st.markdown("## Where Users Drop Off")

funnel_labels = ["credits_below_4","credits_below_3","credits_below_2",
                 "credits_below_1","credits_exceeded","addon_credits_used"]
funnel_values = [213, 229, 111, 127, 97, 38]
funnel_colors = ["#6366f1","#818cf8","#a78bfa","#f59e0b","#f43f5e","#22d3ee"]

fig_funnel = go.Figure(go.Bar(
    x=funnel_values,
    y=funnel_labels,
    orientation='h',
    marker_color=funnel_colors,
    text=[f"{v} users" for v in funnel_values],
    textposition='outside',
    textfont=dict(color='#f0f0fa', size=12),
))
fig_funnel.update_layout(
    paper_bgcolor='#080810',
    plot_bgcolor='#0d0d1a',
    height=300,
    margin=dict(l=20, r=80, t=20, b=20),
    xaxis=dict(color='#6b6b8a', gridcolor='#1e1e2e', showgrid=True),
    yaxis=dict(color='#f0f0fa', gridcolor='#1e1e2e'),
    font=dict(family='DM Mono', color='#f0f0fa'),
)
st.plotly_chart(fig_funnel, use_container_width=True)

st.markdown("""
<div style="background:#0d0010; border:1px solid rgba(244,63,94,0.3); border-radius:8px; 
            padding:14px 20px; font-size:13px; color:#f43f5e; margin-bottom:8px;">
  ⚠️ <strong>89.7% of users who hit the credit wall churned.</strong>
  <span style="color:#9999bb;"> Only 10 of 97 upgraded. The 87 who left averaged 1,027 events — not beginners.</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── BEHAVIORAL GAP (Plotly) ───────────────────────────────
st.markdown('<div class="section-label">03 — Behavioral Gap</div>', unsafe_allow_html=True)
st.markdown("## What Separates Each Segment")

categories = ['Avg Events (÷10)', 'Agent Completions', 'Fullscreen %']
fig_gap = go.Figure()
seg_data = [
    ("Wall Churners", [1027/10, 14, 13], "#f43f5e"),
    ("Wall Upgraders", [5644/10, 105, 40], "#f59e0b"),
    ("Value Upgraders", [1041/10, 35, 36], "#22d3ee"),
]
for name, vals, color in seg_data:
    fig_gap.add_trace(go.Bar(name=name, x=categories, y=vals,
                             marker_color=color, marker_line_width=0))

fig_gap.update_layout(
    barmode='group',
    paper_bgcolor='#080810',
    plot_bgcolor='#0d0d1a',
    height=360,
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(bgcolor='#0d0d1a', bordercolor='#1e1e2e', font=dict(color='#f0f0fa')),
    xaxis=dict(color='#f0f0fa', gridcolor='#1e1e2e'),
    yaxis=dict(color='#6b6b8a', gridcolor='#1e1e2e'),
    font=dict(family='DM Mono', color='#f0f0fa'),
)
st.plotly_chart(fig_gap, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── FEATURE IMPORTANCE (Plotly) ───────────────────────────
st.markdown('<div class="section-label">04 — Model</div>', unsafe_allow_html=True)
st.markdown("## What Predicts Upgrade? — GBM Feature Importance")

features = ['fullscreen','credits_exceeded','refactor','get_block','run_blocks',
            'unique_event_types','agent_completion_rate','agent_chats',
            'total_events','agent_completions']
importances = [0.002, 0.011, 0.016, 0.018, 0.020, 0.046, 0.046, 0.083, 0.367, 0.391]
colors_fi = ['#22d3ee' if v > 0.1 else '#6366f1' for v in importances]

fig_fi = go.Figure(go.Bar(
    x=importances, y=features, orientation='h',
    marker_color=colors_fi,
    text=[f"{v:.3f}" for v in importances],
    textposition='outside',
    textfont=dict(color='#f0f0fa', size=11),
))
fig_fi.update_layout(
    paper_bgcolor='#080810',
    plot_bgcolor='#0d0d1a',
    height=340,
    margin=dict(l=20, r=60, t=20, b=20),
    xaxis=dict(color='#6b6b8a', gridcolor='#1e1e2e', title='Feature Importance', title_font=dict(color='#6b6b8a')),
    yaxis=dict(color='#f0f0fa', gridcolor='#1e1e2e'),
    font=dict(family='DM Mono', color='#f0f0fa'),
)
st.plotly_chart(fig_fi, use_container_width=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── FINDINGS ──────────────────────────────────────────────
st.markdown('<div class="section-label">05 — Key Findings</div>', unsafe_allow_html=True)
st.markdown("## Three Findings That Matter")

findings = [
    ("#6366f1", "01", "Two Upgrade Paths, Not One",
     "<strong>73%</strong> of upgraders never hit the credit wall — they paid because they saw value. Only <strong>27%</strong> upgraded after exhaustion. These groups need completely different product interventions."),
    ("#22d3ee", "02", "Agent Completions = #1 Predictor",
     "GBM feature importance: <strong>0.391</strong>. Wall upgraders completed <strong>7.4×</strong> more agent tasks than churners. Hitting the credit wall ranks last at <strong>0.011</strong> — nearly irrelevant."),
    ("#f43f5e", "03", "87 Users Are a Revenue Leak",
     "Engaged users who burned through credits and silently left. <strong>70%</strong> of wall upgraders converted within 24 hours — intent is immediate. The 87 churners just didn't get the nudge."),
]
for color, num, title, body in findings:
    st.markdown(f"""
    <div class="finding-card" style="border-left: 3px solid {color};">
      <div class="fn" style="color:{color};">Finding {num}</div>
      <div class="ft">{title}</div>
      <div class="fb">{body}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── UPGRADE SCORER ────────────────────────────────────────
st.markdown('<div class="section-label">06 — Live Tool</div>', unsafe_allow_html=True)
st.markdown("## 🔮 Upgrade Risk Scorer")
st.markdown('<p style="color:#9999bb; font-size:13px;">Enter a user profile to predict upgrade likelihood and intervention.</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    completions = st.slider("Agent Task Completions", 0, 200, 14)
    events = st.slider("Total Events", 0, 6000, 500)
with c2:
    chats = st.slider("Agent Chats Started", 0, 100, 5)
    exceeded = st.checkbox("Hit credits_exceeded?")

score = min((completions * 0.391 + events * 0.000367 + chats * 0.083) / 50, 1.0)
score_pct = int(score * 100)

if completions >= 50 and events >= 3000:
    seg, seg_color, seg_bg = "🟡 Wall Upgrader — send upgrade prompt now", "#f59e0b", "rgba(245,158,11,0.12)"
elif completions >= 20:
    seg, seg_color, seg_bg = "🟢 Value Upgrader — highlight advanced features", "#22d3ee", "rgba(34,211,238,0.12)"
elif exceeded and completions < 20:
    seg, seg_color, seg_bg = "🔴 Wall Churner — intervene with bonus credits", "#f43f5e", "rgba(244,63,94,0.12)"
else:
    seg, seg_color, seg_bg = "⚪ Free / Disengaged — onboarding nudge", "#9999bb", "rgba(153,153,187,0.1)"

score_color = "#22d3ee" if score >= 0.6 else "#f59e0b" if score >= 0.3 else "#f43f5e"

st.markdown(f"""
<div class="score-box">
  <div style="font-size:11px; letter-spacing:0.2em; text-transform:uppercase; color:#6b6b8a; margin-bottom:8px;">Upgrade Score</div>
  <div class="score-val" style="color:{score_color};">{score:.2f}</div>
  <div style="font-size:11px; color:#6b6b8a; margin-top:4px;">out of 1.00</div>
  <div class="score-seg" style="color:{seg_color}; background:{seg_bg}; border:1px solid {seg_color}44; margin-top:20px;">
    {seg}
  </div>
</div>
""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("""
<hr class="divider">
<div style="display:flex; justify-content:space-between; align-items:center; padding-bottom:24px;">
  <div>
    <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; color:#f0f0fa;">Dhanashree Bansode</div>
    <div style="font-size:11px; color:#6b6b8a; margin-top:4px;">Zerve $10,000 Data Challenge · March 2026</div>
  </div>
  <div style="text-align:right; font-size:11px; color:#6b6b8a;">
    GBM · AUC 0.998 · 409K events · 4,774 users
  </div>
</div>
""", unsafe_allow_html=True)
