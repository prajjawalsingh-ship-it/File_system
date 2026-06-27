# File Processing Platform

A Python tool for counting records in CSV, JSON, and XML files. Designed for speed, thread-safety, and easy extension.

## Supported Python Versions

- **Python 3.8 to 3.12+**

## Test Coverage

The platform is built with a strong focus on reliability, reaching **81% overall test coverage**:

- **Processor Factory**: 100%
- **JSON Processor**: 81%
- **XML Processor**: 91%
- **CSV Processor**: 82%

## What it Does (Detailed Workflow)

1.  **Entry**: Pass `file_type` and `file_content` to `process_file`.
2.  **Smart Allocation**: Uses a **Thread-Safe Singleton** factory to reuse processor instances.
3.  **Validation**: Ensures structural integrity (headers for CSV, arrays for JSON).
4.  **Hardened Counting**: Skips empty objects, whitespace-only lines, and empty tags.
5.  **Logging**: Successes and errors are recorded via a clean, configurable logger.

## Setup & Running

### Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run

```bash
python3 src/main.py
```

### Test & Coverage

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
# Run tests
python3 -m pytest tests/test_processors.py
# Run coverage report
python3 -m pytest --cov=src tests/test_processors.py
```
