import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# CONFIGURATION VARIABLES
# ══════════════════════════════════════════════════════════════════════════════
DATA_FILE = 'Cleaned_Spotify_2024_Global_Streaming_Data.csv'

STREAM_COL       = 'Total Streams (Millions)'
LISTENER_COL     = 'Monthly Listeners (Millions)'
DURATION_COL     = 'Avg Stream Duration (Min)'
SKIP_COL         = 'Skip Rate (%)'
HOURS_COL        = 'Total Hours Streamed (Millions)'
PLATFORM_COL     = 'Platform Type'
GENRE_COL        = 'Genre'
COUNTRY_COL      = 'Country'
RECENT_STREAM_COL = 'Streams Last 30 Days (Millions)'
RELEASE_COL      = 'Release Year'

GENRE_COLORS = {
    'Pop': '#E74C3C', 'R&B': '#9B59B6', 'Rock': '#3498DB', 'Jazz': '#F39C12',
    'Hip Hop': '#2ECC71', 'K-pop': '#E91E63', 'EDM': '#00BCD4',
    'Reggaeton': '#FF9800', 'Indie': '#8BC34A', 'Classical': '#795548'
}

REGION_MAP = {
    'United States': 'North America', 'Canada': 'North America',
    'Mexico': 'Latin America', 'Brazil': 'Latin America', 'Argentina': 'Latin America',
    'United Kingdom': 'Europe', 'Germany': 'Europe', 'France': 'Europe',
    'Spain': 'Europe', 'Italy': 'Europe', 'Netherlands': 'Europe', 'Sweden': 'Europe',
    'Russia': 'Europe', 'Turkey': 'Europe',
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

# Per-stream revenue estimates (USD)
PREMIUM_RATE = 0.005
FREE_RATE = 0.002

# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df['Region'] = df[COUNTRY_COL].map(REGION_MAP)
    return df

df = load_data()
all_genres = sorted(df[GENRE_COL].unique())
all_countries = sorted(df[COUNTRY_COL].unique())

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — USER CONTROLS
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.title("🎛️ Analysis Controls")
st.sidebar.markdown("Adjust these to explore different genres and regions.")

selected_genres = st.sidebar.multiselect(
    "Select genres to analyse:",
    options=all_genres,
    default=['Pop', 'R&B', 'Rock', 'Jazz'],
    help="Choose which genres to compare. The full landscape always shows all 10."
)

selected_countries = st.sidebar.multiselect(
    "Filter by countries (optional):",
    options=all_countries,
    default=all_countries,
    help="Leave all selected to see the full global picture."
)

metric_choice = st.sidebar.selectbox(
    "Primary metric for ranking:",
    options=[STREAM_COL, LISTENER_COL, DURATION_COL, SKIP_COL, HOURS_COL, RECENT_STREAM_COL],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("**About this tool**")
st.sidebar.markdown(
    "Built for A&R decision-makers at record labels. "
    "Data source: [Kaggle — Spotify Global Streaming Data 2024]"
    "(https://www.kaggle.com/datasets/atharvasoundankar/spotify-global-streaming-data-2024)"
)
st.sidebar.markdown("ACC102 Mini Assignment · Track 4")

# ══════════════════════════════════════════════════════════════════════════════
# FILTER DATA
# ══════════════════════════════════════════════════════════════════════════════
df_filtered = df[df[COUNTRY_COL].isin(selected_countries)]
df_focus = df_filtered[df_filtered[GENRE_COL].isin(selected_genres)].copy()

if len(selected_genres) < 2:
    st.warning("Please select at least 2 genres to enable comparison.")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.title("🎵 Genre Investment Analyser")
st.markdown(
    "**A data-driven tool for record label A&R teams** — compare genre performance, "
    "listener engagement, monetisation potential, and regional preferences across "
    f"**{len(selected_countries)} countries**."
)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1: KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.header("📊 Key Metrics at a Glance")

kpi_cols = st.columns(len(selected_genres))
for i, genre in enumerate(selected_genres):
    subset = df_focus[df_focus[GENRE_COL] == genre]
    with kpi_cols[i]:
        st.metric(label=f"🎵 {genre}", value=f"{subset[STREAM_COL].mean():,.0f}M",
                  delta=f"Skip: {subset[SKIP_COL].mean():.1f}%", delta_color="inverse")
        st.caption(f"👥 {subset[LISTENER_COL].mean():.1f}M listeners · ⏱️ {subset[DURATION_COL].mean():.2f} min avg")

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2: FULL LANDSCAPE
# ══════════════════════════════════════════════════════════════════════════════
st.header("🌐 Full Market Landscape (All 10 Genres)")

all_metrics = df_filtered.groupby(GENRE_COL).agg(
    Avg_Streams=(STREAM_COL, 'mean'),
    Avg_Listeners=(LISTENER_COL, 'mean'),
    Avg_Duration=(DURATION_COL, 'mean'),
    Avg_Skip_Rate=(SKIP_COL, 'mean'),
    Song_Count=(STREAM_COL, 'count')
).round(2).sort_values('Avg_Streams', ascending=False)

col1, col2 = st.columns(2)

with col1:
    fig_land = px.bar(
        all_metrics.reset_index(), x='Avg_Streams', y=GENRE_COL,
        orientation='h', color=GENRE_COL,
        color_discrete_map=GENRE_COLORS,
        title="Average Total Streams by Genre",
        labels={'Avg_Streams': 'Average Streams (Millions)', GENRE_COL: ''}
    )
    fig_land.update_layout(showlegend=False, yaxis={'categoryorder': 'total ascending'}, height=400)
    st.plotly_chart(fig_land, use_container_width=True)

with col2:
    fig_eng = px.bar(
        all_metrics.reset_index(), x='Avg_Skip_Rate', y=GENRE_COL,
        orientation='h', color=GENRE_COL,
        color_discrete_map=GENRE_COLORS,
        title="Skip Rate by Genre (Lower = Better)",
        labels={'Avg_Skip_Rate': 'Skip Rate (%)', GENRE_COL: ''}
    )
    fig_eng.update_layout(showlegend=False, yaxis={'categoryorder': 'total descending'}, height=400)
    st.plotly_chart(fig_eng, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3: FOCUS GENRES DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
st.header(f"🔍 Deep Dive: {' vs '.join(selected_genres)}")

# 2x2 metrics dashboard
focus_metrics = df_focus.groupby(GENRE_COL).agg(
    Avg_Streams=(STREAM_COL, 'mean'),
    Avg_Listeners=(LISTENER_COL, 'mean'),
    Avg_Duration=(DURATION_COL, 'mean'),
    Avg_Skip_Rate=(SKIP_COL, 'mean')
).round(2).reindex(selected_genres)

fig_dash = make_subplots(rows=2, cols=2,
    subplot_titles=("Avg Total Streams (M)", "Monthly Listeners (M)",
                    "Avg Stream Duration (Min)", "Skip Rate (%)"))

for idx, (col_name, metric) in enumerate(zip(
    ['Avg_Streams', 'Avg_Listeners', 'Avg_Duration', 'Avg_Skip_Rate'],
    focus_metrics.columns)):
    row, col = idx // 2 + 1, idx % 2 + 1
    colors = [GENRE_COLORS.get(g, '#888') for g in selected_genres]
    fig_dash.add_trace(
        go.Bar(x=selected_genres, y=focus_metrics[metric].values,
               marker_color=colors, text=focus_metrics[metric].values,
               textposition='outside', texttemplate='%{text:.2f}',
               showlegend=False),
        row=row, col=col
    )

fig_dash.update_layout(height=600, title_text="Business Performance Dashboard")
st.plotly_chart(fig_dash, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4: PREMIUM CONVERSION
# ══════════════════════════════════════════════════════════════════════════════
st.header("💳 Monetisation: Free vs Premium")

col1, col2 = st.columns(2)

# Premium conversion calculation
plat = df_focus.groupby([GENRE_COL, PLATFORM_COL]).size().unstack(fill_value=0)
plat = plat.reindex(selected_genres)
plat['Total'] = plat.sum(axis=1)
plat['Premium_Pct'] = (plat['Premium'] / plat['Total'] * 100).round(1)
plat['Free_Pct'] = (plat['Free'] / plat['Total'] * 100).round(1)

with col1:
    fig_stack = go.Figure()
    fig_stack.add_trace(go.Bar(name='Free', x=selected_genres, y=plat['Free_Pct'],
                               marker_color='#BDC3C7', text=plat['Free_Pct'].apply(lambda x: f'{x:.0f}%'),
                               textposition='inside'))
    fig_stack.add_trace(go.Bar(name='Premium', x=selected_genres, y=plat['Premium_Pct'],
                               marker_color='#2ECC71', text=plat['Premium_Pct'].apply(lambda x: f'{x:.0f}%'),
                               textposition='inside'))
    fig_stack.update_layout(barmode='stack', title="Free vs Premium User Split",
                            yaxis_title="Percentage (%)", height=400)
    st.plotly_chart(fig_stack, use_container_width=True)

with col2:
    fig_prem = px.bar(
        x=selected_genres, y=plat['Premium_Pct'].values,
        color=selected_genres, color_discrete_map=GENRE_COLORS,
        title="Premium Conversion Rate",
        labels={'x': 'Genre', 'y': 'Premium %'},
        text=plat['Premium_Pct'].apply(lambda x: f'{x:.1f}%')
    )
    fig_prem.add_hline(y=50, line_dash="dash", line_color="red",
                       annotation_text="50% benchmark")
    fig_prem.update_layout(showlegend=False, yaxis_range=[0, 70], height=400)
    st.plotly_chart(fig_prem, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 5: WORLD MAP
# ══════════════════════════════════════════════════════════════════════════════
st.header("🗺️ Global Genre Map")

top_genre = df_filtered.groupby(COUNTRY_COL)[GENRE_COL].agg(
    lambda x: x.value_counts().index[0]
)

map_data = []
for country, genre in top_genre.items():
    if country in COUNTRY_COORDS:
        lat, lon = COUNTRY_COORDS[country]
        map_data.append({
            'Country': country, 'Top Genre': genre,
            'lat': lat, 'lon': lon,
            'color': GENRE_COLORS.get(genre, '#888')
        })

map_df = pd.DataFrame(map_data)

fig_map = px.scatter_geo(
    map_df, lat='lat', lon='lon', color='Top Genre',
    color_discrete_map=GENRE_COLORS,
    hover_name='Country', size_max=15,
    title="Most Popular Genre by Country",
    projection="natural earth"
)
fig_map.update_traces(marker=dict(size=12, line=dict(width=1, color='white')))
fig_map.update_layout(height=500, geo=dict(showframe=False, showcoastlines=True,
                                            coastlinecolor='lightgray'))
st.plotly_chart(fig_map, use_container_width=True)

# Regional breakdown
st.subheader("📊 Regional Genre Comparison")
region_genre = df_focus.groupby(['Region', GENRE_COL])[STREAM_COL].mean().reset_index()

fig_region = px.bar(
    region_genre, x='Region', y=STREAM_COL, color=GENRE_COL,
    color_discrete_map=GENRE_COLORS, barmode='group',
    title=f"Average Streams by Region: {' vs '.join(selected_genres)}",
    labels={STREAM_COL: 'Avg Streams (M)'}
)
fig_region.update_layout(height=400)
st.plotly_chart(fig_region, use_container_width=True)

# Country heatmap
st.subheader("🔥 Country × Genre Heatmap")
heat_data = df_filtered.groupby([COUNTRY_COL, GENRE_COL]).size().unstack(fill_value=0)

fig_heat = px.imshow(
    heat_data, color_continuous_scale='YlOrRd',
    title="Genre Concentration by Country (darker = more songs)",
    labels=dict(x="Genre", y="Country", color="Songs"),
    aspect="auto"
)
fig_heat.update_layout(height=600)
st.plotly_chart(fig_heat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 6: ADVANCED ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Advanced Analysis")

tab1, tab2, tab3 = st.tabs(["📈 Correlation", "💰 Revenue Estimation", "📅 Year Trend"])

with tab1:
    num_cols = [STREAM_COL, LISTENER_COL, DURATION_COL, SKIP_COL, HOURS_COL, RECENT_STREAM_COL]
    short_names = ['Streams', 'Listeners', 'Duration', 'Skip Rate', 'Hours', 'Recent Streams']
    corr = df_focus[num_cols].corr().round(2)
    corr.index = short_names
    corr.columns = short_names

    fig_corr = px.imshow(
        corr, color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
        title="Correlation Matrix: Engagement vs Commercial Metrics",
        text_auto='.2f', aspect='equal'
    )
    fig_corr.update_layout(height=500)
    st.plotly_chart(fig_corr, use_container_width=True)

with tab2:
    rev_data = []
    for g in selected_genres:
        sub = df_focus[df_focus[GENRE_COL] == g]
        prem_rev = sub[sub[PLATFORM_COL]=='Premium'][STREAM_COL].sum() * PREMIUM_RATE
        free_rev = sub[sub[PLATFORM_COL]=='Free'][STREAM_COL].sum() * FREE_RATE
        rev_data.append({
            'Genre': g,
            'Premium Revenue ($M)': round(prem_rev, 2),
            'Ad Revenue ($M)': round(free_rev, 2),
            'Total Revenue ($M)': round(prem_rev + free_rev, 2),
            'Revenue/Song ($M)': round((prem_rev + free_rev) / max(len(sub), 1), 2)
        })
    rev_df = pd.DataFrame(rev_data)

    st.dataframe(rev_df.set_index('Genre'), use_container_width=True)

    fig_rev = make_subplots(rows=1, cols=2,
        subplot_titles=("Total Revenue by Genre", "Revenue per Song"))

    fig_rev.add_trace(go.Bar(name='Premium', x=rev_df['Genre'],
                             y=rev_df['Premium Revenue ($M)'], marker_color='#2ECC71'), row=1, col=1)
    fig_rev.add_trace(go.Bar(name='Ad Revenue', x=rev_df['Genre'],
                             y=rev_df['Ad Revenue ($M)'], marker_color='#BDC3C7'), row=1, col=1)

    colors = [GENRE_COLORS.get(g, '#888') for g in rev_df['Genre']]
    fig_rev.add_trace(go.Bar(x=rev_df['Genre'], y=rev_df['Revenue/Song ($M)'],
                             marker_color=colors, showlegend=False,
                             text=rev_df['Revenue/Song ($M)'].apply(lambda x: f'${x:.2f}M'),
                             textposition='outside'), row=1, col=2)

    fig_rev.update_layout(barmode='stack', height=400,
                          title_text="Revenue Estimation (industry avg per-stream rates)")
    st.plotly_chart(fig_rev, use_container_width=True)

    st.caption("💡 Estimates based on ~$0.005/stream (Premium) and ~$0.002/stream (Free/Ad-supported)")

with tab3:
    yr = df_focus.groupby([RELEASE_COL, GENRE_COL]).size().reset_index(name='Count')
    yr = yr[yr[RELEASE_COL] >= 2015]

    fig_yr = px.line(
        yr, x=RELEASE_COL, y='Count', color=GENRE_COL,
        color_discrete_map=GENRE_COLORS, markers=True,
        title="Genre Release Trend (2015–2024): Songs Appearing in Top Charts",
        labels={RELEASE_COL: 'Release Year', 'Count': 'Number of Songs'}
    )
    fig_yr.update_layout(height=400)
    st.plotly_chart(fig_yr, use_container_width=True)

# Scatter plot
st.subheader("🎯 Streams vs Skip Rate")
fig_scat = px.scatter(
    df_focus, x=SKIP_COL, y=STREAM_COL, color=GENRE_COL,
    color_discrete_map=GENRE_COLORS, size=LISTENER_COL,
    hover_data=[COUNTRY_COL, 'Artist'],
    title="Does Lower Skip Rate = More Streams? (bubble size = listeners)",
    labels={SKIP_COL: 'Skip Rate (%)', STREAM_COL: 'Total Streams (M)'}
)
fig_scat.update_layout(height=500)
st.plotly_chart(fig_scat, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# SECTION 7: RECOMMENDATION
# ══════════════════════════════════════════════════════════════════════════════
st.header("💡 Investment Recommendation")

st.markdown("""
| Strategy | Recommended Genre | Why |
|----------|-------------------|-----|
| **Subscription revenue** | Rock 🎸 | Highest premium conversion (~55%) — listeners are willing to pay |
| **Engagement & replay** | R&B 💿 | Highest streams, longest duration, lowest skip rate |
| **Emerging markets** | Jazz 🎷 | Strong presence in Turkey, Mexico, South Korea |
| **Mass reach** | Pop 🎤 | Largest audience but highest skip rate — use as traffic driver |

**Bottom line:** A dual-track strategy investing in **Rock** (for subscription revenue) and **R&B** 
(for engagement-driven value) offers the best risk-adjusted return for a record label's portfolio.
""")

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    "**Data source:** Kaggle — Spotify Global Streaming Data 2024 · "
    "**Course:** ACC102 Mini Assignment · Track 4 · "
    "**Built with:** Python, Streamlit, Plotly"
)
