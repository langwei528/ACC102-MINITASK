import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Genre Investment Analyser",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM STYLING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── ROOT ── */
:root {
    --bg:      #0D0D0D;
    --surface: #161616;
    --border:  #2A2A2A;
    --text:    #F0EDE8;
    --muted:   #888880;
    --accent:  #C8A96E;
}

/* ── GLOBAL ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0D0D0D !important;
    color: #F0EDE8 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0D0D0D !important;
}

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1400px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #2A2A2A !important;
}

[data-testid="stSidebar"] * {
    color: #F0EDE8 !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: #888880 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #1E1E1E !important;
    border-color: #2A2A2A !important;
}

[data-testid="stSidebar"] .stMarkdown p {
    color: #888880 !important;
    font-size: 0.82rem !important;
}

/* ── MULTISELECT TAGS ── */
[data-baseweb="tag"] {
    background: #C8A96E !important;
    color: #0D0D0D !important;
    border-radius: 2px !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #C8A96E !important;
}

/* ── TITLE ── */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em !important;
    color: #F0EDE8 !important;
    line-height: 1.1 !important;
    margin-bottom: 0.5rem !important;
}

h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #F0EDE8 !important;
    margin-top: 2rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid #2A2A2A !important;
}

h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    color: #C8A96E !important;
}

