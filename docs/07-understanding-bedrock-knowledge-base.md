# 07 – Understanding Amazon Bedrock Knowledge Base

## 1. Objective

Understand how Amazon Bedrock Knowledge Bases work and how the Python Boto3 script creates a Knowledge Base connected to an existing Amazon S3 Vectors index.

## 2. Overall Architecture

```text
Insurance Policy Document
          |
          v
       Amazon S3
          |
          v
 Amazon Bedrock Knowledge Base
          |
          +---- Document Chunking
          |
          +---- Titan Text Embeddings V2
          |          |
          |          v
          |    1024-dimensional vectors
          |          |
          v          v
       Amazon S3 Vectors
          |
          v
   insurance-policy-index
```

## 3. AWS Components

### Amazon S3
Stores the original insurance policy document.

### Amazon Bedrock Knowledge Base
Coordinates document processing, chunking, embedding generation and retrieval.

### Amazon Titan Text Embeddings V2
Converts text chunks into numerical vector representations.

Configured dimension: 1024.

### Amazon S3 Vectors
Stores and retrieves vector embeddings using similarity search.

### IAM Execution Role
Allows Amazon Bedrock to access the required AWS resources.

## 4. Python Script Execution Flow

Script: `src/create_knowledge_base.py`

The main API call is:

```python
response = bedrock_agent.create_knowledge_base(
    name=knowledge_base_name,
    description="Insurance policy RAG Knowledge Base using Amazon S3 Vectors",
    roleArn=role_arn,
    knowledgeBaseConfiguration=knowledge_base_configuration,
    storageConfiguration=storage_configuration
)
```

This API requires five inputs.

| Parameter | Purpose |
|---|---|
| name | Knowledge Base name |
| description | Knowledge Base description |
| roleArn | IAM execution role ARN |
| knowledgeBaseConfiguration | Embedding model configuration |
| storageConfiguration | Vector storage configuration |

## 5. Dependency Flow

### Step 1: AWS Session and Clients

Create a Boto3 session and clients for:
- Bedrock Agent
- S3 Vectors
- STS

### Step 2: AWS Account ID

Use:

```python
account_id = sts.get_caller_identity()["Account"]
```

This dynamically retrieves the AWS account ID.

### Step 3: Resource Names and ARNs

Define:
- Knowledge Base name
- Vector bucket name
- Vector index name
- IAM execution role ARN
- Embedding model ARN

### Step 4: Retrieve Existing Vector Resources

Use:
- `get_vector_bucket()` to retrieve vector bucket details.
- `get_index()` to retrieve vector index details.

Capture the index ARN for the Knowledge Base configuration.

### Step 5: Knowledge Base Embedding Configuration

```python
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
```

This configuration tells Bedrock:
- Create a vector Knowledge Base.
- Use Titan Text Embeddings V2.
- Generate 1024-dimensional embeddings.
- Use FLOAT32 data type.

The embedding dimension must match the existing vector index.

### Step 6: Storage Configuration

```python
storage_configuration = {
    "type": "S3_VECTORS",
    "s3VectorsConfiguration": {
        "indexArn": index_arn
    }
}
```

This tells Bedrock which existing S3 Vectors index to use.

### Step 7: Create Knowledge Base

Call:

`bedrock_agent.create_knowledge_base()`

The API receives all the prepared configurations and creates the Knowledge Base.

### Step 8: Capture the Response

```python
knowledge_base = response["knowledgeBase"]

knowledge_base_id = knowledge_base["knowledgeBaseId"]
knowledge_base_arn = knowledge_base["knowledgeBaseArn"]
```

Capture:
- Knowledge Base ID
- Knowledge Base ARN
- Creation status

## 6. Important Distinction

Creating a Knowledge Base does not automatically ingest the documents.

Document ingestion is a separate workflow:

1. Create an S3 data source.
2. Configure chunking.
3. Start an ingestion job.
4. Bedrock reads the documents.
5. Bedrock splits documents into chunks.
6. Titan generates embeddings.
7. Embeddings and associated metadata are stored in S3 Vectors.

## 7. Existing AWS Configuration

- Region: us-east-1
- Source S3 bucket: rag-chatbot-kb-s3vectorYOUR_AWS_ACCOUNT_ID
- Vector bucket: insurance-rag-vector-bucket-YOUR_AWS_ACCOUNT_ID
- Vector index: insurance-policy-index
- Embedding model: Amazon Titan Text Embeddings V2
- Dimensions: 1024
- Data type: FLOAT32
- Distance metric: cosine
- IAM role: AmazonBedrockExecutionRoleForInsuranceKB

## 8. Expected Outcome

A working Bedrock Knowledge Base connected to an existing S3 Vectors index and ready for data source configuration and document ingestion.
