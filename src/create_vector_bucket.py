import boto3

# Create AWS session
region="us-east-1"
session=boto3.Session(region_name=region)

# Create AWS STS client to get the account_id
sts=session.client("sts")
account_id=sts.get_caller_identity()["Account"]
print(account_id)

# Create bucket name
vector_bucket_name=f"insurance-rag-vector-bucket-{account_id}"
print(vector_bucket_name)

s3vector=session.client("s3vectors")

response=s3vector.create_vector_bucket(vectorBucketName=vector_bucket_name)

print(response)