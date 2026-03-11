
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zerve User Success Analysis", layout="wide")
st.title("🏆 Zerve User Success Analysis")
st.markdown("**What behaviors drive upgrades? — by Dhanashree Bansode**")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", "4,774")
col2.metric("Upgrade Rate", "0.8%", "38 users")
col3.metric("Wall Churners", "87", "89.7% lost at wall")
col4.metric("Model AUC", "0.998", "GBM Classifier")
st.divider()

st.subheader("User Segment Behavioral Comparison")
df_display = pd.DataFrame({
    "Avg Total Events": [1027, 5644, 1041],
    "Avg Agent Completions": [14, 105, 35],
    "Fullscreen Usage %": [13, 40, 36],
    "Avg Unique Event Types": [24, 33, 28]
}, index=["Wall Churners (87)","Wall Upgraders (10)","Value Upgraders (28)"])
st.dataframe(df_display, use_container_width=True)

st.subheader("Credit Exhaustion Funnel")
funnel = pd.DataFrame({
    "Stage": ["credits_below_4","credits_below_3","credits_below_2",
              "credits_below_1","credits_exceeded","addon_credits_used"],
    "Users": [213, 229, 111, 127, 97, 38]
})
st.bar_chart(funnel.set_index("Stage"))
st.divider()

st.subheader("Key Findings")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Finding 1 — Two Upgrade Paths**\n\n73% upgraded from value (never hit wall). 27% upgraded after exhaustion.")
with col2:
    st.success("**Finding 2 — Agent Completions = #1 Signal**\n\nGBM importance: 0.391. Wall upgraders completed 7.4x more agent tasks than churners.")
with col3:
    st.error("**Finding 3 — 87 Users Are a Revenue Leak**\n\n70% of wall upgraders converted within 24 hrs. The 87 churners didn't get that nudge.")
st.divider()

st.subheader("🔮 Upgrade Risk Scorer")
st.markdown("Enter a user profile to predict upgrade likelihood:")
col1, col2 = st.columns(2)
with col1:
    completions = st.slider("Agent Task Completions", 0, 200, 14)
    events = st.slider("Total Events", 0, 6000, 500)
with col2:
    chats = st.slider("Agent Chats Started", 0, 100, 5)
    exceeded = st.checkbox("Hit credits_exceeded?")

score = min((completions * 0.391 + events * 0.000367 + chats * 0.083) / 50, 1.0)
if completions >= 50 and events >= 3000:
    segment = "🟡 Wall Upgrader — send upgrade prompt now"
elif completions >= 20:
    segment = "🟢 Value Upgrader — highlight advanced features"
elif exceeded and completions < 20:
    segment = "🔴 Wall Churner — intervene with bonus credits"
else:
    segment = "⚪ Free / Disengaged — onboarding nudge"

st.metric("Upgrade Score", f"{score:.2f} / 1.00")
st.markdown(f"**Predicted Segment:** {segment}")
