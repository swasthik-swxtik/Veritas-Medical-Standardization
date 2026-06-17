# Medical Data Standardization Pipeline

## Overview

The Medical Data Standardization Pipeline is a Python-based solution for processing, standardizing, validating, and analyzing medical laboratory and discharge summary data from JSON files.

The system performs:

* Medical JSON ingestion
* Test name standardization
* Unit normalization
* Validation and outlier detection
* Duplicate document detection
* Fault tolerance handling
* SQLite data storage
* Streamlit dashboard visualization
* Excel export generation

---

## Features

### Data Ingestion

* Reads medical JSON files from the `sample-data` directory.
* Supports laboratory reports and discharge summaries.

### Standardization

* Standardizes test names using configurable mappings.
* Standardizes measurement units using configurable mappings.

### Validation

* Invalid value detection.
* Unit validation.
* Outlier detection using configurable thresholds.

### Duplicate Detection

* Prevents duplicate processing using `document_id`.

### Fault Tolerance

* Failed files are isolated for review.
* Processing of one failed file does not stop the entire pipeline.

### Database Storage

* Stores processed records in SQLite.

### Dashboard

* Interactive Streamlit dashboard.
* JSON file upload functionality.
* Validation metrics and visualizations.
* Discharge summary visualization.

### Export

* Generates Excel output for downstream analysis.

---

## Architecture

The complete architecture documentation is available in:

```text
docs/architecture.md
```

---

## Project Structure

```text
Veritas-Medical-Standardization
│
├── config
│   ├── outlier_rules.json
│   ├── test_name_mapping.json
│   ├── test_unit_rules.json
│   └── unit_mapping.json
│
├── database
│   └── medical.db
│
├── docs
│   ├── architecture.md
│   ├── assumptions.md
│   └── image.png
│
├── sample-data
│   ├── Sample_JSON_file1.json
│   ├── Sample_JSON_file2.json
│   ├── Sample_JSON_file3.json
│   ├── Sample_JSON_file4.json
│   ├── Sample_JSON_file5.json
│   └── test-data.json
│
├── src
│   ├── create_db.py
│   ├── dashboard.py
│   ├── export.py
│   ├── main.py
│   ├── parser.py
│   ├── standardizer.py
│   └── validator.py
│
└── tests
```

---

## Technologies Used

* Python
* SQLite
* Streamlit
* Pandas
* OpenPyXL

---

## How to Run

### Create Database

```bash
python src/create_db.py
```

### Process Medical Files

```bash
python src/main.py
```

### Launch Dashboard

```bash
streamlit run src/dashboard.py
```

### Export Data

```bash
python src/export.py
```

---

## Validation Status Categories

| Status  | Description                     |
| ------- | ------------------------------- |
| VALID   | Record passed validation checks |
| INVALID | Record failed validation checks |
| OUTLIER | Record contains abnormal values |

---

## Assumptions

Project assumptions are documented in:

```text
docs/assumptions.md
```

---


