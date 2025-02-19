import os
import shutil
import uuid
import boto3
from git import Repo
from botocore.client import Config

# MinIO Configuration
MINIO_URL = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin12345"
BUCKET_NAME = "github-repos"

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
        print(f"Bucket '{BUCKET_NAME}' created.")

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
        print(f"Cloning {github_url} into {temp_dir}...")
        Repo.clone_from(clone_url, temp_dir)
        
        # Upload repository files
        for root, _, files in os.walk(temp_dir):
            for file in files:
                local_path = os.path.join(root, file)
                s3_path = os.path.relpath(local_path, temp_dir)  # Relative path for S3
                
                # Upload to S3
                s3.upload_file(local_path, BUCKET_NAME, f"{unique_folder}/{s3_path}")
                print(f"Uploaded {s3_path} to S3")

        print(f"Repository '{repo_name}' uploaded as '{unique_folder}' successfully.")

    except Exception as e:
        print(f"Error cloning or uploading repo: {e}")

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
                print(obj["Key"])  # Print full path
        else:
            print(f"No files found in repository '{unique_folder}'.")

    except Exception as e:
        print(f"Error listing files: {e}")

# 3. Delete a Repository
def delete_repository(unique_folder):
    """Deletes an entire repository folder from S3."""
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{unique_folder}/")
        if "Contents" in objects:
            for obj in objects["Contents"]:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj["Key"])
                print(f"Deleted {obj['Key']}")

            print(f"Repository '{unique_folder}' deleted successfully.")
        else:
            print(f"No repository found with name '{unique_folder}'.")

    except Exception as e:
        print(f"Error deleting repository: {e}")

# Example Usage
if __name__ == "__main__":
    GITHUB_URL = "https://github.com/sanketugale/greenCurve.git"
    USERNAME = "sanketugale"
    ACCESS_TOKEN = ""

    # Step 1: Upload repository
    upload_github_repo(GITHUB_URL, USERNAME, ACCESS_TOKEN)

    # Step 2: List files in repository
    repo_name = GITHUB_URL.split("/")[-1].replace(".git", "")
    unique_folder = f"GreenCurve-APIs_bc30848c"  # Replace with actual ID printed earlier
    list_repository_files(unique_folder)

    # Step 3: Delete repository
    # delete_repository(unique_folder)
