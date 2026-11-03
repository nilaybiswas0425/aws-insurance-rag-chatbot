# 05 – S3 Vectors Creation Using Boto3

## 1. Objective

Create an Amazon S3 Vector bucket and vector index using Python Boto3.

These resources will be used as the vector storage backend for our Amazon Bedrock Knowledge Base.

## 2. Vector Bucket Creation

Python script: `src/create_vector_bucket.py`

Boto3 client:

```python
s3vectors = session.client("s3vectors")
```

AWS API:

```python
s3vectors.create_vector_bucket(
    vectorBucketName="insurance-rag-vector-bucket"
)
```

## 3. Vector Index Creation

Python script: `src/create_vector_index.py`

Created the following index:

| Configuration | Value |
|---|---|
| Index name | insurance-policy-index |
| Data type | float32 |
| Dimensions | 1024 |
| Distance metric | cosine |

The dimension matches the selected Amazon Titan Text Embeddings V2 configuration.

## 4. Verification

List vector buckets:

```bash
aws s3vectors list-vector-buckets --region us-east-1
```

List indexes:

```bash
aws s3vectors list-indexes \
  --vector-bucket-name insurance-rag-vector-bucket \
  --region us-east-1
```

Retrieve index details:

```bash
aws s3vectors get-index \
  --vector-bucket-name insurance-rag-vector-bucket \
  --index-name insurance-policy-index \
  --region us-east-1
```

## 5. Result

Successfully created and verified:

- S3 Vector bucket
- Vector index

## 6. Next Step

Create an IAM execution role to allow Amazon Bedrock to access the required AWS resources.
