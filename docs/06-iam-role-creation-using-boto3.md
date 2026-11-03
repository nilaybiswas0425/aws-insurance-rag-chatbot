# Step 6: IAM Role Creation Using Boto3

## Objective
Create an IAM execution role that allows Amazon Bedrock
Knowledge Bases to access the required AWS resources.

## Role Details

- Role Name: AmazonBedrockExecutionRoleForInsuranceKB
- AWS Service: Amazon Bedrock
- Region: us-east-1

## Trust Policy

Allows the Bedrock service (`bedrock.amazonaws.com`)
to assume this IAM role.

The trust policy restricts access using:
- AWS Source Account
- Bedrock Knowledge Base ARN

## Permissions Policy

The role receives permissions for:

1. Amazon S3
   - ListBucket
   - GetObject

2. Amazon S3 Vectors
   - PutVectors
   - GetVectors
   - DeleteVectors
   - QueryVectors
   - GetIndex

3. Amazon Bedrock
   - InvokeModel
   - ListFoundationModels
   - ListCustomModels

## Implementation

Python script:

`src/create_bedrock_role.py`

Boto3 methods used:

- create_role()
- put_role_policy()

## Result

IAM role created successfully.

Role ARN:
`arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/AmazonBedrockExecutionRoleForInsuranceKB`