import streamlit as st
from back import analyze_text  # make sure backend.py is in same folder

st.set_page_config(page_title="Scam Detector", page_icon="🚨", layout="centered")

st.title("🚨 AI Scam Detector")
st.write("Enter a message below to analyze scam risk")

# Input box
msg = st.text_area("✍️ Enter message here")

# Button
if st.button("Analyze"):
    if msg.strip() == "":
        st.warning("Please enter a message first")
    else:
        result = analyze_text(msg)

        # ---------------- RESULTS ----------------
        st.subheader("📊 Resultuuuuu")

        # Label with color
        label = result["label"]
        if label == "FRAUD":
            st.error(f"🚨 {label}")
        elif label == "SUSPICIOUS":
            st.warning(f"⚠️ {label}")
        else:
            st.success(f"✅ {label}")

        st.metric("Risk Score", result["risk_score"])
        st.metric("Confidence", result["confidence"])

        st.divider()

        st.subheader("🌐 Language")
        st.write(result["language"])

        st.subheader("📝 Highlighted Message")
        st.markdown(result["highlighted_text"])

        st.subheader("🤖 Translated Text")
        st.write(result["translated_text"])

        st.subheader("📌 Reasons")
        if result["reasons"]:
            for r in result["reasons"]:
                st.write("✔", r)
        else:
            st.write("No suspicious reasons found")

        st.subheader("📊 Extracted Entities")

        entities = result["entities"]

        st.write("💳 UPI IDs:", entities["upi_ids"])
        st.write("🔗 Links:", entities["links"])
        st.write("💰 Amounts:", entities["amounts"])