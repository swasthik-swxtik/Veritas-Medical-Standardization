# Assumptions Document

## Project Assumptions

### Input Data

* Input files are provided in JSON format.
* Each document contains a unique document_id.
* The JSON structure follows the format provided in the assignment samples.

### Standardization

* Test names are standardized using mappings defined in config/test_name_mapping.json.
* Units are standardized using mappings defined in config/unit_mapping.json.
* Any unmapped test name is retained as received from the source file.

### Validation

* Expected units for laboratory tests are defined in config/test_unit_rules.json.
* Outlier thresholds are defined in config/outlier_rules.json.
* Null, empty, N/A, NA, NULL, and NONE values are treated as INVALID.

### Duplicate Handling

* Duplicate documents are identified using document_id.
* Duplicate documents are skipped during processing.

### Fault Tolerance

* Failure while processing one file should not stop processing of other files.
* Failed files are moved to the failed_files folder for later review.

### Storage

* SQLite is used as the local database for storing processed records.
* Lab reports and discharge summaries are stored in separate database tables.

### Dashboard & Export

* Streamlit is used for data visualization and file upload functionality.
* Processed data can be exported to Excel format for downstream analysis.