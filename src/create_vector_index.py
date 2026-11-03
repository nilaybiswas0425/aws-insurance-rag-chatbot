import boto3

# AWS configuration
region = "us-east-1"

session = boto3.Session(region_name=region)

# Create AWS STS client to get the account_id
sts=session.client("sts")
account_id=sts.get_caller_identity()["Account"]
print(account_id)

# Create bucket name
vector_bucket_name=f"insurance-rag-vector-bucket-{account_id}"
print(vector_bucket_name)

s3vectors = session.client("s3vectors")

# Create vector index
response = s3vectors.create_index(
    vectorBucketName=vector_bucket_name,
    indexName="insurance-policy-index",
    dataType="float32",
    dimension=1024,
    distanceMetric="cosine",
    metadataConfiguration={
        "nonFilterableMetadataKeys": [
            "AMAZON_BEDROCK_TEXT",
            "AMAZON_BEDROCK_METADATA"
        ]
    }
)

print("Vector index created successfully!")
print(response)