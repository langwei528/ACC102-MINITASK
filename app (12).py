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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400;1,700&family=DM+Mono:wght@300;400;500&family=Space+Grotesk:wght@300;400;500&display=swap');

:root {
    --bg:      #0A0A1A;
    --surface: #12112A;
    --surface2:#1A1836;
    --border:  #2D2B5E;
    --accent:  #7B5CF0;
    --accent2: #A78BFA;
    --text:    #E8E4FF;
    --muted:   #8B84C4;
    --spotify: #1DB954;
}

html, body, [data-testid="stAppViewContainer"] {
    background: #0A0A1A !important;
    color: #E8E4FF !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0A0A1A !important;
}

.main .block-container {
    padding: 2rem 3rem 4rem !important;
    max-width: 1400px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #08081A !important;
    border-right: 1px solid #2D2B5E !important;
}
[data-testid="stSidebar"] * { color: #E8E4FF !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: #8B84C4 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #12112A !important;
    border-color: #2D2B5E !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #8B84C4 !important;
    font-size: 0.82rem !important;
}

/* ── MULTISELECT TAGS ── */
[data-baseweb="tag"] {
    background: #7B5CF0 !important;
    color: white !important;
    border-radius: 2px !important;
}

/* ── SLIDER ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #7B5CF0 !important;
}

/* ── HEADINGS ── */
h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.02em !important;
    color: #E8E4FF !important;
    line-height: 1.1 !important;
}
h2 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #E8E4FF !important;
    border-bottom: 1px solid #2D2B5E !important;
    padding-bottom: 0.5rem !important;
    margin-top: 2rem !important;
}
h3 {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.05rem !important;
    font-weight: 400 !important;
    color: #A78BFA !important;
}

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: #12112A !important;
    border: 1px solid #2D2B5E !important;
    border-top: 2px solid #7B5CF0 !important;
    padding: 1.2rem 1.5rem !important;
    border-radius: 0 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #8B84C4 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #A78BFA !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] {
    border-bottom: 1px solid #2D2B5E !important;
    background: transparent !important;
}
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #8B84C4 !important;
    padding: 0.75rem 1.4rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    border-radius: 0 !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
    color: #A78BFA !important;
    background: #12112A !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #A78BFA !important;
    border-bottom: 2px solid #7B5CF0 !important;
    background: transparent !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border: 1px solid #2D2B5E !important; }
