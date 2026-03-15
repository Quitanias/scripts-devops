# SRE Python Scripts

This folder contains a collection of Python scripts covering common day-to-day tasks for **Site Reliability Engineers (SREs)**. The scripts are focused on AWS infrastructure management, external API consumption, and observability/monitoring routines.

---

## Scripts

### `artifact_clean.py`
Connects to **AWS ECR** and lists images that exceed a configurable retention count, identifying candidates for deletion. Preserves images tagged as `latest` or any production-critical tags. Useful for controlling registry storage costs.

### `certificate.py`
Checks the **SSL certificate expiration date** for a list of domains. Prints a status report indicating how many days remain before expiry, with a critical alert threshold at 30 days.

### `garbage_collector.py`
Scans **AWS EBS volumes** in a given region and identifies those with `available` status — meaning they are not attached to any EC2 instance and are generating unnecessary cost. Outputs a list of orphaned volumes for review.

### `github_api_consumer.py` *(previously `consumo_api.py`)*
Queries the **GitHub API** to list all public repositories for the HashiCorp organization and filters for Terraform-related repos. Demonstrates best practices for API consumption: timeout handling, HTTP error checking via `raise_for_status()`, and CI/CD-friendly exit codes.

### `log_analyzer.py` *(previously `logs_server_script.py`)*
Parses a server log file and counts **HTTP 500 errors per IP address**. Implements two approaches side-by-side: a full file read (simpler, higher memory usage) and a line-by-line read (memory-efficient, recommended for large log files).

---

## Requirements

- Python 3.8+
- `boto3` — for AWS scripts (`artifact_clean.py`, `garbage_collector.py`)
- `requests` — for API scripts (`github_api_consumer.py`)

Install dependencies with:

```bash
pip install boto3 requests
```

> **Note:** AWS scripts require valid credentials configured via `aws configure` or environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
