import sqlite3
import pandas as pd
import streamlit as st
import os
import subprocess
import json

st.set_page_config(
    page_title="Medical Data Standardization Dashboard",
    layout="wide"
)

st.title("Medical Data Standardization Dashboard")

# Upload Section
st.subheader("Upload Medical JSON File")

uploaded_file = st.file_uploader(
    "Drag and drop a JSON file",
    type=["json"]
)

if uploaded_file is not None:

    try:

        # Validate JSON
        json.loads(
            uploaded_file.getvalue().decode("utf-8")
        )

        save_path = os.path.join(
            "sample-data",
            uploaded_file.name
        )

        # Check duplicate file
        if os.path.exists(save_path):

            st.warning(
                f"{uploaded_file.name} already exists in sample-data!"
            )

        else:

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(
                f"{uploaded_file.name} uploaded successfully!"
            )

            if st.button("Process Uploaded File"):

                subprocess.run(
                    ["python", "src/main.py"]
                )

                st.success(
                    "File processed successfully!"
                )

                st.rerun()

    except Exception:

        st.error(
            "Invalid JSON file! Please upload a valid JSON."
        )

st.divider()

# Connect to database
conn = sqlite3.connect("database/medical.db")

# Load lab results
df = pd.read_sql_query(
    "SELECT * FROM lab_results",
    conn
)

# Load discharge summaries
discharge_df = pd.read_sql_query(
    "SELECT * FROM discharge_summaries",
    conn
)

conn.close()

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Records",
        len(df)
    )

with col2:
    st.metric(
        "Valid Records",
        len(
            df[
                df["validation_status"]
                == "VALID"
            ]
        )
    )

with col3:
    st.metric(
        "Invalid Records",
        len(
            df[
                df["validation_status"]
                == "INVALID"
            ]
        )
    )

with col4:
    st.metric(
        "Outlier Records",
        len(
            df[
                df["validation_status"]
                == "OUTLIER"
            ]
        )
    )

st.divider()

# Lab Results
st.subheader("Lab Results")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# Validation Status Distribution
st.subheader("Validation Status Distribution")

status_counts = (
    df["validation_status"]
    .value_counts()
)

st.bar_chart(status_counts)

st.divider()

# Top Test Names
st.subheader("Top Test Names")

test_counts = (
    df["test_name"]
    .value_counts()
    .head(15)
)

st.bar_chart(test_counts)

st.divider()

# Discharge Summaries
st.subheader("Discharge Summaries")

st.metric(
    "Discharge Summary Records",
    len(discharge_df)
)

st.dataframe(
    discharge_df,
    use_container_width=True
)