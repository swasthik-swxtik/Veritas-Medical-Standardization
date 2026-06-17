import json

file_path = "sample-data/Sample_JSON_file2.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

document_id = data["data"]["documentId"]

print("Document ID:", document_id)
print("-" * 50)

for section in data["data"]["responseDetails"]:

    if section["classifier"] == "lab_report":

        report_details = section["data"]["report_details"]

        for test in report_details:
            print(
                test["test_name"],
                "|",
                test["result"],
                "|",
                test["unit"]
            )