# CS-Metrics

This repository provides a small helper module for fetching data from the [Housecall Pro](https://www.housecallpro.com) API. It demonstrates how to retrieve job statistics, technician earnings, and customer reviews.

## Getting Started

The steps below outline how to set up and run the code either on your local computer or inside Codex.

### 1. Clone the repository

```bash
git clone <repo-url>
cd CS-Metrics
```

### 2. Create a Python environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set the Housecall Pro API token

Export your API token so the helper can authenticate requests:

```bash
export HOUSECALL_API_KEY="your-api-key"
```

### 5. Use the helper module

You can import the module in your own scripts or interactively with Python:

```python
from housecall_api import jobs_completed_by_technician, technician_hours_by_job

# example usage
print(jobs_completed_by_technician("2025-07-01", "2025-07-31"))
print(technician_hours_by_job("JOB_ID"))
```

## Running inside Codex

If you are working in the Codex environment, open a terminal in the repository directory and run the same commands as above. The API token must still be set with `export HOUSECALL_API_KEY`. Once the dependencies are installed you can run any script that imports `housecall_api.py`.

## Notes

- All functions raise `HousecallAPIError` if an API request fails.
- The module is intended as a simple example and does not cover every endpoint provided by Housecall Pro.
