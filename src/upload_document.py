import boto3
from pathlib import Path

# Create AWS session
region="us-east-1"
session=boto3.Session(region_name=region)

# Create AWS STS client to get the account_id

sts=session.client("sts")
account_id=sts.get_caller_identity()["Account"]
bucket_name=f"rag-chatbot-kb-s3vector-{account_id}"

print(bucket_name)

# Create AWS s3 client and upload the file
base_dir=Path(__file__).resolve().parents[1]

file_absolute_path=next((base_dir/"data").glob("*.txt"))

file_name=file_absolute_path.name

s3=session.client("s3")

s3_key=f"insurance/{file_name}"

print(s3_key)

s3.upload_file(  str(file_absolute_path),bucket_name,s3_key)