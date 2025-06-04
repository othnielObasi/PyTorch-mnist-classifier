import streamlit as st
import numpy as np
import json
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import os
from dotenv import load_dotenv
from db import log_prediction, get_recent_predictions

# Load .env only locally (not in GitHub Actions)
if os.getenv("GITHUB_ACTIONS") != "true":
    from dotenv import load_dotenv
    load_dotenv()

# Use API URL from environment variable (GitHub or local)
API_ENDPOINT = os.getenv("PREDICTION_API_URL")


# Set up page config to ensure it's wide and the title is set
st.set_page_config(page_title="MNIST Digit Classifier", layout="wide")

# # Header styling
# st.markdown("""
# <style>
#     .main-title {
#         text-align: left;
#         margin-bottom: 0px;
#     }
#     .description {
#         text-align: left;
#         width: 60%;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("<h1 class='main-title'>🧠 MNIST Digit Classifier</h1>", unsafe_allow_html=True)
# st.markdown("<p class='description'>Draw a digit (0–9) below and click Predict.</p>", unsafe_allow_html=True)


st.markdown("""
<style>
    .main-title {
        text-align: left;
        margin-bottom: 0.5em;
        font-size: 2.2em;
    }
    .description {
        text-align: left;
        margin-top: 0.5em;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🧠 MNIST Digit Classifier</h1>", unsafe_allow_html=True)
st.markdown("<p class='description'>Draw a digit (0–9) below and click Predict.</p>", unsafe_allow_html=True)



canvas_col, result_col = st.columns([1, 0.9], gap="small")

# Drawing canvas column
with canvas_col:
    canvas_result = st_canvas(
        fill_color="#000000",
        stroke_width=10,
        stroke_color="#FFFFFF",
        background_color="#000000",
        height=240,
        width=240,
        drawing_mode="freedraw",
        key="canvas"
    )

    if canvas_result.image_data is not None:
        img = Image.fromarray((canvas_result.image_data[:, :, 0]).astype(np.uint8))  # Convert to grayscale
        img = img.resize((28, 28)).convert("L")
        img_array = np.array(img).astype(np.float32)
        img_array = (img_array / 255.0 - 0.1307) / 0.3081  # Normalize image (same as model preprocessing)
        pixels = img_array.tolist()

        if st.button("Predict", key="predict_button"):
            try:
                # Sending the image data for prediction
                response = requests.post(API_ENDPOINT, json={"pixels": pixels})
                response.raise_for_status()
                result = response.json()
                predicted = result["predicted"]
                confidence = round(float(result["confidence"]), 1)

                # Log prediction without true label
                log_prediction(predicted=predicted, confidence=confidence)

                # Store results in session_state for later display
                st.session_state["predicted"] = predicted
                st.session_state["confidence"] = confidence
                st.session_state["pixels"] = pixels

            except Exception as e:
                st.error(f"❌ Failed to get prediction from API: {e}")

with result_col:
    if "predicted" in st.session_state:
        st.markdown("""
        <div style='margin-left: center; margin-right: center; width: 10%; text-align: center;'>
            <div style='margin-bottom: 8px; font-weight: bold;'>🎯 Prediction: <span style="font-weight: normal;">{}</span></div>
            <div style='margin-bottom: 15px; font-weight: bold;'>Confidence: <span style="font-weight: normal;">{}%</span></div>
        </div>
        """.format(st.session_state["predicted"], st.session_state["confidence"]), unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style='border: 0px solid #ddd; padding: 10px 15px; border-radius: 10px; margin-top: 10px;'>
                <h4 style='text-align: left; margin-bottom: 10px;'>Submit Feedback</h4>
            </div>
            """, unsafe_allow_html=True)

            label_col, _ = st.columns([0.1, 0.1])
            with label_col:
                true_label = st.number_input("Enter the true label (0–9)", min_value=0, max_value=9, step=1, key="true_label")

            if st.button("Submit Feedback", key="submit_feedback"):
                log_prediction(
                    predicted=st.session_state["predicted"],
                    confidence=st.session_state["confidence"],
                    true_label=true_label
                )
                st.success("✅ Feedback submitted.")


st.markdown("""
<div style='text-align: left; margin-top: 2em;'>
    <h4 style='margin-bottom: 0.5em;'>📋 Prediction History</h4>
</div>
""", unsafe_allow_html=True)
try:
    logs = get_recent_predictions(limit=10)

    filtered_logs = [
        {
            "#": idx,
            "Timestamp": log["timestamp"],
            "Predicted": log["predicted"],
            "Confidence": f"{round(log['confidence'], 1)}%",
            "True Label": log["true_label"]
        }
        for idx, log in enumerate(logs, start=1)
        if log.get("true_label") is not None
    ]

    if filtered_logs:
        # Custom CSS
        st.markdown("""
        <style>
            .custom-table {
                margin-left: left;
                margin-right: auto;
                width: 80%;
                border-collapse: collapse;
            }
            .custom-table th, .custom-table td {
                border: 0.1px solid #ddd;
                padding: 8px;
                text-align: center;
            }
            
            .custom-table th {
                padding-top: 10px;
                padding-bottom: 10px;
               
            }
        </style>
        """, unsafe_allow_html=True)

        # Render HTML Table
        table_html = "<table class='custom-table'>"
        headers = ["#", "Timestamp", "Predicted",  "True Label", "Confidence"]
        table_html += "<tr>" + "".join([f"<th>{col}</th>" for col in headers]) + "</tr>"

        for row in filtered_logs:
            table_html += "<tr>" + "".join([f"<td>{row[col]}</td>" for col in headers]) + "</tr>"
        table_html += "</table>"

        st.markdown(table_html, unsafe_allow_html=True)

    else:
        st.info("No predictions with feedback yet.")
except Exception as e:
    st.error(f"❌ Failed to load logs.\n\n{e}")




