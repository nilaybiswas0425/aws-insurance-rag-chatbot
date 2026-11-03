import boto3

region = "us-east-1"

knowledge_base_id = "E1RNVKEBQF"
data_source_id = "TJKRHQLM2S"

session = boto3.Session(region_name=region)

bedrock_agent = session.client("bedrock-agent")

response = bedrock_agent.get_data_source(
    knowledgeBaseId=knowledge_base_id,
    dataSourceId=data_source_id
)

data_source = response["dataSource"]

print("Data Source Name:", data_source["name"])
print("Data Source Status:", data_source["status"])
print("Data Deletion Policy:", data_source["dataDeletionPolicy"])