.dvn-scroller { background: #12112A !important; }

/* ── SELECTBOX ── */
[data-baseweb="select"] > div {
    background: #12112A !important;
    border-color: #2D2B5E !important;
    color: #E8E4FF !important;
    border-radius: 0 !important;
}

/* ── PARAGRAPH TEXT in markdown containers ── */
[data-testid="stMarkdownContainer"] > p { color: #8B84C4 !important; }
[data-testid="stMarkdownContainer"] li  { color: #8B84C4 !important; }

/* ── ALERT ── */
[data-testid="stAlert"] {
    background: #12112A !important;
    border: 1px solid #7B5CF0 !important;
    border-radius: 0 !important;
    color: #E8E4FF !important;
}

/* ── CAPTION ── */
[data-testid="stCaptionContainer"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #3D3B7E !important;
    letter-spacing: 0.06em !important;
}

/* ── DIVIDER ── */
hr { border-color: #2D2B5E !important; }

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── HERO HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    padding: 2.5rem 0 2rem;
    border-bottom: 1px solid #2D2B5E;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
">
    <div style="
        position: absolute; top: -100px; right: -100px;
        width: 400px; height: 400px;
        background: radial-gradient(circle, rgba(123,92,240,0.08) 0%, transparent 70%);
        pointer-events: none;
    "></div>
    <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:1rem;">
        <div style="
            width:32px; height:32px; background:#1DB954; border-radius:50%;
            display:flex; align-items:center; justify-content:center; flex-shrink:0;
        ">
            <svg viewBox="0 0 24 24" fill="white" width="18" height="18">
                <path d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/>
            </svg>
        </div>
        <p style="
            font-family: DM Mono, monospace;
            font-size: 0.62rem;
            letter-spacing: 0.22em;
            text-transform: uppercase;
            color: #A78BFA;
            margin: 0;
        ">ACC102 · Record Label A&R Intelligence · Spotify Global 2024</p>
    </div>
    <h1 style="
        font-family: Playfair Display, serif;
        font-size: 2.8rem;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.02em;
        color: #E8E4FF;
        margin-bottom: 0.75rem;
    ">Genre Investment <em style="color:#A78BFA; font-style:italic;">Analyser</em></h1>
    <p style="
        font-family: Space Grotesk, sans-serif;
        font-size: 0.92rem;
        color: #8B84C4;
        max-width: 620px;
        line-height: 1.75;
        margin: 0;
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
    'Pop':       '#E07070',
    'R&B':       '#A78BFA',
    'Rock':      '#5DADE2',
    'Jazz':      '#F4D03F',
    'Hip Hop':   '#52BE80',
    'K-pop':     '#F1948A',
    'EDM':       '#48C9B0',
    'Reggaeton': '#F0A500',
    'Indie':     '#BB8FCE',

    'Classical': '#85929E',
}

# Plotly dark purple theme applied to all charts
def dark_theme(fig, height=380):
    fig.update_layout(
        paper_bgcolor='#12112A',
        plot_bgcolor='#12112A',
        font=dict(family='Space Grotesk, sans-serif', color='#8B84C4', size=11),
        height=height,
        xaxis=dict(gridcolor='#2D2B5E', linecolor='#2D2B5E',
                   tickcolor='#2D2B5E', tickfont=dict(color='#8B84C4', size=10),
                   zerolinecolor='#2D2B5E'),
        yaxis=dict(gridcolor='#2D2B5E', linecolor='#2D2B5E',
                   tickcolor='#2D2B5E', tickfont=dict(color='#8B84C4', size=10),
                   zerolinecolor='#2D2B5E'),
        legend=dict(bgcolor='transparent', font=dict(color='#8B84C4')),
    )
    return fig

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
              color:#A78BFA;margin-bottom:0.25rem;">Analysis Controls</p>
    <p style="font-size:0.82rem;color:#8B84C4;">Adjust to explore different genres and regions.</p>
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
<div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid #2D2B5E;">
    <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
              color:#A78BFA;margin-bottom:0.5rem;">About</p>
    <p style="font-size:0.78rem;color:#666;line-height:1.6;">
        Built for A&R decision-makers at record labels.<br><br>
        <a href="https://www.kaggle.com/datasets/atharvasoundankar/spotify-global-streaming-data-2024"
           style="color:#A78BFA;" target="_blank">Spotify Global Streaming Data 2024</a><br><br>
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
<p style="font-size:0.82rem;color:#8B84C4;font-family:'Space Grotesk',sans-serif;
   padding:0.5rem 0 1.5rem;border-bottom:1px solid #2D2B5E;">
   Currently showing <span style="color:#A78BFA;font-weight:500;">{len(selected_genres)} genres</span>
   across <span style="color:#A78BFA;font-weight:500;">{len(selected_countries)} countries</span>.
   Use the sidebar to change filters.
</p>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<p style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;
   color:#A78BFA;font-family:'Space Grotesk',sans-serif;margin-top:1rem;margin-bottom:0.5rem;">
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
        norm.T, color_continuous_scale=[[0,'#5C0A0A'],[0.3,'#7B1818'],[0.5,'#1A1836'],[0.7,'#1A4D3A'],[1,'#1E8449']],
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
        heat, color_continuous_scale=[[0,'#0A0A1A'],[0.3,'#2D1B69'],[0.6,'#7B5CF0'],[1,'#A78BFA']],
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
        corr, color_continuous_scale=[[0,'#5C1A1A'],[0.25,'#7B1818'],[0.5,'#1A1836'],[0.75,'#1A3A4D'],[1,'#1A6B3A']], zmin=-1, zmax=1,
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
<div style="margin-top:3rem;padding-top:2rem;border-top:1px solid #2D2B5E;">
    <p style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;
              color:#A78BFA;font-family:'Space Grotesk',sans-serif;margin-bottom:0.5rem;">
        05 — Investment Recommendation
    </p>
    <h2 style="font-family:'Playfair Display',serif;font-size:2rem;font-weight:700;
               color:#E8E4FF;border:none!important;margin-bottom:1.5rem;">
        The A&R portfolio strategy.
    </h2>
</div>
""", unsafe_allow_html=True)

col_r1, col_r2 = st.columns(2)
with col_r1:
    st.markdown("""
    <div style="padding:1.5rem;background:#12112A;border:1px solid #2D2B5E;
                border-bottom:3px solid #5DADE2;margin-bottom:1rem;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#8B84C4;margin-bottom:0.4rem;">Strategy A · Subscription Revenue</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#5DADE2;margin-bottom:0.75rem;font-weight:700;">Rock 🎸</p>
        <p style="font-size:0.85rem;color:#8B84C4;line-height:1.7;">
            Highest premium conversion (55%) and broadest monthly listener base.
            Every Rock signing maximises subscription revenue potential.
        </p>
    </div>
    <div style="padding:1.5rem;background:#12112A;border:1px solid #2D2B5E;
                border-bottom:3px solid #B7950B;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#8B84C4;margin-bottom:0.4rem;">Strategy C · Emerging Market</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#B7950B;margin-bottom:0.75rem;font-weight:700;">Jazz 🎷</p>
        <p style="font-size:0.85rem;color:#8B84C4;line-height:1.7;">
            Surprisingly strong in Turkey, Mexico and South Korea. High-quality
            premium audience in underserved markets.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_r2:
    st.markdown("""
    <div style="padding:1.5rem;background:#12112A;border:1px solid #2D2B5E;
                border-bottom:3px solid #7B5CF0;margin-bottom:1rem;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#8B84C4;margin-bottom:0.4rem;">Strategy B · Catalogue & Engagement</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#A78BFA;margin-bottom:0.75rem;font-weight:700;">R&B 💿</p>
        <p style="font-size:0.85rem;color:#8B84C4;line-height:1.7;">
            Highest streams, lowest skip rate, longest sessions. Ideal for
            long-term catalogue royalties and playlist placement.
        </p>
    </div>
    <div style="padding:1.5rem;background:#12112A;border:1px solid #2D2B5E;
                border-bottom:3px solid #E07070;">
        <p style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;
                  color:#8B84C4;margin-bottom:0.4rem;">Strategy D · Traffic & Discovery</p>
        <p style="font-family:'Playfair Display',serif;font-size:1.6rem;
                  color:#F08080;margin-bottom:0.75rem;font-weight:700;">Pop 🎤</p>
        <p style="font-size:0.85rem;color:#8B84C4;line-height:1.7;">
            Widest reach but highest skip rate and lowest premium conversion.
            Use as a traffic driver, not a core investment.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:2rem;padding:1.5rem 2rem;background:#12112A;
            border:1px solid #A78BFA;text-align:center;">
    <p style="font-size:0.78rem;color:#8B84C4;margin-bottom:0.5rem;">Bottom line</p>
    <p style="font-family:'Playfair Display',serif;font-size:1.1rem;color:#E8E4FF;
              font-style:italic;">
        "A dual-track investment in Rock (subscription revenue) and R&B (engagement value)
        offers the best risk-adjusted return for a record label's portfolio."
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="margin-top:3rem;padding-top:1.5rem;border-top:1px solid #2D2B5E;
            display:flex;justify-content:space-between;">
    <p style="font-size:0.72rem;color:#444;letter-spacing:0.05em;">
        Genre Investment Analyser · ACC102 Mini Assignment · Xi'an Jiaotong-Liverpool University
    </p>
    <p style="font-size:0.72rem;color:#444;">
        Data: Kaggle Spotify Global Streaming Data 2024 · Built with Python, Streamlit, Plotly
    </p>
</div>
""", unsafe_allow_html=True)
