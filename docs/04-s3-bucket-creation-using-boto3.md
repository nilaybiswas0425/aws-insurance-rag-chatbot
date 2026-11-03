# 04 – S3 Bucket Creation Using Boto3

## 1. Objective

Create an Amazon S3 bucket programmatically using Python Boto3.

The bucket will store sample insurance policy documents used by the Amazon Bedrock Knowledge Base.

## 2. AWS Configuration

- AWS Region: us-east-1
- AWS SDK: Boto3
- Authentication: Existing AWS CLI credentials

## 3. Implementation

Python script: `src/create_s3_bucket.py`

The script:
1. Establishes an AWS session.
2. Retrieves the AWS account ID using STS.
3. Generates a globally unique S3 bucket name.
4. Creates an S3 bucket using Boto3.

## 4. AWS API Used

```python
s3.create_bucket(Bucket=bucket_name)
```

## 5. Verification

Verified bucket creation using AWS CLI:

```bash
aws s3 ls
```

Checked bucket accessibility:

```bash
aws s3api head-bucket --bucket BUCKET_NAME
```

## 6. Result

Successfully created and verified the project S3 bucket in AWS.

## 7. Next Step

Upload a sample insurance policy document to the S3 bucket.
