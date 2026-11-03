import boto3
import json

# AWS configuration
region = "us-east-1"
session=boto3.Session(region_name=region)
iam=session.client("iam")
sts=session.client("sts")
account_id=sts.get_caller_identity()["Account"]

print(account_id)

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": account_id
                },
                "ArnLike": {
                    "aws:SourceArn": (
                        f"arn:aws:bedrock:{region}:"
                        f"{account_id}:knowledge-base/*"
                    )
                }
            }
        }
    ]
}

# Get existing S3 bucket name
bucket_name = f"rag-chatbot-kb-s3vector-{account_id}"

# Permissions policy
permissions_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3ListBucket",
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": f"arn:aws:s3:::{bucket_name}"
        },
        {
            "Sid": "S3ReadInsuranceDocuments",
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": f"arn:aws:s3:::{bucket_name}/insurance/*"
        },
        {
            "Sid": "S3VectorsAccess",
            "Effect": "Allow",
            "Action": [
                "s3vectors:PutVectors",
                "s3vectors:GetVectors",
                "s3vectors:DeleteVectors",
                "s3vectors:QueryVectors",
                "s3vectors:GetIndex"
                     ],
            "Resource": (
                f"arn:aws:s3vectors:{region}:{account_id}:"
                f"bucket/insurance-rag-vector-bucket-{account_id}/"
                "index/insurance-policy-index"
                        )
        },
        {
            "Sid": "TitanEmbeddingAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": (
                f"arn:aws:bedrock:{region}::foundation-model/"
                "amazon.titan-embed-text-v2:0"
            )
        },
        {
            "Sid": "BedrockModelListing",
            "Effect": "Allow",
            "Action": [
                "bedrock:ListFoundationModels",
                "bedrock:ListCustomModels"
            ],
            "Resource": "*"
        }
    ]
}

# IAM role configuration
role_name = "AmazonBedrockExecutionRoleForInsuranceKB"

# Create IAM role
response = iam.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(trust_policy),
    Description="Execution role for Insurance RAG Knowledge Base"
)

role_arn = response["Role"]["Arn"]

print("IAM role created successfully!")
print("Role ARN:", role_arn)

iam.put_role_policy(
    RoleName=role_name,
    PolicyName="InsuranceKnowledgeBasePermissions",
    PolicyDocument=json.dumps(permissions_policy)
)

print("Permissions policy attached successfully!")