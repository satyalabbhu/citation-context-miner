# streamlit_app.py

import streamlit as st
import pandas as pd
import sys
import os
import time

# Fix backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))
from get_citations import get_citing_papers
from analyze_context import analyze_context

# --- Page Setup ---
st.set_page_config(page_title="Citation Context Miner", layout="wide")
st.title("📘 Citation Context Miner")
st.markdown("Use AI to explore **how** a paper is cited in other research — praised, extended, or criticized.")

# --- Input Field ---
doi_input = st.text_input("🔗 Enter DOI", placeholder="e.g., 10.1016/j.lisr.2020.101015")

# --- Process on Input ---
if doi_input:
    with st.spinner("🔄 Fetching citing papers and analyzing context..."):
        papers = get_citing_papers(doi_input.strip())

        if not papers:
            st.warning("⚠️ No citing papers found, or DOI is not indexed in OpenAlex.")
        else:
            results = []

            for paper in papers:
                title = paper.get("title", "")
                abstract_data = paper.get("abstract", {})
                if not abstract_data:
                    continue

                # Reconstruct abstract from OpenAlex inverted index
                words = []
                for word, pos_list in abstract_data.items():
                    for pos in pos_list:
                        words.append((pos, word))
                abstract = ' '.join([w for _, w in sorted(words)])

                analysis = analyze_context(abstract)

                results.append({
                    "Title": title,
                    "Summary": analysis["summary"],
                    "Sentiment": analysis["sentiment"],
                    "Confidence": round(analysis["confidence"] * 100, 2)
                })

            # Convert to DataFrame
            df = pd.DataFrame(results)

            # Highlight rows based on sentiment
            def highlight_sentiment(row):
                if row.Sentiment == "POSITIVE":
                    return ['background-color: #d4edda'] * len(row)
                elif row.Sentiment == "NEGATIVE":
                    return ['background-color: #f8d7da'] * len(row)
                else:
                    return ['background-color: #f0f0f0'] * len(row)

            st.subheader("📊 Citation Summary Table")
            st.dataframe(df.style.apply(highlight_sentiment, axis=1), use_container_width=True)
