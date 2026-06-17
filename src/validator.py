import json

# Load outlier rules
with open(
    "config/outlier_rules.json",
    "r"
) as file:

    outlier_rules = json.load(file)

# Load unit validation rules
with open(
    "config/test_unit_rules.json",
    "r"
) as file:

    unit_rules = json.load(file)


def validate_result(
    result,
    test_name,
    unit
):

    # Missing value validation
    if result is None:
        return "INVALID"

    result = str(result).strip()

    if result == "":
        return "INVALID"

    if result.upper() in [
        "N/A",
        "NA",
        "NULL",
        "NONE"
    ]:
        return "INVALID"

    # Outlier range validation
    if test_name in outlier_rules:

        try:

            value = float(result)

            min_value = outlier_rules[
                test_name
            ]["min"]

            max_value = outlier_rules[
                test_name
            ]["max"]

            if (
                value < min_value
                or
                value > max_value
            ):
                return "OUTLIER"

        except:
            pass

    # Unit validation
    if test_name in unit_rules:

        allowed_units = unit_rules[
            test_name
        ]

        if unit not in allowed_units:
            return "OUTLIER"

    return "VALID"