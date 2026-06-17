import json

# Load mappings
with open("config/test_name_mapping.json", "r") as file:
    mappings = json.load(file)


def standardize_test_name(test_name):
    for canonical_name, aliases in mappings.items():
        if test_name in aliases:
            return canonical_name
    return test_name


# Load JSON file
with open("sample-data/Sample_JSON_file2.json", "r") as file:
    data = json.load(file)

# Find lab report
for section in data["data"]["responseDetails"]:

    if section["classifier"] == "lab_report":

        report_details = section["data"]["report_details"]

        for test in report_details:

            original_name = test["test_name"]

            standardized_name = standardize_test_name(original_name)

            print(f"Original: {original_name}")
            print(f"Standardized: {standardized_name}")
            print("-" * 40)