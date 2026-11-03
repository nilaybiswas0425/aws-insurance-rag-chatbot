# AWS Insurance RAG Chatbot Using Amazon Bedrock

A hands-on Retrieval-Augmented Generation (RAG) project built using Python, Boto3, Amazon Bedrock Knowledge Bases, Amazon S3 Vectors, and Amazon Nova Lite.

## Project Overview

This project demonstrates how to build an insurance policy chatbot that answers natural-language questions using information retrieved from insurance policy documents.

Instead of relying only on a language model's existing knowledge, the chatbot retrieves relevant document content from an Amazon Bedrock Knowledge Base and uses Amazon Nova Lite to generate contextual answers.

The project was developed to understand the complete RAG workflow using native AWS services and Python Boto3.

## Architecture

```text
                 User
                  |
                  v
             Python Chatbot
                  |
                  v
       Amazon Bedrock Knowledge Base
                  |
                  v
              S3 Vectors
                  |
          Retrieve Relevant
           Policy Chunks
                  |
                  v
           Amazon Nova Lite
                  |
             Generate Answer
                  |
                  v
          Answer + Source
```

## AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon S3 | Stores insurance policy documents |
| Amazon S3 Vectors | Stores and searches vector embeddings |
| Amazon Bedrock Knowledge Bases | Manages document retrieval |
| Amazon Titan Text Embeddings V2 | Generates text embeddings |
| Amazon Nova Lite | Generates natural-language responses |
| AWS IAM | Manages permissions and access |
| AWS STS | Retrieves the AWS account identity |

## Technology Stack

- Python 3.12
- Boto3
- Amazon Bedrock
- Amazon S3
- Amazon S3 Vectors
- Amazon Titan Text Embeddings V2
- Amazon Nova Lite

## Project Structure

```text
rag-chatbot-kb-s3vector/
|
├── data/
│   └── sample_insurance_policy.txt
|
├── docs/
│   ├── 01-project-overview.md
│   ├── 02-project-architecture.md
│   ├── 03-environment-configuration.md
│   ├── 04-s3-bucket-creation-using-boto3.md
│   ├── 05-s3-vectors-creation-using-boto3.md
│   ├── 06-iam-role-creation-using-boto3.md
│   ├── 07-understanding-bedrock-knowledge-base.md
│   ├── 08-bedrock-knowledge-base-creation.md
│   ├── 09-s3-data-source-and-ingestion.md
│   └── 10-chatbot-implementation.md
|
├── src/
│   ├── aws_connection.py
│   ├── create_s3_bucket.py
│   ├── upload_document.py
│   ├── create_vector_bucket.py
│   ├── create_vector_index.py
│   ├── create_bedrock_role.py
│   ├── create_knowledge_base.py
│   ├── create_data_source.py
│   ├── start_ingestion_job.py
│   ├── test_retrieval.py
│   ├── chatbot.py
│   ├── check_data_source.py
│   └── cleanup_aws_resources.py
|
├── tests/
├── logs/
├── screenshots/
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, you need:

1. An AWS account.
2. Python 3.12 or compatible version.
3. AWS CLI installed and configured.
4. Appropriate IAM permissions.
5. Access to the required Amazon Bedrock foundation models in your AWS region.

The project uses `us-east-1` as its AWS region.

## Environment Setup

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd rag-chatbot-kb-s3vector
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Configure AWS credentials using the AWS CLI:

```bash
aws configure
```

Never commit AWS credentials or secret keys to GitHub.

## Implementation Workflow

The project follows these steps:

1. Create an Amazon S3 bucket using Boto3.
2. Upload an insurance policy document.
3. Create an S3 Vectors bucket.
4. Create a vector index with 1024 dimensions.
5. Create an IAM execution role for Bedrock.
6. Create an Amazon Bedrock Knowledge Base.
7. Configure the S3 data source.
8. Start the ingestion job.
9. Test document retrieval.
10. Implement the interactive RAG chatbot.
11. Display generated answers and source references.

## Running the Chatbot

After configuring AWS resources and completing document ingestion:

```bash
cd src
python chatbot.py
```

Example interaction:

```text
ABC INSURANCE - RAG CHATBOT

You: What is my deductible?

ABC Insurance Bot:

Your deductible for home insurance is CAD 1,000 per covered claim.
```

## Key Learning Outcomes

Through this project, I explored:

- AWS resource creation using Python Boto3.
- AWS IAM roles and permissions.
- Amazon S3 and document uploads.
- Amazon S3 Vectors and vector indexes.
- Text embeddings using Amazon Titan.
- Amazon Bedrock Knowledge Bases.
- Document ingestion and chunking.
- Semantic retrieval.
- Retrieval-Augmented Generation.
- Prompt customization.
- Conversational session management.
- Source attribution.
- AWS resource cleanup using Boto3.

## AWS Resource Cleanup

The project includes a cleanup script:

```bash
python cleanup_aws_resources.py
```

The script defaults to dry-run mode.

Review the script carefully before enabling deletion. It permanently deletes the configured project resources when explicitly authorized.

## Important Notes

- This is a learning and demonstration project.
- The insurance policy is sample data, not a real insurance contract.
- AWS service usage may incur charges.
- Model access and permissions must be configured in your AWS account.
- Resource identifiers and account-specific configuration should not be hard-coded for reusable deployments.

## Future Enhancements

- Add more insurance policy documents.
- Introduce metadata-based filtering.
- Improve retrieval accuracy.
- Add automated tests.
- Build a web-based chatbot interface.
- Explore additional foundation models.

---

**Author:** Nilay Biswas

**Focus Areas:** AWS | Data Engineering | Python | Generative AI | RAG