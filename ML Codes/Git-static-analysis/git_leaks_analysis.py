import os
import shutil
import subprocess
import json
import pandas as pd
import boto3
from botocore.client import Config

# MinIO/S3 Configuration
MINIO_URL = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin12345"

# S3 Buckets
REPO_BUCKET = "github-repos"  # Stores GitHub/GitLab repos
SCAN_BUCKET = "repo-scans"    # Stores scan reports

# Initialize S3 Client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

# Ensure buckets exist
def ensure_bucket(bucket_name):
    existing_buckets = s3.list_buckets()
    if bucket_name not in [bucket["Name"] for bucket in existing_buckets["Buckets"]]:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")

# 1️⃣ UNIVERSAL FUNCTION TO SCAN REPOSITORY
def scan_repository_from_s3(unique_folder):
    """
    Downloads a repository from S3, runs a Gitleaks scan,
    and uploads the vulnerability report back to S3.
    
    Args:
        unique_folder (str): The repository's unique name in S3.
    
    Returns:
        str: S3 path to the uploaded scan report, or None if no vulnerabilities are found.
    """
    ensure_bucket(SCAN_BUCKET)

    temp_dir = f"/tmp/{unique_folder}"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Downloading repository '{unique_folder}' from S3...")

    # Fetch all objects under the repo folder
    objects = s3.list_objects_v2(Bucket=REPO_BUCKET, Prefix=f"{unique_folder}/")
    if "Contents" not in objects:
        print(f"Repository '{unique_folder}' not found in S3.")
        return None

    # Download repository from S3 and preserve directory structure
    for obj in objects["Contents"]:
        s3_key = obj["Key"]
        # Remove the repository folder prefix (e.g. "MindCare-APIs_bc30848c/")
        relative_path = s3_key[len(unique_folder) + 1 :]
        local_path = os.path.join(temp_dir, relative_path)

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading {s3_key} -> {local_path}")
        s3.download_file(REPO_BUCKET, s3_key, local_path)

    print(f"Repository downloaded to: {temp_dir}")

    # Run Gitleaks scan using the directory mode
    scan_report = f"/tmp/{unique_folder}_scan.json"
    csv_report = f"/tmp/{unique_folder}_scan.csv"

    try:
        print(f"Running Gitleaks scan on {temp_dir}...")
        # Using "gitleaks dir" mode to scan the downloaded repo directory.
        command = f"gitleaks dir -v {temp_dir} -f json -r {scan_report}"
        result = subprocess.run(command, shell=True)

        # Gitleaks returns 0 if no leaks, 1 if leaks are found.
        if result.returncode not in [0, 1]:
            print(f"Gitleaks encountered an error. Exit code: {result.returncode}")
            return None

        if not os.path.exists(scan_report):
            print("Error: Gitleaks scan report not found.")
            return None

        # Read and parse the JSON output
        with open(scan_report, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in Gitleaks report.")
                return None

        if not data:
            print("Scan report is empty (No vulnerabilities found).")
            return None

        # Extract relevant details from each finding using the documented keys
        findings = []
        for leak in data:
            findings.append({
                "file_name": leak.get("File", "N/A"),
                "line_number": leak.get("Line", "N/A"),
                "secret": leak.get("Secret", "N/A"),
                "rule_id": leak.get("RuleID", "N/A"),
                "entropy": leak.get("Entropy", "N/A"),
                "commit": leak.get("Commit", "N/A")
            })

        if not findings:
            print("No valid vulnerabilities found.")
            return None

        # Save findings to CSV
        df = pd.DataFrame(findings)
        df.to_csv(csv_report, index=False)
        print(f"Converted scan report to CSV: {csv_report}")

        # Upload the CSV report to S3
        s3.upload_file(csv_report, SCAN_BUCKET, f"{unique_folder}_scan.csv")
        print(f"Scan report uploaded to S3 bucket '{SCAN_BUCKET}' as '{unique_folder}_scan.csv'")

        return f"s3://{SCAN_BUCKET}/{unique_folder}_scan.csv"

    except Exception as e:
        print(f"Error running Gitleaks: {e}")
        return None

    finally:
        # Cleanup local storage
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(scan_report):
            os.remove(scan_report)
        if os.path.exists(csv_report):
            os.remove(csv_report)

# 2️⃣ List Scan Reports
def list_scan_reports():
    """Lists all scan reports stored in S3."""
    objects = s3.list_objects_v2(Bucket=SCAN_BUCKET)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            print(obj["Key"])
    else:
        print("No scan reports found.")

# 3️⃣ Delete a Scan Report
def delete_scan_report(unique_folder):
    """Deletes a scan report from S3."""
    try:
        s3.delete_object(Bucket=SCAN_BUCKET, Key=f"{unique_folder}_scan.csv")
        print(f"Deleted scan report: {unique_folder}_scan.csv")
    except Exception as e:
        print(f"Error deleting scan report: {e}")

# Example Usage
if __name__ == "__main__":
    UNIQUE_FOLDER = "greenCurve_af297ba3"  # Example repository folder in S3

    report_path = scan_repository_from_s3(UNIQUE_FOLDER)
    if report_path:
        print(f"Vulnerability report saved at: {report_path}")

    list_scan_reports()
