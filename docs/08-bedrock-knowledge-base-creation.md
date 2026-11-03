# 08 – Bedrock Knowledge Base Creation Using Boto3

## 1. Objective

Create an Amazon Bedrock Knowledge Base using Python Boto3 and connect it to an existing Amazon S3 Vectors index.

## 2. Prerequisites

The following AWS resources were created before Knowledge Base creation:

1. Amazon S3 source bucket.
2. Uploaded insurance policy document.
3. Amazon S3 Vectors bucket.
4. Amazon S3 Vectors index.
5. IAM execution role with the required permissions.

## 3. AWS Configuration

| Property | Value |
|---|---|
| AWS Region | us-east-1 |
| AWS Account ID | YOUR_AWS_ACCOUNT_ID |
| Knowledge Base Name | insurance-rag-knowledge-base |
| Vector Bucket | insurance-rag-vector-bucket-YOUR_AWS_ACCOUNT_ID |
| Vector Index | insurance-policy-index |
| Embedding Model | amazon.titan-embed-text-v2:0 |
| Embedding Dimension | 1024 |
| IAM Role | AmazonBedrockExecutionRoleForInsuranceKB |

## 4. Vector Index Configuration

The existing vector index was initially created without the Bedrock metadata configuration.

The empty index was deleted and recreated with the following configuration:

```python
metadataConfiguration={
    "nonFilterableMetadataKeys": [
        "AMAZON_BEDROCK_TEXT",
        "AMAZON_BEDROCK_METADATA"
    ]
}
```

Other index settings:

- Data type: float32
- Dimension: 1024
- Distance metric: cosine

The index configuration was verified using the AWS CLI:

```bash
aws s3vectors get-index \
  --vector-bucket-name insurance-rag-vector-bucket-YOUR_AWS_ACCOUNT_ID \
  --index-name insurance-policy-index \
  --region us-east-1
```

## 5. Knowledge Base Creation Script

Python file:

`src/create_knowledge_base.py`

Boto3 client:

```python
bedrock_agent = session.client("bedrock-agent")
```

Main API:

```python
response = bedrock_agent.create_knowledge_base(
    name=knowledge_base_name,
    description="Insurance policy RAG Knowledge Base using Amazon S3 Vectors",
    roleArn=role_arn,
    knowledgeBaseConfiguration=knowledge_base_configuration,
    storageConfiguration=storage_configuration
)
```

## 6. Execution Command

From the project `src` directory:

```bash
python create_knowledge_base.py
```

## 7. AWS CLI Verification

The Knowledge Base status was verified using:

```bash
aws bedrock-agent get-knowledge-base \
  --knowledge-base-id E1RNVKEBQF \
  --region us-east-1
```

## 8. Creation Result

**Status: ACTIVE**

| Property | Result |
|---|---|
| Knowledge Base Name | insurance-rag-knowledge-base |
| Knowledge Base ID | E1RNVKEBQF |
| AWS Region | us-east-1 |
| Embedding Model | Titan Text Embeddings V2 |
| Embedding Dimension | 1024 |
| Storage Type | S3_VECTORS |
| Vector Index | insurance-policy-index |
| Status | ACTIVE |

## 9. Knowledge Base ARN

```text
arn:aws:bedrock:us-east-1:YOUR_AWS_ACCOUNT_ID:knowledge-base/E1RNVKEBQF
```

## 10. Milestone Completed

Successfully created an Amazon Bedrock Knowledge Base using Python Boto3.

The Knowledge Base is connected to the existing S3 Vectors index and is now ACTIVE.

## 11. Next Implementation Milestone

Configure an Amazon S3 data source using Boto3.

Upcoming activities:

1. Create the data source.
2. Configure document chunking.
3. Start document ingestion.
4. Monitor ingestion status.
5. Test retrieval using natural-language questions.