p, li { color: #888880 !important; }

/* ── METRICS (KPI cards) ── */
[data-testid="stMetric"] {
    background: #161616 !important;
    border: 1px solid #2A2A2A !important;
    border-top: 2px solid #C8A96E !important;
    padding: 1.2rem 1.5rem !important;
    border-radius: 0 !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #888880 !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #F0EDE8 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #2A2A2A !important;
    gap: 0 !important;
    background: transparent !important;
}

[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #888880 !important;
    padding: 0.75rem 1.5rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    border-radius: 0 !important;
    transition: all 0.2s !important;
}

[data-testid="stTabs"] [role="tab"]:hover {
    color: #F0EDE8 !important;
    background: #161616 !important;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #C8A96E !important;
    border-bottom: 2px solid #C8A96E !important;
    background: transparent !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #2A2A2A !important;
}

.dvn-scroller { background: #161616 !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
    background: #1E1E1E !important;
    border-color: #2A2A2A !important;
    color: #F0EDE8 !important;
    border-radius: 0 !important;
}

/* ── DIVIDER ── */
hr {
    border-color: #2A2A2A !important;
    margin: 1.5rem 0 !important;
}

/* ── WARNING/INFO ── */
[data-testid="stAlert"] {
    background: #1E1E1E !important;
    border: 1px solid #C8A96E !important;
    border-radius: 0 !important;
    color: #F0EDE8 !important;
}

/* ── CAPTION ── */
[data-testid="stCaptionContainer"] p {
    font-size: 0.75rem !important;
    color: #555 !important;
}

/* ── PLOTLY CHARTS — make bg match ── */
.js-plotly-plot .plotly {
    border: 1px solid #2A2A2A !important;
}

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    padding: 3rem 0 2rem;
    border-bottom: 1px solid #2A2A2A;
    margin-bottom: 2rem;
">
    <p style="
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #C8A96E;
        font-family: DM Sans, sans-serif;
        margin-bottom: 0.75rem;
    ">ACC102 · Record Label A&R Intelligence</p>
    <h1 style="
        font-family: Playfair Display, serif;
        font-size: 3rem;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #F0EDE8;
        margin-bottom: 0.75rem;
    ">Genre Investment<br><em style='color:#C8A96E; font-style:italic;'>Analyser</em></h1>
    <p style="
        font-family: DM Sans, sans-serif;
        font-size: 0.95rem;
        color: #888880;
        max-width: 600px;
        line-height: 1.7;
    ">A data-driven tool for record label A&R teams — compare genre commercial
    performance, artist market structure, monetisation potential and regional
    trends across 20 countries.</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
DATA_FILE         = 'Cleaned_Spotify_2024_Global_Streaming_Data.csv'
STREAM_COL        = 'Total Streams (Millions)'
LISTENER_COL      = 'Monthly Listeners (Millions)'
DURATION_COL      = 'Avg Stream Duration (Min)'
SKIP_COL          = 'Skip Rate (%)'
HOURS_COL         = 'Total Hours Streamed (Millions)'
PLATFORM_COL      = 'Platform Type'
GENRE_COL         = 'Genre'
COUNTRY_COL       = 'Country'
ARTIST_COL        = 'Artist'
ALBUM_COL         = 'Album'
RECENT_STREAM_COL = 'Streams Last 30 Days (Millions)'
RELEASE_COL       = 'Release Year'

GENRE_COLORS = {
    'Pop':       '#C0392B',
    'R&B':       '#6C3483',
    'Rock':      '#1A5276',
    'Jazz':      '#B7950B',
    'Hip Hop':   '#1E8449',
    'K-pop':     '#A93226',
    'EDM':       '#117A65',
    'Reggaeton': '#935116',
    'Indie':     '#4A235A',
    'Classical': '#424949',
}

REGION_MAP = {
    'United States': 'North America', 'Canada': 'North America',
    'Mexico': 'Latin America', 'Brazil': 'Latin America', 'Argentina': 'Latin America',
    'United Kingdom': 'Europe', 'Germany': 'Europe', 'France': 'Europe',
    'Spain': 'Europe', 'Italy': 'Europe', 'Netherlands': 'Europe',
    'Sweden': 'Europe', 'Russia': 'Europe', 'Turkey': 'Europe',
    'India': 'Asia-Pacific', 'Japan': 'Asia-Pacific',
    'South Korea': 'Asia-Pacific', 'Indonesia': 'Asia-Pacific', 'Australia': 'Asia-Pacific',
    'South Africa': 'Africa'
}

COUNTRY_COORDS = {
    'United States': (37.1, -95.7), 'United Kingdom': (52.2, -1.2),
    'Canada': (56.1, -106.3), 'Brazil': (-14.2, -51.9),
    'Argentina': (-38.4, -63.6), 'Mexico': (23.6, -102.6),
    'Germany': (51.2, 10.5), 'France': (46.2, 2.2),
    'Spain': (40.5, -3.7), 'Italy': (41.9, 12.6),
    'Netherlands': (52.1, 5.3), 'Sweden': (60.1, 18.6),
    'Russia': (61.5, 105.3), 'Turkey': (39.1, 35.2),
    'India': (20.6, 78.9), 'Japan': (36.2, 138.3),
    'South Korea': (35.9, 128.0), 'Indonesia': (-0.8, 113.9),
    'Australia': (-25.3, 133.8), 'South Africa': (-30.6, 22.9)
}

PER_STREAM_RATE = {'Premium': 0.005, 'Free': 0.002}

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['Region']           = df[COUNTRY_COL].map(REGION_MAP)
    df['Engagement_Ratio'] = (df[HOURS_COL] / df[STREAM_COL]).round(4)
    df['Momentum_Pct']     = (df[RECENT_STREAM_COL] / df[STREAM_COL] * 100).round(2)
    df['Revenue_Est']      = df.apply(
        lambda r: r[STREAM_COL] * PER_STREAM_RATE.get(r[PLATFORM_COL], 0.003), axis=1
    ).round(2)
    return df

df = load_data()
all_genres     = sorted(df[GENRE_COL].unique())
all_countries  = sorted(df[COUNTRY_COL].unique())

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="padding:1rem 0 0.5rem;">
    <p style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;
              color:#C8A96E;margin-bottom:0.25rem;">Analysis Controls</p>
    <p style="font-size:0.82rem;color:#888880;">Adjust to explore different genres and regions.</p>
</div>
""", unsafe_allow_html=True)

selected_genres = st.sidebar.multiselect(
    "Select genres to analyse:",
    options=all_genres,
    default=['Pop', 'R&B', 'Rock', 'Jazz'],
    help="Choose which genres to compare in the deep-dive sections."
)

selected_countries = st.sidebar.multiselect(
    "Filter by countries:",
    options=all_countries,
    default=all_countries,
)

top_n = st.sidebar.slider("Top N artists to show:", min_value=3, max_value=10, value=6)

st.sidebar.markdown("""
<div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #2A2A2A;">
    <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
              color:#C8A96E;margin-bottom:0.5rem;">About</p>
    <p style="font-size:0.78rem;color:#666;line-height:1.6;">
        Built for A&R decision-makers at record labels.<br><br>
        <a href="https://www.kaggle.com/datasets/atharvasoundankar/spotify-global-streaming-data-2024"
           style="color:#C8A96E;" target="_blank">Spotify Global Streaming Data 2024</a><br><br>
        ACC102 Mini Assignment · Track 4
    </p>
</div>
""", unsafe_allow_html=True)

if len(selected_genres) < 2:
    st.warning("Please select at least 2 genres.")
    st.stop()

# ── Filter data ──
df_f = df[df[COUNTRY_COL].isin(selected_countries)]
df_focus = df_f[df_f[GENRE_COL].isin(selected_genres)].copy()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<p style="font-size:0.82rem;color:#888880;font-family:'DM Sans',sans-serif;
   padding:0.5rem 0 1.5rem;border-bottom:1px solid #2A2A2A;">
   Currently showing <span style="color:#C8A96E;font-weight:500;">{len(selected_genres)} genres</span>
   across <span style="color:#C8A96E;font-weight:500;">{len(selected_countries)} countries</span>.
   Use the sidebar to change filters.
</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;
   color:#C8A96E;font-family:'DM Sans',sans-serif;margin-top:1rem;margin-bottom:0.5rem;">
   📌 Snapshot: Selected Genres
</p>""", unsafe_allow_html=True)
cols = st.columns(len(selected_genres))
for i, genre in enumerate(selected_genres):
    sub = df_focus[df_focus[GENRE_COL] == genre]
    prem_pct = len(sub[sub[PLATFORM_COL] == 'Premium']) / max(len(sub), 1) * 100
    with cols[i]:
        st.metric(
            label=f"🎵 {genre}",
            value=f"{sub[STREAM_COL].mean():,.0f}M streams",
            delta=f"Skip: {sub[SKIP_COL].mean():.1f}%",
            delta_color="inverse"
        )
        st.caption(
            f"👥 {sub[LISTENER_COL].mean():.1f}M listeners  \n"
            f"💳 {prem_pct:.0f}% Premium  \n"
            f"⏱️ {sub[DURATION_COL].mean():.2f} min avg"
        )

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌐 Full Landscape",
    "🔍 Genre Deep Dive",
    "🎤 Artist Analysis",
    "🗺️ Regional Map",
    "💰 Revenue & Momentum",
    "🔬 Correlation"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: FULL LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("All 10 Genres — Market Overview")
    st.markdown("Before focusing on specific genres, here is the complete market landscape.")

    all_m = df_f.groupby(GENRE_COL).agg(
        Avg_Streams        = (STREAM_COL, 'mean'),
        Avg_Listeners      = (LISTENER_COL, 'mean'),
        Avg_Hours          = (HOURS_COL, 'mean'),
        Avg_Skip           = (SKIP_COL, 'mean'),
        Avg_Duration       = (DURATION_COL, 'mean'),
        Avg_Engagement     = ('Engagement_Ratio', 'mean'),
        Avg_Momentum       = ('Momentum_Pct', 'mean'),
        Count              = (STREAM_COL, 'count'),
    ).round(2).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig = px.scatter(
            all_m, x='Avg_Listeners', y='Avg_Streams',
            size='Avg_Hours', color=GENRE_COL,
            color_discrete_map=GENRE_COLORS,
            hover_name=GENRE_COL,
            hover_data={'Avg_Skip': ':.1f', 'Avg_Hours': ':.0f'},
            title="Genre Landscape: Streams vs Listeners<br><sup>Bubble size = total hours streamed</sup>",
            labels={'Avg_Listeners': 'Avg Monthly Listeners (M)', 'Avg_Streams': 'Avg Total Streams (M)'}
        )
        fig.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.bar(
            all_m.sort_values('Avg_Skip'), x='Avg_Skip', y=GENRE_COL,
            orientation='h', color=GENRE_COL,
            color_discrete_map=GENRE_COLORS,
            title="Skip Rate by Genre<br><sup>Lower = better listener retention</sup>",
            labels={'Avg_Skip': 'Skip Rate (%)', GENRE_COL: ''}
        )
        fig2.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig2, use_container_width=True)

    # Scorecard heatmap
    st.subheader("Genre Scorecard — All Metrics")
    plat_all = df_f.groupby([GENRE_COL, PLATFORM_COL]).size().unstack(fill_value=0)
    plat_all['Premium_Pct'] = (plat_all.get('Premium', 0) /
                                plat_all.sum(axis=1) * 100).round(1)

    scorecard = pd.DataFrame({
        'Avg Streams (M)':   all_m.set_index(GENRE_COL)['Avg_Streams'],
        'Avg Listeners (M)': all_m.set_index(GENRE_COL)['Avg_Listeners'],
        'Skip Rate (%)':     all_m.set_index(GENRE_COL)['Avg_Skip'],
        'Engagement Ratio':  all_m.set_index(GENRE_COL)['Avg_Engagement'],
        'Premium Conv. (%)': plat_all['Premium_Pct'],
        'Momentum (%)':      all_m.set_index(GENRE_COL)['Avg_Momentum'],
    }).round(2)

    norm = scorecard.copy()
    for col in norm.columns:
        rng = norm[col].max() - norm[col].min()
        if rng > 0:
            if col == 'Skip Rate (%)':
                norm[col] = 1 - (norm[col] - norm[col].min()) / rng
            else:
                norm[col] = (norm[col] - norm[col].min()) / rng

    fig_heat = px.imshow(
        norm.T, color_continuous_scale='RdYlGn',
        zmin=0, zmax=1,
        title="Genre Scorecard (green = stronger, red = weaker)",
        labels=dict(color="Normalised score"),
        aspect="auto",
        text_auto=False
    )
    # Add actual values as annotations
    for i, col in enumerate(norm.columns):
        for j, metric in enumerate(norm.index):
            fig_heat.add_annotation(
                x=i, y=j,
                text=str(scorecard.loc[metric, col]),
                showarrow=False, font=dict(size=10)
            )
    fig_heat.update_layout(height=420)
    st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: GENRE DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader(f"Deep Dive: {' vs '.join(selected_genres)}")

    # Radar chart
    focus_m = df_focus.groupby(GENRE_COL).agg(
        Streams    = (STREAM_COL, 'mean'),
        Listeners  = (LISTENER_COL, 'mean'),
        Duration   = (DURATION_COL, 'mean'),
        Hours      = (HOURS_COL, 'mean'),
        Momentum   = ('Momentum_Pct', 'mean'),
    ).round(2).reindex(selected_genres)

    pf = df_focus.groupby([GENRE_COL, PLATFORM_COL]).size().unstack(fill_value=0).reindex(selected_genres)
    if 'Premium' not in pf.columns: pf['Premium'] = 0
    if 'Free' not in pf.columns: pf['Free'] = 0
    pf['Premium_Pct'] = (pf['Premium'] / pf.sum(axis=1) * 100).round(1)
    focus_m['Premium'] = pf['Premium_Pct']

    norm_r = focus_m.copy()
    for col in norm_r.columns:
        rng = norm_r[col].max() - norm_r[col].min()
        if rng > 0:
            norm_r[col] = (norm_r[col] - norm_r[col].min()) / rng

    categories = ['Streams', 'Listeners', 'Duration', 'Hours', 'Momentum', 'Premium %']
    fig_radar = go.Figure()
    for genre in selected_genres:
        vals = norm_r.loc[genre].tolist()
        vals_closed = vals + [vals[0]]
        cats_closed = categories + [categories[0]]
        fig_radar.add_trace(go.Scatterpolar(
            r=vals_closed, theta=cats_closed,
            fill='toself', name=genre,
            line_color=GENRE_COLORS.get(genre, '#888'),
            fillcolor=GENRE_COLORS.get(genre, '#888'),
            opacity=0.25
        ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title=f"Performance Radar: {' vs '.join(selected_genres)}",
        height=500, showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # 2x2 metrics
    st.subheader("Key Metrics Comparison")
    metrics = [
        (STREAM_COL, 'Avg Total Streams (M)'),
        (LISTENER_COL, 'Monthly Listeners (M)'),
        (DURATION_COL, 'Avg Duration (Min)'),
        (SKIP_COL, 'Skip Rate (%) — lower is better')
    ]
    c1, c2 = st.columns(2)
    for idx, (col, title) in enumerate(metrics):
        data = df_focus.groupby(GENRE_COL)[col].mean().reindex(selected_genres).reset_index()
        data.columns = [GENRE_COL, 'value']
        fig_m = px.bar(
            data, x=GENRE_COL, y='value',
            color=GENRE_COL, color_discrete_map=GENRE_COLORS,
            title=title, text='value'
        )
        fig_m.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_m.update_layout(showlegend=False, height=320)
        if idx % 2 == 0:
            c1.plotly_chart(fig_m, use_container_width=True)
        else:
            c2.plotly_chart(fig_m, use_container_width=True)

    # Monetisation
    st.subheader("Monetisation: Free vs Premium")
    col1, col2 = st.columns(2)

    pf2 = df_focus.groupby([GENRE_COL, PLATFORM_COL]).size().unstack(fill_value=0).reindex(selected_genres)
    if 'Premium' not in pf2.columns: pf2['Premium'] = 0
    if 'Free' not in pf2.columns: pf2['Free'] = 0
    pf2['Prem_Pct'] = (pf2['Premium'] / pf2.sum(axis=1) * 100).round(1)
    pf2['Free_Pct'] = (pf2['Free']    / pf2.sum(axis=1) * 100).round(1)

    with col1:
        fig_s = go.Figure()
        fig_s.add_trace(go.Bar(name='Free', x=selected_genres, y=pf2['Free_Pct'],
                               marker_color='#D5D8DC',
                               text=pf2['Free_Pct'].apply(lambda x: f'{x:.0f}%'),
                               textposition='inside'))
        fig_s.add_trace(go.Bar(name='Premium', x=selected_genres, y=pf2['Prem_Pct'],
                               marker_color='#1A5276',
                               text=pf2['Prem_Pct'].apply(lambda x: f'{x:.0f}%'),
                               textposition='inside'))
        fig_s.update_layout(barmode='stack', title='Free vs Premium Split', height=380)
        st.plotly_chart(fig_s, use_container_width=True)

    with col2:
        fig_lol = go.Figure()
        for i, (genre, val) in enumerate(pf2['Prem_Pct'].items()):
            fig_lol.add_trace(go.Scatter(
                x=[0, val], y=[genre, genre], mode='lines',
                line=dict(color=GENRE_COLORS.get(genre, '#888'), width=3),
                showlegend=False
            ))
            fig_lol.add_trace(go.Scatter(
                x=[val], y=[genre], mode='markers+text',
                marker=dict(color=GENRE_COLORS.get(genre, '#888'), size=14),
                text=[f'{val:.1f}%'], textposition='middle right',
                showlegend=False
            ))
        fig_lol.add_vline(x=50, line_dash='dash', line_color='red',
                          annotation_text='50% line')
        fig_lol.update_layout(title='Premium Conversion Rate', xaxis_range=[0, 75], height=380)
        st.plotly_chart(fig_lol, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: ARTIST ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Artist-Level Analysis")
    st.markdown(
        "Artist data helps answer key signing decisions: "
        "**Who are the stars? How concentrated is the market? Where is the room for new talent?**"
    )

    col1, col2 = st.columns(2)

    # Top artists per selected genre
    with col1:
        genre_sel = st.selectbox("Select genre for top artists:", selected_genres)
        sub_art = df_focus[df_focus[GENRE_COL] == genre_sel]
        top_art = sub_art.groupby(ARTIST_COL)[STREAM_COL].mean().nlargest(top_n).reset_index()
        top_art.columns = [ARTIST_COL, STREAM_COL]

        fig_art = px.bar(
            top_art.sort_values(STREAM_COL), x=STREAM_COL, y=ARTIST_COL,
            orientation='h', color_discrete_sequence=[GENRE_COLORS.get(genre_sel, '#888')],
            title=f"Top {top_n} Artists — {genre_sel}",
            labels={STREAM_COL: 'Avg Streams (M)', ARTIST_COL: ''},
            text=STREAM_COL
        )
        fig_art.update_traces(texttemplate='%{text:.0f}M', textposition='outside')
        fig_art.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_art, use_container_width=True)

    # Market concentration
    with col2:
        conc = {}
        for g in selected_genres:
            s = df_focus[df_focus[GENRE_COL] == g].groupby(ARTIST_COL)[STREAM_COL].mean().sort_values(ascending=False)
            conc[g] = round(s.iloc[:3].sum() / s.sum() * 100, 1) if len(s) >= 3 else 0

        conc_df = pd.DataFrame(list(conc.items()), columns=['Genre', 'Top3_Share'])
        fig_conc = px.bar(
            conc_df.sort_values('Top3_Share'), x='Top3_Share', y='Genre',
            orientation='h', color='Genre',
            color_discrete_map=GENRE_COLORS,
            title="Market Concentration<br><sup>% of streams from top 3 artists — higher = dominated by superstars</sup>",
            labels={'Top3_Share': 'Top-3 Artist Stream Share (%)', 'Genre': ''},
            text='Top3_Share'
        )
        fig_conc.add_vline(x=50, line_dash='dash', line_color='red')
        fig_conc.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_conc.update_layout(showlegend=False, height=400, xaxis_range=[0, 90])
        st.plotly_chart(fig_conc, use_container_width=True)

    # Artist commercial map (scatter)
    st.subheader("Artist Commercial Map: Streams vs Skip Rate")
    artist_data = df_focus.groupby([ARTIST_COL, GENRE_COL]).agg(
        Streams   = (STREAM_COL, 'mean'),
        SkipRate  = (SKIP_COL, 'mean'),
        Listeners = (LISTENER_COL, 'mean')
    ).reset_index()

    fig_scat = px.scatter(
        artist_data, x='SkipRate', y='Streams',
        color=GENRE_COL, color_discrete_map=GENRE_COLORS,
        size='Listeners', hover_name=ARTIST_COL,
        title="Artist Map: Streams vs Skip Rate (bubble = listener size)",
        labels={'SkipRate': 'Skip Rate (%) — lower is better', 'Streams': 'Avg Streams (M)'}
    )
    fig_scat.add_vline(x=df_focus[SKIP_COL].mean(), line_dash='dot', line_color='gray',
                       annotation_text='avg skip rate')
    fig_scat.add_hline(y=df_focus[STREAM_COL].mean(), line_dash='dot', line_color='gray',
                       annotation_text='avg streams')
    fig_scat.update_layout(height=500)
    st.plotly_chart(fig_scat, use_container_width=True)

    # Box plot: stream distribution
    st.subheader("Stream Distribution by Genre")
    box_data = []
    for g in selected_genres:
        vals = df_focus[df_focus[GENRE_COL] == g].groupby(ARTIST_COL)[STREAM_COL].mean().values
        for v in vals:
            box_data.append({'Genre': g, STREAM_COL: v})
    box_df = pd.DataFrame(box_data)

    fig_box = px.box(
        box_df, x='Genre', y=STREAM_COL,
        color='Genre', color_discrete_map=GENRE_COLORS,
        title="Stream Distribution per Genre<br><sup>Box = IQR, dots = individual artists</sup>",
        points='all'
    )
    fig_box.update_layout(showlegend=False, height=420)
    st.plotly_chart(fig_box, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: REGIONAL MAP
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Global Genre Preferences")

    top_genre = df_f.groupby(COUNTRY_COL)[GENRE_COL].agg(lambda x: x.value_counts().index[0])
    map_rows = []
    for country, genre in top_genre.items():
        if country in COUNTRY_COORDS:
            lat, lon = COUNTRY_COORDS[country]
            map_rows.append({'Country': country, 'Top Genre': genre, 'lat': lat, 'lon': lon})
    map_df = pd.DataFrame(map_rows)

    fig_map = px.scatter_geo(
        map_df, lat='lat', lon='lon', color='Top Genre',
        color_discrete_map=GENRE_COLORS,
        hover_name='Country', size_max=18,
        title="Most Popular Genre by Country",
        projection="natural earth"
    )
    fig_map.update_traces(marker=dict(size=14, line=dict(width=1.5, color='white')))
    fig_map.update_layout(
        height=520,
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor='lightgray',
                 showland=True, landcolor='#F0F0F0', showocean=True, oceancolor='#E8F4F8')
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # Country heatmap
    st.subheader("Country × Genre Heatmap")
    heat = df_f.groupby([COUNTRY_COL, GENRE_COL]).size().unstack(fill_value=0)

    fig_heat2 = px.imshow(
        heat, color_continuous_scale='YlOrRd',
        title="Song Count by Country and Genre (darker = more)",
        labels=dict(x='Genre', y='Country', color='Songs'),
        aspect='auto'
    )
    fig_heat2.update_layout(height=600)
    st.plotly_chart(fig_heat2, use_container_width=True)

    # Regional bar
    st.subheader("Regional Performance — Focus Genres")
    region_data = df_focus.groupby(['Region', GENRE_COL])[STREAM_COL].mean().reset_index()
    fig_reg = px.bar(
        region_data, x='Region', y=STREAM_COL,
        color=GENRE_COL, color_discrete_map=GENRE_COLORS,
        barmode='group',
        title=f"Average Streams by Region: {' vs '.join(selected_genres)}",
        labels={STREAM_COL: 'Avg Streams (M)'}
    )
    fig_reg.update_layout(height=420, xaxis_tickangle=-20)
    st.plotly_chart(fig_reg, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: REVENUE & MOMENTUM
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Revenue Estimation & Streaming Momentum")
    st.markdown(
        "Revenue is estimated using industry per-stream rates: "
        "**$0.005/stream (Premium)** and **$0.002/stream (Free/Ad-supported)**."
    )

    rev_rows = []
    for g in selected_genres:
        sub = df_focus[df_focus[GENRE_COL] == g]
        pr = sub[sub[PLATFORM_COL] == 'Premium'][STREAM_COL].sum() * PER_STREAM_RATE['Premium']
        fr = sub[sub[PLATFORM_COL] == 'Free'][STREAM_COL].sum() * PER_STREAM_RATE['Free']
        n  = max(len(sub), 1)
        rev_rows.append({
            'Genre':              g,
            'Premium Rev ($M)':   round(pr, 2),
            'Ad Rev ($M)':        round(fr, 2),
            'Total Rev ($M)':     round(pr + fr, 2),
            'Rev/Song ($M)':      round((pr + fr) / n, 2),
            'Momentum (%)':       round(sub['Momentum_Pct'].mean(), 2)
        })
    rev_df = pd.DataFrame(rev_rows).set_index('Genre')

    st.dataframe(rev_df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            name='Premium', x=selected_genres,
            y=rev_df['Premium Rev ($M)'], marker_color='#1A5276'))
        fig_rev.add_trace(go.Bar(
            name='Ad Revenue', x=selected_genres,
            y=rev_df['Ad Rev ($M)'], marker_color='#D5D8DC'))
        fig_rev.update_layout(barmode='stack', title='Total Revenue by Genre', height=380)
        st.plotly_chart(fig_rev, use_container_width=True)

    with col2:
        fig_eff = px.bar(
            rev_df.reset_index(), x='Genre', y='Rev/Song ($M)',
            color='Genre', color_discrete_map=GENRE_COLORS,
            title='Revenue per Song<br><sup>Investment efficiency</sup>',
            text='Rev/Song ($M)'
        )
        fig_eff.update_traces(texttemplate='$%{text:.2f}M', textposition='outside')
        fig_eff.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_eff, use_container_width=True)

    with col3:
        fig_mom = px.bar(
            rev_df.reset_index().sort_values('Momentum (%)'),
            x='Momentum (%)', y='Genre', orientation='h',
            color='Genre', color_discrete_map=GENRE_COLORS,
            title='Streaming Momentum<br><sup>Recent streams / total streams</sup>',
            text='Momentum (%)'
        )
        fig_mom.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_mom.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_mom, use_container_width=True)

    # Release year trend
    st.subheader("Release Year Trend (2015–2024)")
    yr = df_focus.groupby([RELEASE_COL, GENRE_COL]).size().reset_index(name='Count')
    yr = yr[yr[RELEASE_COL] >= 2015]
    fig_yr = px.line(
        yr, x=RELEASE_COL, y='Count', color=GENRE_COL,
        color_discrete_map=GENRE_COLORS, markers=True,
        title="Songs Appearing in Top Charts by Release Year",
        labels={RELEASE_COL: 'Release Year', 'Count': 'Number of Songs'}
    )
    fig_yr.update_layout(height=380)
    st.plotly_chart(fig_yr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6: CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("Correlation Analysis")
    st.markdown("Understanding which metrics move together helps identify the real drivers of commercial success.")

    num_cols    = [STREAM_COL, LISTENER_COL, DURATION_COL, SKIP_COL,
                   HOURS_COL, RECENT_STREAM_COL, 'Engagement_Ratio', 'Momentum_Pct']
    short_names = ['Streams', 'Listeners', 'Duration', 'Skip Rate',
                   'Hours', 'Recent Streams', 'Engagement', 'Momentum']
    corr = df_focus[num_cols].corr().round(2)
    corr.index = short_names
    corr.columns = short_names

    fig_corr = px.imshow(
        corr, color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
        title="Correlation Matrix — All Key Metrics",
        text_auto='.2f', aspect='equal'
    )
    fig_corr.update_layout(height=550)
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("**Key takeaways:**")
    insights = []
    for c1, c2 in [('Streams', 'Hours'), ('Streams', 'Skip Rate'),
                   ('Listeners', 'Duration'), ('Engagement', 'Momentum')]:
        val = corr.loc[c1, c2]
        direction = "positively" if val > 0 else "negatively"
        strength  = "strongly" if abs(val) > 0.5 else "weakly"
        insights.append(f"- **{c1}** and **{c2}** are {strength} {direction} correlated ({val:+.2f})")
    for line in insights:
        st.markdown(line)

# ══════════════════════════════════════════════════════════════════════════════
# RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="margin-top:3rem;padding-top:2rem;border-top:1px solid #2A2A2A;">
    <p style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;
              color:#C8A96E;font-family:'DM Sans',sans-serif;margin-bottom:0.5rem;">
        05 — Investment Recommendation
    </p>
    <h2 style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;
               color:#F0EDE8;border:none!important;margin-bottom:1.5rem;">
        The A&R portfolio strategy.
    </h2>
</div>
""", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown("""
    <div style="padding:1.5rem;background:#161616;border:1px solid #2A2A2A;
                border-bottom:3px solid #1A5276;margin-bottom:1rem;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#888880;margin-bottom:0.4rem;">Strategy A · Subscription Revenue</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#4A90C4;margin-bottom:0.75rem;font-weight:700;">Rock 🎸</p>
        <p style="font-size:0.85rem;color:#888880;line-height:1.7;">
            Highest premium conversion (55%) and broadest monthly listener base.
            Every Rock signing maximises subscription revenue potential.
        </p>
    </div>
    <div style="padding:1.5rem;background:#161616;border:1px solid #2A2A2A;
                border-bottom:3px solid #B7950B;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#888880;margin-bottom:0.4rem;">Strategy C · Emerging Market</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#B7950B;margin-bottom:0.75rem;font-weight:700;">Jazz 🎷</p>
        <p style="font-size:0.85rem;color:#888880;line-height:1.7;">
            Surprisingly strong in Turkey, Mexico and South Korea. High-quality
            premium audience in underserved markets.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_r2:
    st.markdown("""
    <div style="padding:1.5rem;background:#161616;border:1px solid #2A2A2A;
                border-bottom:3px solid #6C3483;margin-bottom:1rem;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#888880;margin-bottom:0.4rem;">Strategy B · Catalogue & Engagement</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#9B6DB5;margin-bottom:0.75rem;font-weight:700;">R&B 💿</p>
        <p style="font-size:0.85rem;color:#888880;line-height:1.7;">
            Highest streams, lowest skip rate, longest sessions. Ideal for
            long-term catalogue royalties and playlist placement.
        </p>
    </div>
    <div style="padding:1.5rem;background:#161616;border:1px solid #2A2A2A;
                border-bottom:3px solid #C0392B;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#888880;margin-bottom:0.4rem;">Strategy D · Traffic & Discovery</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#E07070;margin-bottom:0.75rem;font-weight:700;">Pop 🎤</p>
        <p style="font-size:0.85rem;color:#888880;line-height:1.7;">
            Widest reach but highest skip rate and lowest premium conversion.
            Use as a traffic driver, not a core investment.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:2rem;padding:1.5rem 2rem;background:#161616;
            border:1px solid #C8A96E;text-align:center;">
    <p style="font-size:0.78rem;color:#888880;margin-bottom:0.5rem;">Bottom line</p>
    <p style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#F0EDE8;
              font-style:italic;">
        "A dual-track investment in Rock (subscription revenue) and R&B (engagement value)
        offers the best risk-adjusted return for a record label's portfolio."
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid #2A2A2A;
            display:flex;justify-content:space-between;">
    <p style="font-size:0.72rem;color:#444;letter-spacing:0.05em;">
        Genre Investment Analyser · ACC102 Mini Assignment · Xi'an Jiaotong-Liverpool University
    </p>
    <p style="font-size:0.72rem;color:#444;">
        Data: Kaggle Spotify Global Streaming Data 2024 · Built with Python, Streamlit, Plotly
    </p>
</div>
""", unsafe_allow_html=True)
