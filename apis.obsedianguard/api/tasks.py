import json
import os
import time
from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import send_mail
import random

from obsedianguard import config
from .models import Testing, User
from django.template import loader
from django_celery_beat.models import PeriodicTask
from obsedianguard.celery import app
from celery import Celery
import os
import shutil
import uuid
import boto3
from git import Repo
from botocore.client import Config
import logging
import concurrent.futures
import urllib3
import requests

import pandas as pd
import subprocess



from decouple import config

logger = logging.getLogger(__name__)

@shared_task(bind=True)
def CloneRepoTask(self, data):
    MINIO_URL = config('MINIO_URL')
    ACCESS_KEY = config('MINIO_ACCESS_KEY')
    SECRET_KEY = config('MINIO_SECRET_KEY')
    BUCKET_NAME = config('MINIO_BUCKET')

    # Initialize S3 Client
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    # Ensure bucket exists
    def ensure_bucket():
        existing_buckets = s3.list_buckets()
        if BUCKET_NAME not in [bucket["Name"] for bucket in existing_buckets["Buckets"]]:
            s3.create_bucket(Bucket=BUCKET_NAME)
            logger.info(f"Bucket '{BUCKET_NAME}' created.")

    # 1. Upload GitHub Repository to MinIO
    def upload_github_repo(github_url, username, access_token):
        """Clones a GitHub repo and uploads it to MinIO."""
        ensure_bucket()

        # Generate a unique folder name
        repo_name = github_url.split("/")[-1].replace(".git", "")
        unique_folder = f"{repo_name}_{uuid.uuid4().hex[:8]}"  # Append unique ID
        
        # Clone repository
        temp_dir = f"/tmp/{unique_folder}"
        clone_url = f"https://{username}:{access_token}@{github_url.replace('https://', '')}"
        
        try:
            logger.info(f"Cloning {github_url} into {temp_dir}...")
            Repo.clone_from(clone_url, temp_dir)
            
            # Upload repository files
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    local_path = os.path.join(root, file)
                    s3_path = os.path.relpath(local_path, temp_dir)  # Relative path for S3
                    
                    # Upload to S3
                    s3.upload_file(local_path, BUCKET_NAME, f"{unique_folder}/{s3_path}")
                    logger.info(f"Uploaded {s3_path} to S3")

            logger.info(f"Repository '{repo_name}' uploaded as '{unique_folder}' successfully.")
            return unique_folder


        except Exception as e:
            logger.info(f"Error cloning or uploading repo: {e}")

        finally:
            # Cleanup temp directory
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    # 2. List All Files in a Repository
    def list_repository_files(unique_folder):
        """Lists all files and subfolders inside a specific repository."""
        try:
            objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{unique_folder}/")
            
            if "Contents" in objects:
                for obj in objects["Contents"]:
                    logger.info(obj["Key"])  # logger.info full path
            else:
                logger.info(f"No files found in repository '{unique_folder}'.")

        except Exception as e:
            logger.info(f"Error listing files: {e}")

    # 3. Delete a Repository
    def delete_repository(unique_folder):
        """Deletes an entire repository folder from S3."""
        try:
            objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{unique_folder}/")
            if "Contents" in objects:
                for obj in objects["Contents"]:
                    s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                    logger.info(f"Deleted {obj['Key']}")

                logger.info(f"Repository '{unique_folder}' deleted successfully.")
            else:
                logger.info(f"No repository found with name '{unique_folder}'.")

        except Exception as e:
            logger.info(f"Error deleting repository: {e}")

    # Example Usage
    logger.info(data)
    data = json.loads(data)
    GITHUB_URL = data['source_url'] #"https://github.com/sanketugale/greenCurve.git"
    USERNAME = data['repo_username'] #"sanketugale"
    ACCESS_TOKEN = data['repo_token']


    # Step 1: Upload repository
    folder_name = upload_github_repo(GITHUB_URL, USERNAME, ACCESS_TOKEN)
    Testing.objects.filter(pk=data['test_id']).update(repo_folder_name=folder_name, testing_status='Cloning')
    data['folder_name'] = folder_name
    LLMtestingTask.delay(data)
    # GitLeaksTestingTask.delay(data)
    # CVEscanTestingTask.delay(data)
    Testing.objects.filter(pk=data['test_id']).update(repo_folder_name=folder_name, testing_status='InProgress')
    return f"{folder_name} Created Successfully & started with the testing ✅"


    

    # Step 2: List files in repository
    # repo_name = GITHUB_URL.split("/")[-1].replace(".git", "")
    # unique_folder = f"GreenCurve-APIs_bc30848c"  # Replace with actual ID logger.infoed earlier
    # list_repository_files(unique_folder)

    # Step 3: Delete repository
    # delete_repository(unique_folder)



