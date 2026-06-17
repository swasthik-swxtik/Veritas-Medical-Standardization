import json
import sqlite3
import os
import shutil

from validator import validate_result


# Load test mappings
with open("config/test_name_mapping.json", "r") as file:
    mappings = json.load(file)

# Load unit mappings
with open("config/unit_mapping.json", "r") as file:
    unit_mappings = json.load(file)


def standardize_test_name(test_name):

    for canonical_name, aliases in mappings.items():

        if test_name in aliases:
            return canonical_name

    return test_name


def standardize_unit(unit):

    return unit_mappings.get(unit, unit)


# Create failed_files folder if it doesn't exist
os.makedirs(
    "failed_files",
    exist_ok=True
)

# Connect to SQLite
conn = sqlite3.connect("database/medical.db")
cursor = conn.cursor()

# Read all JSON files
for filename in os.listdir("sample-data"):

    if filename.endswith(".json"):

        file_path = os.path.join(
            "sample-data",
            filename
        )

        try:

            print(
                f"Processing: {filename}"
            )

            with open(
                file_path,
                "r"
            ) as file:

                data = json.load(file)

            document_id = data["data"]["documentId"]

            # Duplicate document check
            cursor.execute("""
            SELECT
            (
                SELECT COUNT(*)
                FROM lab_results
                WHERE document_id = ?
            )
            +
            (
                SELECT COUNT(*)
                FROM discharge_summaries
                WHERE document_id = ?
            )
            """, (document_id, document_id))

            exists = cursor.fetchone()[0]

            if exists > 0:

                print(
                    f"Skipping duplicate document: "
                    f"{document_id}"
                )

                continue

            for section in data["data"]["responseDetails"]:

                # LAB REPORTS
                if section["classifier"] == "lab_report":

                    report_details = section["data"]["report_details"]

                    for test in report_details:

                        original_name = test["test_name"]

                        standardized_name = standardize_test_name(
                            original_name
                        )

                        result = test["result"]

                        unit = standardize_unit(
                            test["unit"]
                        )

                        validation_status = validate_result(
                            result,
                            standardized_name,
                            unit
                        )

                        cursor.execute("""
                        INSERT INTO lab_results (
                            document_id,
                            test_name,
                            result,
                            unit,
                            validation_status
                        )
                        VALUES (?, ?, ?, ?, ?)
                        """, (
                            document_id,
                            standardized_name,
                            result,
                            unit,
                            validation_status
                        ))

                # DISCHARGE SUMMARY
                elif section["classifier"] == "discharge_summary":

                    discharge = section["data"]

                    cursor.execute("""
                    INSERT INTO discharge_summaries (
                        document_id,
                        patient_name,
                        age,
                        gender,
                        diagnosis,
                        admission_date,
                        discharge_date,
                        hospital_name,
                        doctor_name
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        document_id,
                        discharge.get("patientName"),
                        discharge.get("age"),
                        discharge.get("gender"),
                        discharge.get("diagnosis"),
                        discharge.get("admissionDate"),
                        discharge.get("dischargeDate"),
                        discharge.get("hospitalName"),
                        discharge.get("doctorName")
                    ))

        except Exception as e:

            print(
                f"FAILED FILE: {filename}"
            )

            print(
                f"ERROR: {e}"
            )

            shutil.move(
                file_path,
                os.path.join(
                    "failed_files",
                    filename
                )
            )

            print(
                f"Moved {filename} "
                f"to failed_files/"
            )

            continue

conn.commit()

print(
    "All files processed successfully!"
)

conn.close()