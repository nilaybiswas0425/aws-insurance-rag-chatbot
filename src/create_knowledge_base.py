import boto3

# AWS configuration
region = "us-east-1"

# Create AWS session
session = boto3.Session(region_name=region)

# Create client
bedrock_agent = session.client("bedrock-agent")
s3vectors = session.client("s3vectors")
sts = session.client("sts")

# Get AWS account ID
account_id = sts.get_caller_identity()["Account"]

print("AWS Account:", account_id)
print("Bedrock Agent client created successfully!")

# Name assignment
knowledge_base_name = "insurance-rag-knowledge-base"
vector_bucket_name = f"insurance-rag-vector-bucket-{account_id}"
vector_index_name = "insurance-policy-index"

# Setup arn
# Existing IAM execution role
role_arn = (
    f"arn:aws:iam::{account_id}:"
    "role/AmazonBedrockExecutionRoleForInsuranceKB"
)

# Embedding model
embedding_model_arn = (
    f"arn:aws:bedrock:{region}::foundation-model/"
    "amazon.titan-embed-text-v2:0"
)

# Retrieve vector bucket details
bucket_response = s3vectors.get_vector_bucket(
    vectorBucketName=vector_bucket_name
)

vector_bucket_arn = bucket_response["vectorBucket"]["vectorBucketArn"]

# Retrieve vector index details
index_response = s3vectors.get_index(
    vectorBucketName=vector_bucket_name,
    indexName=vector_index_name
)

index_arn = index_response["index"]["indexArn"]

print("Vector Bucket ARN:", vector_bucket_arn)
print("Vector Index ARN:", index_arn)
print("Embedding Dimension:", index_response["index"]["dimension"])

# Knowledge Base embedding configuration
knowledge_base_configuration = {
    "type": "VECTOR",
    "vectorKnowledgeBaseConfiguration": {
        "embeddingModelArn": embedding_model_arn,
        "embeddingModelConfiguration": {
            "bedrockEmbeddingModelConfiguration": {
                "dimensions": 1024,
                "embeddingDataType": "FLOAT32"
            }
        }
    }
}

# S3 Vectors storage configuration
storage_configuration = {
    "type": "S3_VECTORS",
    "s3VectorsConfiguration": {
        "indexArn": index_arn
    }
}

# Create Bedrock Knowledge Base
response = bedrock_agent.create_knowledge_base(
    name=knowledge_base_name,
    description="Insurance policy RAG Knowledge Base using Amazon S3 Vectors",
    roleArn=role_arn,
    knowledgeBaseConfiguration=knowledge_base_configuration,
    storageConfiguration=storage_configuration
)

# Capture Knowledge Base details
knowledge_base = response["knowledgeBase"]

knowledge_base_id = knowledge_base["knowledgeBaseId"]
knowledge_base_arn = knowledge_base["knowledgeBaseArn"]

print("Knowledge Base creation initiated!")
print("Knowledge Base ID:", knowledge_base_id)
print("Knowledge Base ARN:", knowledge_base_arn)
print("Status:", knowledge_base["status"])