@shared_task(bind=True)
def LLMtestingTask(self, data):

    # code for LLM testing
    API_URL = config('LLM_API_URL')
    HEADERS = {"Content-Type": "application/json"}

    # Disable SSL warnings (for testing purposes only)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # MinIO/S3 Configuration
    MINIO_URL = config('MINIO_URL')
    ACCESS_KEY = config('MINIO_ACCESS_KEY')
    SECRET_KEY = config('MINIO_SECRET_KEY')

    # S3 Buckets
    REPO_BUCKET = config('MINIO_BUCKET')  # Repository storage bucket
    SCAN_BUCKET = config('SCAN_BUCKET')    # Vulnerability scan reports bucket

    # Initialize S3 Client
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name=config('S3_REGION'),
    )

    # ---------- Utility Functions ----------

    def ensure_bucket(bucket_name):
        """Ensure the specified S3 bucket exists; if not, create it."""
        existing_buckets = s3.list_buckets()
        if bucket_name not in [bucket["Name"] for bucket in existing_buckets["Buckets"]]:
            s3.create_bucket(Bucket=bucket_name)
            logger.info(f"Bucket '{bucket_name}' created.")

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
            "model": config('LLM_MODEL_NAME'),
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Scan the following file for security vulnerabilities and generate fixes. "
                        "Return the results in JSON format with the following fields:\n\n"
                        "- id (it should be according to the vulnerability_type id)\n"
                        "- vulnerability_type(select for this array ['A01:2021-Broken Access Control', 'A02:2021-Cryptographic Failures', 'A03:2021-Injection', 'A04:2021-Insecure Design', 'A05:2021-Security Misconfiguration', 'A06:2021-Vulnerable and Outdated Components', 'A07:2021-Identification and Authentication Failures', 'A08:2021-Software and Data Integrity Failures', 'A09:2021-Security Logging and Monitoring Failures', 'A10:2021-Server-Side Request Forgery', 'A11:2021-Insecure Serialization', 'Miscellaneous'])\n"
                        "- title\n"
                        "- severity\n"
                        "- location (include file path and line number)\n"
                        "- description\n"
                        "- fix (suggets correct code)\n\n"
                        "- tips (provide additional information to the developer)\n\n"
                        f"File path: {file_path}\n\n"
                        "vulnerableCode:\n" + code
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
                logger.info(f"Failed to scan {file_path}. Status code: {response.status_code}")
                return ""
        except Exception as e:
            logger.info(f"Exception while scanning {file_path}: {e}")
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
                logger.info(f"Skipping binary file: {file_path}")
                return None
            # Skip non-source files (e.g., .pyc files or anything in a .git folder)
            if file_path.endswith(".pyc") or ".git" in file_path:
                logger.info(f"Skipping non-source file: {file_path}")
                return None

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            logger.info(f"Scanning file: {file_path}...")
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
                    logger.info(f"Error parsing vulnerability result for {file_path}: {e}")
                    return {"file_path": file_path, "raw_response": result}
            else:
                return None
        except Exception as e:
            logger.info(f"Skipping file {file_path} due to error: {e}")
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
        logger.info(f"Downloading repository '{unique_folder}' from S3...")

        objects = s3.list_objects_v2(Bucket=REPO_BUCKET, Prefix=f"{unique_folder}/")
        if "Contents" not in objects:
            logger.info(f"Repository '{unique_folder}' not found in S3.")
            return None

        # Download files from S3, preserving directory structure.
        for obj in objects["Contents"]:
            s3_key = obj["Key"]
            relative_path = s3_key[len(unique_folder) + 1 :]  # Remove the repository folder prefix.
            local_path = os.path.join(temp_dir, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            logger.info(f"Downloading {s3_key} -> {local_path}")
            s3.download_file(REPO_BUCKET, s3_key, local_path)

        logger.info(f"Repository downloaded to: {temp_dir}")

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
            logger.info(f"Vulnerability report saved at: {report_json_path}")
            s3.upload_file(report_json_path, SCAN_BUCKET, f"{unique_folder}_vuln_report.json")
            logger.info(f"Vulnerability report uploaded to S3 bucket '{SCAN_BUCKET}' as '{unique_folder}_vuln_report.json'")
            report_s3_path = f"s3://{SCAN_BUCKET}/{unique_folder}_vuln_report.json"
        else:
            logger.info("No vulnerabilities detected in the repository.")

        # Cleanup temporary files.
        shutil.rmtree(temp_dir, ignore_errors=True)
        return report_s3_path

    def list_scan_reports():
        """Lists all vulnerability scan reports stored in S3."""
        objects = s3.list_objects_v2(Bucket=SCAN_BUCKET)
        if "Contents" in objects:
            for obj in objects["Contents"]:
                logger.info(obj["Key"])
        else:
            logger.info("No scan reports found.")

    def delete_scan_report(unique_folder):
        """Deletes a vulnerability scan report from S3."""
        try:
            s3.delete_object(Bucket=SCAN_BUCKET, Key=f"{unique_folder}_vuln_report.json")
            logger.info(f"Deleted scan report: {unique_folder}_vuln_report.json")
        except Exception as e:
            logger.info(f"Error deleting scan report: {e}")

    # ---------- Example Usage ----------


    UNIQUE_FOLDER = data['folder_name']  # Example repository folder in S3
    report_path = scan_repository_with_llm(UNIQUE_FOLDER)
    if report_path:
        logger.info(f"Vulnerability report available at: {report_path}")
    list_scan_reports()


    testing_obj = Testing.objects.get(pk=data['test_id'])
    if testing_obj.test_count<2:
        testing_obj.test_count += 1
        testing_obj.LLM_test_result = report_path
        testing_obj.save()
    else:
        Testing.objects.filter(pk=data['test_id']).update(testing_status='Completed', LLM_test_result=report_path)

    return f"{data} \n\n =========================== LLM Testing Done Successfully ✅ ==========================="







@shared_task(bind=True)
def GitLeaksTestingTask(self, data):

    # code for GitLeaks testing
     # MinIO/S3 Configuration
    MINIO_URL = config('MINIO_URL')
    ACCESS_KEY = config('MINIO_ACCESS_KEY')
    SECRET_KEY = config('MINIO_SECRET_KEY')

    # S3 Buckets
    REPO_BUCKET = config('MINIO_BUCKET')  # Repository storage bucket
    SCAN_BUCKET = config('SCAN_BUCKET')    # Vulnerability scan reports bucket

    # Initialize S3 Client
    s3 = boto3.client(
        "s3",
        endpoint_url=MINIO_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name=config('S3_REGION'),
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

        temp_dir = f"/tmp/a/{unique_folder}"
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
        scan_report = f"/tmp/a/{unique_folder}_scan.json"
        csv_report = f"/tmp/a/{unique_folder}_scan.csv"

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

    UNIQUE_FOLDER = data['folder_name'] 
    report_path = scan_repository_from_s3(UNIQUE_FOLDER)
    if report_path:
        print(f"Vulnerability report saved at: {report_path}")

    # list_scan_reports()

    testing_obj = Testing.objects.get(pk=data['test_id'])
    if testing_obj.test_count<2:
        testing_obj.test_count += 1
        testing_obj.GitLeaks_test_result = report_path
        testing_obj.save()
    else:
        Testing.objects.filter(pk=data['test_id']).update(testing_status='Completed', GitLeaks_test_result=report_path)
    return f"{data} \n\n =========================== GitLeaks Testing Done Successfully ✅ ==========================="

@shared_task(bind=True)
def NuclieTestingTask(self, data):

    return f"{data} \n\n =========================== Nuclie Testing Done Successfully ✅ ==========================="

@shared_task(bind=True)
def CVEscanTestingTask(self, data):

    # code for CVEscan testing
    time.sleep(15)

    testing_obj = Testing.objects.get(pk=data['test_id'])
    if testing_obj.test_count<2:
        testing_obj.test_count += 1
        testing_obj.CVEscan_test_result = ""
        testing_obj.save()
    else:
        Testing.objects.filter(pk=data['test_id']).update(testing_status='Completed', CVEscan_test_result="")
    return f"{data} \n\n =========================== CVEscan Testing Done Successfully ✅ ==========================="