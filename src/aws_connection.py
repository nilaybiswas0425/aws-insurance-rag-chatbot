import boto3

session=boto3.Session(region_name="us-east-1")
sts=session.client("sts")

response=sts.get_caller_identity()

print("Aws Connection successful")
print("Account Id",response["Account"])
print("ARN",response["Arn"])