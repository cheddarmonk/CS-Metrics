import os
import requests
from datetime import datetime

BASE_URL = "https://api.housecallpro.com"
API_KEY = os.getenv("HOUSECALL_API_KEY")

class HousecallAPIError(Exception):
    pass


def _request(method: str, endpoint: str, **kwargs):
    """Internal helper to send an HTTP request."""
    if API_KEY is None:
        raise HousecallAPIError("Missing HOUSECALL_API_KEY environment variable")

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {API_KEY}"
    headers["Accept"] = "application/json"

    url = f"{BASE_URL}/{endpoint.lstrip('/') }"
    response = requests.request(method, url, headers=headers, **kwargs)
    if not response.ok:
        raise HousecallAPIError(
            f"Error {response.status_code} for {endpoint}: {response.text}"
        )
    return response.json()


def get_jobs(start_date: str, end_date: str):
    """Return jobs completed between start_date and end_date."""
    params = {"start": start_date, "end": end_date}
    return _request("GET", "/v2/jobs", params=params)


def get_job(job_id: str):
    """Return a specific job's details."""
    return _request("GET", f"/v2/jobs/{job_id}")


def get_technicians():
    """Return a list of technicians."""
    return _request("GET", "/v2/technicians")


def get_reviews(source: str = "housecall"):
    """Fetch reviews from HouseCall or Google.
    Source must be either 'housecall' or 'google'.
    """
    source = source.lower()
    if source not in {"housecall", "google"}:
        raise ValueError("source must be 'housecall' or 'google'")
    return _request("GET", f"/v2/reviews/{source}")


def jobs_completed_by_technician(start_date: str, end_date: str):
    """Return number of jobs completed by each technician in a date range."""
    jobs = get_jobs(start_date, end_date)
    counts = {}
    for job in jobs:
        tech_id = job.get("technician_id")
        if tech_id is None:
            continue
        counts[tech_id] = counts.get(tech_id, 0) + 1
    return counts


def technician_hours(job: dict):
    """Return the total technician hours for a job.
    Expects job to include a 'time_logs' list with entries for each technician.
    """
    total = 0.0
    for log in job.get("time_logs", []):
        start = datetime.fromisoformat(log["start"])
        end = datetime.fromisoformat(log["end"])
        total += (end - start).total_seconds() / 3600
    return total


def technician_hours_by_job(job_id: str):
    job = get_job(job_id)
    return technician_hours(job)


def earnings_by_technician(tech_id: str, start_date: str, end_date: str):
    """Return total earnings for a technician for a date range."""
    jobs = get_jobs(start_date, end_date)
    total = 0.0
    for job in jobs:
        if job.get("technician_id") == tech_id:
            total += float(job.get("amount_collected", 0))
    return total


def earnings_daily(tech_id: str, date: str):
    """Return total earnings for a technician on a single day."""
    return earnings_by_technician(tech_id, date, date)


def earnings_monthly(tech_id: str, year: int, month: int):
    """Return total earnings for a technician for a specific month."""
    start = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end = f"{year + 1:04d}-01-01"
    else:
        end = f"{year:04d}-{month + 1:02d}-01"
    return earnings_by_technician(tech_id, start, end)


def earnings_yearly(tech_id: str, year: int):
    """Return total earnings for a technician for a specific year."""
    start = f"{year:04d}-01-01"
    end = f"{year + 1:04d}-01-01"
    return earnings_by_technician(tech_id, start, end)


def earnings_year_to_date(tech_id: str):
    """Return year-to-date earnings for a technician."""
    today = datetime.utcnow().date()
    start = f"{today.year:04d}-01-01"
    end = today.isoformat()
    return earnings_by_technician(tech_id, start, end)
