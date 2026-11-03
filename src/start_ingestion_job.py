
import boto3

region = "us-east-1"

session = boto3.Session(region_name=region)

bedrock_agent = session.client("bedrock-agent")

response = bedrock_agent.start_ingestion_job(
    knowledgeBaseId="E1RNVKEBQF",
    dataSourceId="TJKRHQLM2S"
)

ingestion_job = response["ingestionJob"]

print("Ingestion Job ID:", ingestion_job["ingestionJobId"])
print("Status:", ingestion_job["status"])
