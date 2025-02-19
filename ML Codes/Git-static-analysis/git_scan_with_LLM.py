import os
import shutil
import json
import requests
import boto3
import concurrent.futures
import urllib3
from botocore.client import Config

# ---------- Configuration ----------

# LLM API endpoint and headers
API_URL = "http://192.168.1.10:8080/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}

# Disable SSL warnings (for testing purposes only)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# MinIO/S3 Configuration
MINIO_URL = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin12345"

# S3 Buckets
REPO_BUCKET = "github-repos"  # Repository storage bucket
SCAN_BUCKET = "repo-scans"    # Vulnerability scan reports bucket

# Initialize S3 Client
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

# ---------- Utility Functions ----------

def ensure_bucket(bucket_name):
    """Ensure the specified S3 bucket exists; if not, create it."""
    existing_buckets = s3.list_buckets()
    if bucket_name not in [bucket["Name"] for bucket in existing_buckets["Buckets"]]:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created.")

def is_text_file(file_path):
    """
    Heuristic: read the first 1024 bytes in binary mode.
    If a null byte is found, treat it as binary.
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False
    except Exception:
        return False
    return True

# ---------- LLM Vulnerability Scanner ----------

def scan_file_for_vulnerabilities(file_path, code):
    """
    Sends the file's content to the LLM vulnerability scanning API.
    Uses verify=False to disable SSL verification (for testing).
    Returns the API response (expected as a JSON string).
    note: If you dont find any vulnerabilities in the code, you can return a blank string or space.
    """
    payload = {
        "model": "lily-cybersecurity-7b-v0.2",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Scan the following file for security vulnerabilities and generate fixes. "
                    "Return the results in JSON format with the following fields:\n\n"
                    "- vulnerability_id (it should be according to the vulnerability_type id)\n"
                    "- vulnerability_type(select for this array ['A01:2021-Broken Access Control', 'A02:2021-Cryptographic Failures', 'A03:2021-Injection', 'A04:2021-Insecure Design', 'A05:2021-Security Misconfiguration', 'A06:2021-Vulnerable and Outdated Components', 'A07:2021-Identification and Authentication Failures', 'A08:2021-Software and Data Integrity Failures', 'A09:2021-Security Logging and Monitoring Failures', 'A10:2021-Server-Side Request Forgery', 'A11:2021-Insecure Serialization', 'Miscellaneous'])\n"
                    "- title\n"
                    "- severity\n"
                    "- location (include file path and line number)\n"
                    "- description\n"
                    "- recommendation\n\n"
                    f"File path: {file_path}\n\n"
                    "Source Code:\n" + code
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload), verify=False)
        if response.status_code == 200:
            content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            return content
        else:
            print(f"Failed to scan {file_path}. Status code: {response.status_code}")
            return ""
    except Exception as e:
        print(f"Exception while scanning {file_path}: {e}")
        return ""

def process_file(file_path):
    """
    Processes a single file:
      - Skips non-text files and files in the .git folder or with unwanted extensions.
      - Reads the file content.
      - Calls the LLM vulnerability scanner.
      - Returns a parsed JSON result (or raw text) enriched with file path info.
    """
    try:
        # Skip binary files
        if not is_text_file(file_path):
            print(f"Skipping binary file: {file_path}")
            return None
        # Skip non-source files (e.g., .pyc files or anything in a .git folder)
        if file_path.endswith(".pyc") or ".git" in file_path:
            print(f"Skipping non-source file: {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
        print(f"Scanning file: {file_path}...")
        result = scan_file_for_vulnerabilities(file_path, code)
        if result:
            try:
                parsed_result = json.loads(result)
                if "location" not in parsed_result:
                    parsed_result["location"] = {"file_path": file_path, "line": parsed_result.get("line", "N/A")}
                elif isinstance(parsed_result["location"], str):
                    parsed_result["location"] = {"file_path": file_path, "line": parsed_result.get("line", "N/A")}
                return parsed_result
            except Exception as e:
                print(f"Error parsing vulnerability result for {file_path}: {e}")
                return {"file_path": file_path, "raw_response": result}
        else:
            return None
    except Exception as e:
        print(f"Skipping file {file_path} due to error: {e}")
        return None

# ---------- Repository Scanner using S3 and Multithreading ----------

def scan_repository_with_llm(unique_folder):
    """
    Downloads a repository from S3, iterates over every file (recursively),
    sends each file's content to the LLM vulnerability scanning API (waiting for its response),
    and aggregates any detected vulnerabilities in a JSON report.
    The final JSON report is then uploaded to the designated S3 bucket.
    
    Returns the S3 path to the uploaded JSON report (if any vulnerabilities are detected) or None.
    """
    ensure_bucket(SCAN_BUCKET)
    temp_dir = f"/tmp/{unique_folder}"
    os.makedirs(temp_dir, exist_ok=True)
    print(f"Downloading repository '{unique_folder}' from S3...")

    objects = s3.list_objects_v2(Bucket=REPO_BUCKET, Prefix=f"{unique_folder}/")
    if "Contents" not in objects:
        print(f"Repository '{unique_folder}' not found in S3.")
        return None

    # Download files from S3, preserving directory structure.
    for obj in objects["Contents"]:
        s3_key = obj["Key"]
        relative_path = s3_key[len(unique_folder) + 1 :]  # Remove the repository folder prefix.
        local_path = os.path.join(temp_dir, relative_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        print(f"Downloading {s3_key} -> {local_path}")
        s3.download_file(REPO_BUCKET, s3_key, local_path)

    print(f"Repository downloaded to: {temp_dir}")

    vulnerability_results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for root, _, files in os.walk(temp_dir):
            for filename in files:
                full_path = os.path.join(root, filename)
                futures.append(executor.submit(process_file, full_path))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                vulnerability_results.append(result)

    report_s3_path = None
    # Only create the report if vulnerabilities were detected.
    if vulnerability_results:
        report_json_path = f"/tmp/{unique_folder}_vuln_report.json"
        with open(report_json_path, "w", encoding="utf-8") as report_file:
            json.dump(vulnerability_results, report_file, indent=4)
        print(f"Vulnerability report saved at: {report_json_path}")
        s3.upload_file(report_json_path, SCAN_BUCKET, f"{unique_folder}_vuln_report.json")
        print(f"Vulnerability report uploaded to S3 bucket '{SCAN_BUCKET}' as '{unique_folder}_vuln_report.json'")
        report_s3_path = f"s3://{SCAN_BUCKET}/{unique_folder}_vuln_report.json"
    else:
        print("No vulnerabilities detected in the repository.")

    # Cleanup temporary files.
    shutil.rmtree(temp_dir, ignore_errors=True)
    return report_s3_path

def list_scan_reports():
    """Lists all vulnerability scan reports stored in S3."""
    objects = s3.list_objects_v2(Bucket=SCAN_BUCKET)
    if "Contents" in objects:
        for obj in objects["Contents"]:
            print(obj["Key"])
    else:
        print("No scan reports found.")

def delete_scan_report(unique_folder):
    """Deletes a vulnerability scan report from S3."""
    try:
        s3.delete_object(Bucket=SCAN_BUCKET, Key=f"{unique_folder}_vuln_report.json")
        print(f"Deleted scan report: {unique_folder}_vuln_report.json")
    except Exception as e:
        print(f"Error deleting scan report: {e}")

# ---------- Example Usage ----------

if __name__ == "__main__":
    UNIQUE_FOLDER = "greenCurve_af297ba3"  # Example repository folder in S3
    report_path = scan_repository_with_llm(UNIQUE_FOLDER)
    if report_path:
        print(f"Vulnerability report available at: {report_path}")
    list_scan_reports()
