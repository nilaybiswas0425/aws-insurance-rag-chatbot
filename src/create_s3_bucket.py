import boto3

# Get the AWS account ID for the current configured credentials.
region="us-east-1"

# Create AWS session
session=boto3.Session(region_name=region)

# Create AWS client
sts=session.client("sts")

# Get AWS account ID

response=sts.get_caller_identity()
account_id = response["Account"]

# Create S3 Bucket
bucket_name=f"rag-chatbot-kb-s3vector-{account_id}"

s3=session.client("s3")
s3.create_bucket(Bucket=bucket_name)