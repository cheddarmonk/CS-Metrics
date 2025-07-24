# CS-Metrics

This repository contains simple utilities for interacting with the
[Housecall Pro](https://www.housecallpro.com) API. The `housecall_api.py`
module provides helper functions for retrieving job details, technician
hours and earnings, and customer reviews.

## Installation

1. Install Python 3.8+.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your Housecall Pro API token as an environment variable:
   ```bash
   export HOUSECALL_API_KEY="your-api-key"
   ```

## Usage

Import the module in your Python code and call the desired functions:

```python
from housecall_api import (
    jobs_completed_by_technician,
    technician_hours_by_job,
    earnings_daily,
    earnings_monthly,
    earnings_year_to_date,
    get_reviews,
)

jobs = jobs_completed_by_technician("2025-07-01", "2025-07-31")
print(jobs)

hours = technician_hours_by_job("JOB_ID")
print(hours)

money = earnings_year_to_date("TECH_ID")
print(money)

google_reviews = get_reviews("google")
```

All functions raise `HousecallAPIError` if the API request fails.
