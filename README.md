# 🎵 Genre Investment Analyser

An interactive data product for record label A&R teams to compare music genre performance across streaming volume, listener engagement, monetisation potential, and regional preferences.

**🔗 Live App:** [Click here to open the Streamlit app](https://your-app-url.streamlit.app)  
**🎥 Demo Video:** [1–3 minute walkthrough](https://your-video-link)

---

## 1. Problem & User

**Target User:** A&R (Artist & Repertoire) decision-makers at a record label, responsible for deciding which music genres to invest in.

**Core Question:** Among all music genres on Spotify's global platform, which genres offer the best commercial return — and should the label prioritise streaming volume, listener engagement, or paid subscription revenue?

## 2. Data

- **Source:** [Kaggle — Spotify Global Streaming Data 2024](https://www.kaggle.com/datasets/atharvasoundankar/spotify-global-streaming-data-2024)
- **Access Date:** April 2026
- **Size:** 500 rows × 12 columns, covering 20 countries and 10 genres
- **Key fields:** Total Streams, Monthly Listeners, Avg Stream Duration, Skip Rate, Platform Type (Free/Premium), Country

## 3. Methods

1. Full-landscape scan of all 10 genres using pandas `groupby` aggregation
2. Deep-dive into 4 focus genres (Pop, R&B, Rock, Jazz) — user-configurable via sidebar
3. Premium conversion rate analysis via cross-tabulation of Genre × Platform Type
4. Regional analysis with geographic mapping (Plotly scatter_geo)
5. Correlation matrix of engagement vs commercial metrics
6. Revenue estimation using industry per-stream rates ($0.005 Premium / $0.002 Free)
7. Release year trend analysis

## 4. Key Findings

- **R&B** has the highest average streams and lowest skip rate — strongest listener loyalty
- **Rock** has the highest premium conversion rate (~55%) — listeners most willing to pay
- **Jazz** shows surprisingly strong presence in non-traditional markets (Turkey, Mexico, South Korea)
- **Pop** delivers the widest reach but has the highest skip rate — best used as a traffic driver
- **Recommendation:** Dual-track investment in Rock (subscription revenue) + R&B (engagement value)

## 5. How to Run

### Option A: Visit the live app
Click the Streamlit link above — no installation needed.

### Option B: Run locally
```bash
git clone https://github.com/YOUR_USERNAME/acc102-genre-investment.git
cd acc102-genre-investment
pip install -r requirements.txt
streamlit run app.py
```

## 6. Project Structure

```
├── app.py                                        # Streamlit interactive tool
├── ACC102_Genre_Investment_Analysis.ipynb         # Python notebook (full analysis)
├── Cleaned_Spotify_2024_Global_Streaming_Data.csv # Dataset
├── requirements.txt                              # Python dependencies
├── figures/                                      # Exported chart images
└── README.md                                     # This file
```

## 7. Limitations & Next Steps

- Single-year dataset (2024) — multi-year trends would strengthen the investment case
- 500 observations across 20 countries is a limited sample
- Spotify does not operate in China — Asia-Pacific analysis uses proxy markets (Japan, South Korea, India, Indonesia)
- Per-stream revenue rates are industry estimates, not actual Spotify payouts
- **Next steps:** Add time-series data, incorporate artist-level granularity, connect to Spotify API for live data
