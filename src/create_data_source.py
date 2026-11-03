
import boto3

region = "us-east-1"

session = boto3.Session(region_name=region)

bedrock_agent = session.client("bedrock-agent")
sts = session.client("sts")

account_id = sts.get_caller_identity()["Account"]

source_bucket_name = (
    f"rag-chatbot-kb-s3vector-{account_id}"
)

response = bedrock_agent.create_data_source(
    knowledgeBaseId="E1RNVKEBQF",
    name="insurance-policy-s3-source",
    description="insurance-policy-s3-source for RAG",

    dataSourceConfiguration={
        "type": "S3",
        "s3Configuration": {
            "bucketArn": f"arn:aws:s3:::{source_bucket_name}",
            "inclusionPrefixes": [
                "insurance/"
            ],
           "bucketOwnerAccountId": account_id
        }
    },

    dataDeletionPolicy="DELETE",

    vectorIngestionConfiguration={
        "chunkingConfiguration": {
            "chunkingStrategy": "FIXED_SIZE",
            "fixedSizeChunkingConfiguration": {
                "maxTokens": 200,
                "overlapPercentage": 20
            }
        }
    }
)

data_source = response["dataSource"]

print("Data source creation initiated!")
print("Data Source ID:", data_source["dataSourceId"])
print("Data Source Name:", data_source["name"])
print("Status:", data_source["status"])