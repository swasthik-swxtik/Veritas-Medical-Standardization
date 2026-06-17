import sqlite3
import pandas as pd
import json

# Load canonical tests
with open("config/test_name_mapping.json", "r") as file:
    mappings = json.load(file)

canonical_tests = list(mappings.keys())

# Connect to database
conn = sqlite3.connect("database/medical.db")

# Load lab results
lab_df = pd.read_sql_query(
    """
    SELECT
        document_id,
        test_name,
        result,
        unit,
        validation_status
    FROM lab_results
    """,
    conn
)

# Load discharge summaries
discharge_df = pd.read_sql_query(
    """
    SELECT
        document_id,
        patient_name,
        age,
        gender,
        diagnosis,
        admission_date,
        discharge_date,
        hospital_name,
        doctor_name
    FROM discharge_summaries
    """,
    conn
)

conn.close()

output_rows = []

for document_id in lab_df["document_id"].unique():

    doc_df = lab_df[
        lab_df["document_id"] == document_id
    ]

    row = {
        "document_id": document_id
    }

    # Add discharge summary information
    patient_info = discharge_df[
        discharge_df["document_id"] == document_id
    ]

    if not patient_info.empty:

        patient_info = patient_info.iloc[0]

        row["patient_name"] = patient_info["patient_name"]
        row["age"] = patient_info["age"]
        row["gender"] = patient_info["gender"]
        row["diagnosis"] = patient_info["diagnosis"]
        row["admission_date"] = patient_info["admission_date"]
        row["discharge_date"] = patient_info["discharge_date"]
        row["hospital_name"] = patient_info["hospital_name"]
        row["doctor_name"] = patient_info["doctor_name"]

    else:

        row["patient_name"] = ""
        row["age"] = ""
        row["gender"] = ""
        row["diagnosis"] = ""
        row["admission_date"] = ""
        row["discharge_date"] = ""
        row["hospital_name"] = ""
        row["doctor_name"] = ""

    # Create blank columns for all canonical tests
    for test in canonical_tests:

        test_col = (
            test.upper()
            .replace(" ", "_")
            .replace("-", "_")
        )

        row[f"{test_col}_RESULT"] = ""
        row[f"{test_col}_UNIT"] = ""
        row[f"{test_col}_ANALYTICS"] = ""

    # Populate matching tests
    for _, record in doc_df.iterrows():

        if record["test_name"] not in canonical_tests:
            continue

        test_col = (
            record["test_name"]
            .upper()
            .replace(" ", "_")
            .replace("-", "_")
        )

        row[f"{test_col}_RESULT"] = record["result"]
        row[f"{test_col}_UNIT"] = record["unit"]
        row[f"{test_col}_ANALYTICS"] = record["validation_status"]

    output_rows.append(row)

# Create final dataframe
wide_df = pd.DataFrame(output_rows)

# Export to Excel
wide_df.to_excel(
    "output_fixed_schema_v3.xlsx",
    index=False
)

print(
    f"Exported {len(wide_df)} documents "
    f"to output_fixed_schema_v3.xlsx"
)

print(
    f"Total Columns: {len(wide_df.columns)}"
)