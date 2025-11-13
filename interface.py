import streamlit as st
from ultralytics import YOLO
import os
import json

# Import functions from your core script
from tp_index1 import index_all_videos, search_keyword_in_results, RESULTS_JSON # type: ignore

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="🎥 Video Indexer", layout="wide")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #fdfdfd;
    }
    body {
        background-color: #fdfdfd;
        color: #2c3e50;
    }
    .title {
        font-size: 2.8em;
        color: #2c3e50;
        font-weight: bold;
    }
    .subtitle {
        color: #566573;
        font-size: 1.3em;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 0.6rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# --- HEADER ---
st.markdown("<p class='title'>🎥 Smart Video Indexing & Search</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Index videos, extract frames and audio, detect objects, and search via text or object labels.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- MAIN SECTION ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Actions")

    if st.button("📁 Index All Videos"):
        with st.spinner("Indexing all videos. Please wait..."):
            index_all_videos()
        st.success("✅ Indexing complete!")

    show_json = st.checkbox("📂 Show raw JSON results")

with col2:
    st.subheader("🔍 Search")

    keyword = st.text_input("Enter a keyword to search (e.g. 'person', 'dog', 'hello')")

    if st.button("🔎 Search"):              
        if keyword.strip():
            with st.spinner(f"Searching for '{keyword}'..."):
                results = search_keyword_in_results(keyword)
            if results:
                st.success(f"Found {len(results)} result(s) for '{keyword}'")
                for res in results:
                    with st.expander(f"{res['type'].capitalize()} match in: {os.path.basename(res['video'])}"):
                        if res["type"] == "text":
                            st.write(f"📝 **Text**: {res['text']}")
                            st.write(f"🕒 **Time**: {res['time']:.2f} sec")
                            if res.get("frame"):
                                st.image(res["frame"], caption="Frame at time of speech", use_column_width=True)

                        elif res["type"] == "object":
                            st.write(f"🎯 **Detected Objects**: {', '.join(res['objects'])}")
                            st.write(f"🕒 **Time**: {res.get('time', 0):.2f} sec")
                            st.image(res["frame"], caption="Detected Frame", use_column_width=True)

            else:
                st.warning("No matches found.")
        else:
            st.error("Please enter a keyword.")

# --- RAW JSON VIEW ---
if show_json:
    st.subheader("📦 Raw JSON Results")
    if os.path.exists(RESULTS_JSON):
        with open(RESULTS_JSON, "r") as f:
            st.json(json.load(f))
    else:
        st.error("No JSON file found. Please run indexing first.")
