# 🎵 Genre Investment Analyser
### A Data-Driven Tool for Record Label A&R Decision-Making

**🔗 Live App:** [https://acc102-minitask-cnz6volhvpvni7uhngvfun.streamlit.app](https://acc102-minitask-cnz6volhvpvni7uhngvfun.streamlit.app)  
**🎥 Demo Video:** *(link to be added after recording)*  
**📓 Notebook:** `ACC102_Genre_Investment_Analysis_v2.ipynb`

---

## 1. Problem & User

**Target user:** A&R (Artist & Repertoire) managers at a record label who decide which music genres to invest in and which artists to sign.

**Core question:** Among all genres on Spotify's global platform — Pop, R&B, Rock, Jazz and beyond — which genres offer the best commercial return? Should the label prioritise streaming volume, listener engagement, premium conversion, or regional expansion?

---

## 2. Data

| Field | Detail |
|-------|--------|
| **Source** | [Kaggle — Spotify Global Streaming Data 2024](https://www.kaggle.com/datasets/atharvasoundankar/spotify-global-streaming-data-2024) |
| **Access date** | April 2026 |
| **Size** | 500 rows × 12 columns |
| **Coverage** | 20 countries · 10 genres · multiple artists and albums |

**Key fields used:**
- `Total Streams (Millions)` — core commercial volume metric
- `Monthly Listeners (Millions)` — audience reach
- `Avg Stream Duration (Min)` — engagement depth
- `Skip Rate (%)` — listener retention quality
- `Platform Type` (Free / Premium) — monetisation potential
- `Total Hours Streamed (Millions)` — catalogue value indicator
- `Streams Last 30 Days (Millions)` — current momentum
- `Country` — regional market analysis

**Derived metrics (computed in Python):**
- `Engagement_Ratio` = Hours Streamed ÷ Total Streams
- `Momentum_Pct` = Recent Streams ÷ Total Streams × 100
- `Revenue_Est` = Streams × per-stream rate ($0.005 Premium / $0.002 Free)

---

## 3. Methods

1. **Data loading & feature engineering** — loaded CSV with pandas, computed three derived metrics and mapped countries to world regions
2. **Full landscape scan** — analysed all 10 genres using `groupby` aggregation before narrowing focus
3. **Genre scorecard** — normalised all metrics (0–1) and built a heatmap scorecard
4. **Deep dive on focus genres** — radar chart, 2×2 metrics dashboard, free vs premium split
5. **Artist-level analysis** — top artists per genre, market concentration (top-3 stream share), box plots
6. **Album & engagement analysis** — engagement ratio ranking and violin distribution plots
7. **Regional analysis** — world map, country×genre heatmap, regional grouped bar charts
8. **Revenue estimation & momentum** — dollar estimates using industry per-stream rates
9. **Correlation analysis** — lower-triangle correlation matrix across all key metrics

**Tools:** Python · pandas · numpy · matplotlib · seaborn · plotly · streamlit

---

## 4. Key Findings

- **R&B** generates the highest average streams and lowest skip rate — most loyal and engaged listeners
- **Rock** has the highest premium conversion (~55%) — strongest driver of subscription revenue
- **Jazz** is niche but shows strong presence in non-traditional markets (Turkey, Mexico, South Korea) with high premium conversion (~47%)
- **Pop** has the widest reach but highest skip rate — better as a traffic driver than core investment
- **Market concentration** in R&B and Rock is moderate, leaving room for new signings
- **Asia-Pacific** shows Jazz performing better than expected in South Korea and Indonesia

---

## 5. How to Run

### Option A — Live app (no installation needed)
Click the Streamlit link above. Select any genre combination, filter by country, and explore all 6 analysis tabs.

### Option B — Run locally
```bash
git clone https://github.com/langwei528/ACC102-MINITASK.git
cd ACC102-MINITASK
pip install -r requirements.txt
streamlit run app.py
```

---

## 6. Product Link / Demo

| Product | Link |
|---------|------|
| **Streamlit app** | [acc102-minitask.streamlit.app](https://acc102-minitask-cnz6volhvpvni7uhngvfun.streamlit.app) |
| **Notebook** | `ACC102_Genre_Investment_Analysis_v2.ipynb` |
| **Demo video** | *(link to be added)* |

**App features:** 6 tabs · radar chart · bubble chart · lollipop · box plot · violin plot · world map · all interactive (Plotly)

---

## 7. Limitations & Next Steps

**Limitations:**
- Single-year snapshot (2024) — multi-year data would confirm trend direction
- 500 observations across 20 countries is a limited sample
- Spotify not available in China — Asia-Pacific uses proxy markets (Japan, South Korea, India, Indonesia)
- Per-stream revenue figures are industry estimates, not actual Spotify payouts
- Genre labels follow Spotify metadata, which may not match standard industry definitions

**Next steps:**
- Incorporate 3-year historical data to validate momentum signals
- Add artist-level revenue breakdown for individual signing decisions
- Connect to Spotify Web API for live data refresh
- Include label affiliation data to benchmark major vs independent labels

---

## Repository Structure

```
ACC102-MINITASK/
├── app.py                                         # Streamlit interactive tool
├── ACC102_Genre_Investment_Analysis_v2.ipynb      # Python analysis notebook
├── Cleaned_Spotify_2024_Global_Streaming_Data.csv # Dataset
├── requirements.txt                               # Dependencies
└── README.md                                      # This file
```

---

*ACC102 Mini Assignment · 2nd Semester 2024–25 · Xi'an Jiaotong-Liverpool University*
