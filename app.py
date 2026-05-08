# ============================================================
# TrendCompass — Streamlit App
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="TrendCompass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS — dark editorial theme ────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

  html, body, [data-testid="stAppViewContainer"] {
      background-color: #0C0E14 !important;
      color: #E8E6E0 !important;
  }
  [data-testid="stAppViewContainer"] > .main {
      background-color: #0C0E14 !important;
  }
  [data-testid="block-container"] {
      padding: 2.5rem 3rem 4rem 3rem !important;
      max-width: 1280px;
  }
  h1, h2, h3 { font-family: 'DM Serif Display', Georgia, serif !important; }
  p, div, span, label { font-family: 'DM Sans', sans-serif !important; }

  .tc-header {
      display: flex;
      align-items: baseline;
      gap: 16px;
      border-bottom: 1px solid #1E2130;
      padding-bottom: 18px;
      margin-bottom: 32px;
  }
  .tc-wordmark {
      font-family: 'DM Serif Display', serif;
      font-size: 2.4rem;
      font-style: italic;
      color: #F0EDE6;
      letter-spacing: -0.5px;
      line-height: 1;
  }
  .tc-tagline {
      font-family: 'DM Mono', monospace;
      font-size: 0.72rem;
      color: #4A5068;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      padding-bottom: 4px;
  }
  .tc-compass {
      margin-left: auto;
      font-size: 1.9rem;
      opacity: 0.55;
  }

  .metric-row {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin-bottom: 28px;
  }
  .metric-card {
      background: #12141D;
      border: 1px solid #1C1F2E;
      border-radius: 10px;
      padding: 18px 22px;
      position: relative;
      overflow: hidden;
  }
  .metric-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; right: 0;
      height: 2px;
  }
  .metric-card.blue::before  { background: #4B8EF1; }
  .metric-card.red::before   { background: #E05B5B; }
  .metric-card.gold::before  { background: #C9A84C; }
  .metric-label {
      font-family: 'DM Mono', monospace;
      font-size: 0.68rem;
      color: #4A5068;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 8px;
  }
  .metric-value {
      font-family: 'DM Serif Display', serif;
      font-size: 2rem;
      color: #F0EDE6;
      line-height: 1;
  }
  .metric-sub {
      font-family: 'DM Sans', sans-serif;
      font-size: 0.75rem;
      color: #525870;
      margin-top: 5px;
  }

  [data-testid="stSelectbox"] > div > div {
      background-color: #12141D !important;
      border: 1px solid #1C1F2E !important;
      border-radius: 8px !important;
      color: #E8E6E0 !important;
      font-family: 'DM Sans', sans-serif !important;
  }
  [data-testid="stSelectbox"] label {
      color: #7A8099 !important;
      font-family: 'DM Mono', monospace !important;
      font-size: 0.72rem !important;
      text-transform: uppercase !important;
      letter-spacing: 0.1em !important;
  }

  .chart-wrap {
      background: #10121A;
      border: 1px solid #1C1F2E;
      border-radius: 12px;
      padding: 8px;
      margin-bottom: 24px;
  }

  [data-testid="stAlert"] {
      border-radius: 10px !important;
      font-family: 'DM Sans', sans-serif !important;
      font-size: 0.92rem !important;
      border-left-width: 3px !important;
  }

  .insight-box {
      background: #12141D;
      border: 1px solid #1C1F2E;
      border-radius: 10px;
      padding: 22px 26px;
      margin-top: 20px;
  }
  .insight-title {
      font-family: 'DM Serif Display', serif;
      font-size: 1.1rem;
      color: #C9A84C;
      margin-bottom: 10px;
  }
  .insight-body {
      font-family: 'DM Sans', sans-serif;
      font-size: 0.87rem;
      color: #7A8099;
      line-height: 1.7;
  }

  .tc-footer {
      margin-top: 48px;
      padding-top: 18px;
      border-top: 1px solid #1C1F2E;
      font-family: 'DM Mono', monospace;
      font-size: 0.68rem;
      color: #2E3248;
      text-align: center;
      letter-spacing: 0.08em;
  }

  #MainMenu, footer, header { visibility: hidden; }
  [data-testid="stToolbar"]  { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/precomputed_cases.csv", parse_dates=["Date"])
    return df

df = load_data()
keywords = sorted(df["Keyword"].unique().tolist())

# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="tc-header">
  <div class="tc-wordmark">TrendCompass</div>
  <div class="tc-tagline">Cultural Trend Intelligence · Sentiment Index Dashboard</div>
  <div class="tc-compass">🧭</div>
</div>
""", unsafe_allow_html=True)

# ── Selector ─────────────────────────────────────────────────
col_sel, col_pad = st.columns([1, 3])
with col_sel:
    selected = st.selectbox("Select Keyword", keywords)

# ── Filter data ───────────────────────────────────────────────
kdf = df[df["Keyword"] == selected].copy().sort_values("Date")
kdf_sentiment = kdf[kdf["Sentiment_Score"].notna()]

# ── Derived metrics ───────────────────────────────────────────
peak_vol        = int(kdf["Search_Volume"].max())
peak_date       = kdf.loc[kdf["Search_Volume"].idxmax(), "Date"].strftime("%b %d")
avg_sentiment   = kdf_sentiment["Sentiment_Score"].mean() if len(kdf_sentiment) > 0 else 0
sentiment_label = (
    "Positive 😊" if avg_sentiment > 0.2 else
    "Neutral 😐"  if avg_sentiment > -0.2 else
    "Negative 😔"
)
days_tracked = (kdf["Date"].max() - kdf["Date"].min()).days + 1

# ── Metric cards ──────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card blue">
    <div class="metric-label">Peak Search Volume</div>
    <div class="metric-value">{peak_vol}</div>
    <div class="metric-sub">Reached on {peak_date}</div>
  </div>
  <div class="metric-card red">
    <div class="metric-label">Avg Fatigue Score</div>
    <div class="metric-value">{avg_sentiment:+.2f}</div>
    <div class="metric-sub">{sentiment_label}</div>
  </div>
  <div class="metric-card gold">
    <div class="metric-label">Days Tracked</div>
    <div class="metric-value">{days_tracked}</div>
    <div class="metric-sub">{kdf["Date"].min().strftime("%b %d")} — {kdf["Date"].max().strftime("%b %d, %Y")}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Dual-axis chart ───────────────────────────────────────────
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=kdf["Date"],
        y=kdf["Search_Volume"],
        name="Search Volume",
        mode="lines",
        line=dict(color="#4B8EF1", width=2.5),
        fill="tozeroy",
        fillcolor="rgba(75, 142, 241, 0.12)",
        hovertemplate="<b>%{x|%b %d}</b><br>Search Volume: %{y}<extra></extra>",
    ),
    secondary_y=False,
)

if len(kdf_sentiment) > 0:
    fig.add_trace(
        go.Scatter(
            x=kdf_sentiment["Date"],
            y=kdf_sentiment["Sentiment_Score"],
            name="Fatigue Score",
            mode="lines+markers",
            line=dict(color="#E05B5B", width=2.5),
            marker=dict(size=7, color="#E05B5B",
                        line=dict(color="#0C0E14", width=2)),
            hovertemplate="<b>%{x|%b %d}</b><br>Fatigue Score: %{y:.2f}<extra></extra>",
        ),
        secondary_y=True,
    )

fig.add_hline(
    y=0, secondary_y=True,
    line=dict(color="#2E3248", width=1, dash="dot"),
)

fig.update_layout(
    plot_bgcolor  = "#10121A",
    paper_bgcolor = "#10121A",
    font          = dict(family="DM Sans, sans-serif", color="#7A8099", size=12),
    legend        = dict(
        orientation="h", x=0.0, y=1.08,
        font=dict(size=12, color="#A0A4B8"),
        bgcolor="rgba(0,0,0,0)",
    ),
    margin        = dict(l=20, r=20, t=50, b=20),
    hovermode     = "x unified",
    hoverlabel    = dict(
        bgcolor="#1C1F2E", font_color="#E8E6E0",
        font_family="DM Mono, monospace", font_size=12,
        bordercolor="#2E3248",
    ),
    xaxis=dict(
        showgrid=False,
        tickfont=dict(family="DM Mono, monospace", size=11, color="#4A5068"),
        tickformat="%b %d",
        showline=True, linecolor="#1C1F2E",
    ),
    height=400,
)

fig.update_yaxes(
    title_text="Search Volume (0–100)",
    secondary_y=False,
    showgrid=True,
    gridcolor="#141720",
    gridwidth=1,
    tickfont=dict(family="DM Mono, monospace", size=11, color="#4B8EF1"),
    title_font=dict(color="#4B8EF1", size=11),
    zeroline=False,
    range=[0, max(kdf["Search_Volume"].max() * 1.2, 10)],
)

fig.update_yaxes(
    title_text="Fatigue Score (−1 to +1)",
    secondary_y=True,
    showgrid=False,
    tickfont=dict(family="DM Mono, monospace", size=11, color="#E05B5B"),
    title_font=dict(color="#E05B5B", size=11),
    zeroline=False,
    range=[-1.2, 1.2],
    tickvals=[-1.0, -0.5, 0.0, 0.5, 1.0],
)

st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
st.markdown('</div>', unsafe_allow_html=True)

# ── Dynamic insight cards ─────────────────────────────────────
if selected == "Coachella":
    st.error(
        "⚡ **Fad Signal Detected** — Coachella exhibits a classic fad lifecycle: "
        "search interest spikes sharply in mid-April (festival dates) then collapses "
        "within days. Sentiment data confirms audience sentiment becomes negative by the final weekend. "
        "Brands engaging with Coachella content after the search peak face rapidly "
        "diminishing returns and increased risk of audience backlash."
    )
else:
    st.success(
        "🌱 **Sustained Trend Signal** — Alo Yoga aesthetic shows the hallmarks of a "
        "durable cultural trend: moderate but consistent search interest across the "
        "observation window with a positive average sentiment score. Unlike fad-driven "
        "spikes, this pattern suggests the aesthetic is embedded in ongoing community "
        "identity (gym culture, 'that girl' aesthetic, wellness lifestyle) rather than "
        "a single event. Low negative sentiment risk in this window."
    )

# ── Analytical insight box ────────────────────────────────────
if selected == "Coachella":
    interpretation = (
        "The dual-signal chart reveals a textbook <b>fad pattern</b> as described by Rogers' "
        "Diffusion of Innovations: search volume peaks sharply around the festival dates "
        "(April 11–13 and April 18–20, 2025) before collapsing back to baseline within "
        "72 hours. The negative Fatigue Score on high-volume days indicates that even at "
        "peak cultural saturation, a segment of the audience has already entered the "
        "<em>reactance phase</em> — expressing annoyance at overexposure rather than "
        "enthusiasm. Marketers should note the 2–3 day lead time: sentiment turns negative "
        "slightly before search volume peaks, providing an early-exit signal."
    )
    verdict_color = "#E05B5B"
    verdict       = "FAD — Event-Driven Lifecycle"
else:
    interpretation = (
        "The Alo Yoga aesthetic signal demonstrates a <b>resilient trend</b> pattern: "
        "search interest remains relatively stable across the full observation window "
        "without a single catastrophic spike-and-crash. The positive Fatigue Score "
        "confirms that community sentiment surrounding the aesthetic remains net-positive "
        "— consistent with Maslach's emotional exhaustion model predicting low depletion "
        "risk for stimuli that feel chosen rather than imposed. The brand's alignment with "
        "the 'clean girl' and 'that girl' identity movements provides structural durability "
        "independent of any single cultural moment."
    )
    verdict_color = "#4DB87A"
    verdict       = "TREND — Identity-Embedded, Low Fatigue Risk"

st.markdown(f"""
<div class="insight-box">
  <div class="insight-title">Analytical Interpretation</div>
  <div class="insight-body">
    <span style="font-family:'DM Mono',monospace; font-size:0.72rem; color:{verdict_color};
                 background:{'rgba(224,91,91,0.1)' if selected=='Coachella' else 'rgba(77,184,122,0.1)'};
                 padding:3px 10px; border-radius:4px; margin-right:10px;">
      {verdict}
    </span><br><br>
    {interpretation}
  </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div class="tc-footer">
  TRENDCOMPASS · DATA: GOOGLE TRENDS + PULLPUSH.IO REDDIT ARCHIVE ·
  NLP: CARDIFFNLP ROBERTA · BUILT WITH STREAMLIT + PLOTLY
</div>
""", unsafe_allow_html=True)
