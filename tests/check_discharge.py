import json

with open("sample-data/Sample_JSON_file4.json", "r") as f:
    data = json.load(f)

for section in data["data"]["responseDetails"]:
    if section["classifier"] == "lab_report":
        for test in section["data"]["report_details"]:
            if "40.60" in str(test.get("result", "")):
                print(test)