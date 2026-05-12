import streamlit as st
import pandas as pd
import feedparser
import os
from datetime import datetime

# ================= 1. initialize =================
st.set_page_config(page_title="ATMP Intelligence Monitor", layout="wide")

MASTER_FILE = "master_regulations.csv"  # Original database
# add RSS link
RSS_FEEDS = {
    "FDA (Biologics)": "https://www.fda.gov/about-fda/contact-fda/get-email-updates/rss-feeds/biologics/rss.xml",
    "EMA (Updates)": "https://www.ema.europa.eu/en/whats-new.xml"
}
# define the key words
KEYWORDS = ["TCR", "T-cell", "Gene Therapy", "ATMP", "Cell Therapy", "Regenerative"]

# Initize the functional
if not os.path.exists(MASTER_FILE):
    pd.DataFrame(columns=["Input_Date", "Area", "Part", "Guideline_Name", "Past_Requirement", "Latest_Update", "TCR_T_Impact"]).to_csv(MASTER_FILE, index=False)

# ================= 2. functional =================

# RSS scan and compare
    def scan_rss():
    alerts = []
    # read the database and compare
    try:
        db = pd.read_csv(MASTER_FILE)
        existing_guidelines = db['Guideline_Name'].fillna("").tolist()
    except:
        existing_guidelines = []

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            # filter keywords
            if any(key.lower() in entry.title.lower() for key in KEYWORDS):
                # Automatich compare
                status = "🆕 NEW REGULATION"
                for existing in existing_guidelines:
                    if existing.lower() in entry.title.lower() or entry.title.lower() in existing.lower():
                        status = "⚠️ POTENTIAL UPDATE (Match Found)"
                        break
                
                alerts.append({
                    "Source": source,
                    "Title": entry.title,
                    "Link": entry.link,
                    "Published": entry.get('published', 'N/A'),
                    "Status": status
                })
    return alerts

# ================= 3. Streamlit UI Interface =================

st.title("🛡️ ATMP Global Regulatory Intelligence Monitor")
st.markdown(f"**Current Focus:** TCR T-cell Therapies | **Keywords:** {', '.join(KEYWORDS)}")

# --- sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    p_type = st.text_input("Current Product Type", "TCR T-cell therapies")
    st.divider()
    if st.button("🔄 Refresh RSS Feeds"):
        st.cache_data.clear()
    st.write("This tool monitors FDA/EMA for updates and helps with Gap Analysis.")

# --- First part：RSS Live Alerts ---
st.header("📡 Live Alerts (Auto-Filtered)")
alerts = scan_rss()

if alerts:
    for alert in alerts:
        with st.container():
            col_a, col_b = st.columns([4, 1])
            with col_a:
                color = "#ff4b4b" if "UPDATE" in alert['Status'] else "#28a745"
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>[{alert['Status']}]</span> **{alert['Source']}**", unsafe_allow_html=True)
                st.markdown(f"**{alert['Title']}**")
                st.caption(f"Published: {alert['Published']} | [Link to Official Doc]({alert['Link']})")
            with col_b:
                # click Import the topic will save to session_state
                if st.button("📝 Import Info", key=alert['Title']):
                    st.session_state['import_title'] = alert['Title']
            st.divider()
else:
    st.info("No relevant updates found in current RSS feeds.")

# --- Part II：Gap Analysis & data input ---
st.header("✍️ Analysis & Data Entry")
with st.expander("➕ Open Entry Form (Gap Analysis)"):
    # automatic imput (RSS click Import)
    default_title = st.session_state.get('import_title', "")
    
    c1, c2 = st.columns(2)
    with c1:
        in_area = st.selectbox("Area", ["USA (FDA)", "Europe (EMA)", "Japan (PMDA)", "UK (MHRA)", "ICH"])
        in_title = st.text_input("Guideline Name", value=default_title)
    with c2:
        in_part = st.selectbox("Part", ["CMC (Quality)", "Non-Clinical", "Clinical", "Regulatory"])
        in_date = st.date_input("Effective Date")

    c3, c4 = st.columns(2)
    with c3:
        in_past = st.text_area("Past Requirement (Old)")
    with c4:
        in_latest = st.text_area("Latest Update (New)")
    
    in_impact = st.text_area(f"Specific Impact on {p_type}")

    if st.button("💾 Save Analysis to Database"):
        new_row = pd.DataFrame([{
            "Input_Date": datetime.now().strftime("%Y-%m-%d"),
            "Area": in_area,
            "Part": in_part,
            "Guideline_Name": in_title,
            "Past_Requirement": in_past,
            "Latest_Update": in_latest,
            "TCR_T_Impact": in_impact
        }])
        new_row.to_csv(MASTER_FILE, mode='a', header=False, index=False)
        st.success("Entry successfully saved!")

# --- part III：database and output---
st.header("📊 Regulatory Knowledge Base")
if os.path.exists(MASTER_FILE):
    df_db = pd.read_csv(MASTER_FILE)
    if not df_db.empty:
        # filters
        f_area = st.multiselect("Filter by Area", df_db['Area'].unique(), default=df_db['Area'].unique())
        filtered_view = df_db[df_db['Area'].isin(f_area)]
        
        st.dataframe(filtered_view, use_container_width=True)
        
        # output Excel butten
        if st.button("📥 Export Current View to Excel"):
            excel_name = f"ATMP_Report_{datetime.now().strftime('%Y%m%d')}.xlsx"
            filtered_view.to_excel(excel_name, index=False)
            st.success(f"Generated: {excel_name}")
    else:
        st.write("Database is empty.")
