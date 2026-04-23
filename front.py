import streamlit as st
from back import analyze_text

st.title("🚨 Scam Detector")

msg = st.text_area("Enter message")

if st.button("Analyze"):
    result = analyze_text(msg)

    st.write("Label:", result["label"])
    st.write("Risk Score:", result["risk_score"])