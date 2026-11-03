
import boto3
import time
from botocore.exceptions import ClientError


# ============================================================
# 1. CONFIGURATION
# ============================================================

REGION = "us-east-1"

KNOWLEDGE_BASE_ID = "E1RNVKEBQF"
DATA_SOURCE_ID = "TJKRHQLM2S"

session = boto3.Session(region_name=REGION)

sts = session.client("sts")

account_id = sts.get_caller_identity()["Account"]

S3_BUCKET_NAME = f"rag-chatbot-kb-s3vector-{account_id}"

VECTOR_BUCKET_NAME = f"insurance-rag-vector-bucket-{account_id}"

IAM_ROLE_NAME = "AmazonBedrockExecutionRoleForInsuranceKB"

# SAFETY SWITCH:
# False = show cleanup plan only
# True  = actually delete AWS resources

EXECUTE_DELETION = False


# ============================================================
# 2. AWS CLIENTS
# ============================================================



bedrock_agent = session.client("bedrock-agent")
s3 = session.client("s3")
s3vectors = session.client("s3vectors")
iam = session.client("iam")
sts = session.client("sts")

account_id = sts.get_caller_identity()["Account"]

S3_BUCKET_NAME = f"rag-chatbot-kb-s3vector-{account_id}"

VECTOR_BUCKET_NAME = f"insurance-rag-vector-bucket-{account_id}"


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def is_not_found(error):
    code = error.response["Error"]["Code"]
    return code in [
        "ResourceNotFoundException",
        "NotFoundException",
        "NoSuchBucket",
        "404"
    ]


def wait_for_resource_deletion(check_function, resource_name):
    print(f"Waiting for {resource_name} deletion...")

    for attempt in range(60):
        try:
            check_function()
            time.sleep(5)
        except ClientError as error:
            if is_not_found(error):
                print(f"{resource_name} deleted successfully.")
                return
            raise

    raise TimeoutError(
        f"Timed out waiting for {resource_name} deletion."
    )


# ============================================================
# 4. DELETE BEDROCK DATA SOURCE
# ============================================================

def delete_data_source():

    print("\nSTEP 1: Deleting Bedrock Data Source")

    try:
        bedrock_agent.get_data_source(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID
        )

        bedrock_agent.delete_data_source(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID
        )

        def check_data_source():
            bedrock_agent.get_data_source(
                knowledgeBaseId=KNOWLEDGE_BASE_ID,
                dataSourceId=DATA_SOURCE_ID
            )

        wait_for_resource_deletion(
            check_data_source,
            "Bedrock Data Source"
        )

    except ClientError as error:
        if is_not_found(error):
            print("Data source already deleted.")
        else:
            raise


# ============================================================
# 5. DELETE BEDROCK KNOWLEDGE BASE
# ============================================================

def delete_knowledge_base():

    print("\nSTEP 2: Deleting Bedrock Knowledge Base")

    try:
        bedrock_agent.get_knowledge_base(
            knowledgeBaseId=KNOWLEDGE_BASE_ID
        )

        bedrock_agent.delete_knowledge_base(
            knowledgeBaseId=KNOWLEDGE_BASE_ID
        )

        def check_knowledge_base():
            bedrock_agent.get_knowledge_base(
                knowledgeBaseId=KNOWLEDGE_BASE_ID
            )

        wait_for_resource_deletion(
            check_knowledge_base,
            "Bedrock Knowledge Base"
        )

    except ClientError as error:
        if is_not_found(error):
            print("Knowledge Base already deleted.")
        else:
            raise


# ============================================================
# 6. DELETE S3 VECTORS INDEXES AND BUCKET
# ============================================================

def delete_vector_resources():

    print("\nSTEP 3: Deleting S3 Vectors Resources")

    try:
        paginator = s3vectors.get_paginator("list_indexes")

        for page in paginator.paginate(
            vectorBucketName=VECTOR_BUCKET_NAME
        ):
            for index in page.get("indexes", []):

                index_name = index["indexName"]

                print("Deleting vector index:", index_name)

                s3vectors.delete_index(
                    vectorBucketName=VECTOR_BUCKET_NAME,
                    indexName=index_name
                )

        s3vectors.delete_vector_bucket(
            vectorBucketName=VECTOR_BUCKET_NAME
        )

        print("S3 Vectors bucket deleted.")

    except ClientError as error:
        if is_not_found(error):
            print("S3 Vectors bucket already deleted.")
        else:
            raise


# ============================================================
# 7. EMPTY ORDINARY S3 BUCKET
#    INCLUDING OBJECT VERSIONS AND DELETE MARKERS
# ============================================================

def empty_s3_bucket():

    print("\nSTEP 4: Emptying Ordinary S3 Bucket")

    paginator = s3.get_paginator("list_object_versions")

    objects_to_delete = []

    try:
        for page in paginator.paginate(
            Bucket=S3_BUCKET_NAME
        ):

            for version in page.get("Versions", []):
                objects_to_delete.append({
                    "Key": version["Key"],
                    "VersionId": version["VersionId"]
                })

            for marker in page.get("DeleteMarkers", []):
                objects_to_delete.append({
                    "Key": marker["Key"],
                    "VersionId": marker["VersionId"]
                })

            if len(objects_to_delete) >= 1000:
                s3.delete_objects(
                    Bucket=S3_BUCKET_NAME,
                    Delete={
                        "Objects": objects_to_delete,
                        "Quiet": True
                    }
                )
                objects_to_delete = []

        if objects_to_delete:
            s3.delete_objects(
                Bucket=S3_BUCKET_NAME,
                Delete={
                    "Objects": objects_to_delete,
                    "Quiet": True
                }
            )

        print("S3 bucket contents deleted.")

    except ClientError as error:
        if is_not_found(error):
            print("S3 bucket already deleted.")
        else:
            raise


def delete_s3_bucket():

    print("\nSTEP 5: Deleting Ordinary S3 Bucket")

    try:
        s3.delete_bucket(Bucket=S3_BUCKET_NAME)
        print("Ordinary S3 bucket deleted.")

    except ClientError as error:
        if is_not_found(error):
            print("S3 bucket already deleted.")
        else:
            raise


# ============================================================
# 8. DELETE IAM ROLE AND ITS ATTACHMENTS
# ============================================================

def delete_iam_role():

    print("\nSTEP 6: Deleting IAM Role")

    try:
        iam.get_role(RoleName=IAM_ROLE_NAME)

        # Delete inline policies
        paginator = iam.get_paginator("list_role_policies")

        for page in paginator.paginate(
            RoleName=IAM_ROLE_NAME
        ):
            for policy_name in page["PolicyNames"]:

                print("Deleting inline policy:", policy_name)

                iam.delete_role_policy(
                    RoleName=IAM_ROLE_NAME,
                    PolicyName=policy_name
                )

        # Detach managed policies
        paginator = iam.get_paginator(
            "list_attached_role_policies"
        )

        for page in paginator.paginate(
            RoleName=IAM_ROLE_NAME
        ):
            for policy in page["AttachedPolicies"]:

                print(
                    "Detaching managed policy:",
                    policy["PolicyName"]
                )

                iam.detach_role_policy(
                    RoleName=IAM_ROLE_NAME,
                    PolicyArn=policy["PolicyArn"]
                )

        # Remove role from instance profiles
        paginator = iam.get_paginator(
            "list_instance_profiles_for_role"
        )

        for page in paginator.paginate(
            RoleName=IAM_ROLE_NAME
        ):
            for profile in page["InstanceProfiles"]:

                profile_name = profile["InstanceProfileName"]

                iam.remove_role_from_instance_profile(
                    InstanceProfileName=profile_name,
                    RoleName=IAM_ROLE_NAME
                )

                iam.delete_instance_profile(
                    InstanceProfileName=profile_name
                )

        # Delete role
        iam.delete_role(RoleName=IAM_ROLE_NAME)

        print("IAM role deleted.")

    except ClientError as error:
        if is_not_found(error):
            print("IAM role already deleted.")
        else:
            raise


# ============================================================
# 9. MAIN CLEANUP
# ============================================================

def main():

    print("=" * 60)
    print("AWS RAG PROJECT CLEANUP")
    print("=" * 60)

    if not EXECUTE_DELETION:

        print("\nDRY RUN MODE")
        print("No AWS resources will be deleted.")

        print("\nResources scheduled for cleanup:")
        print("1. Bedrock Data Source")
        print("2. Bedrock Knowledge Base")
        print("3. S3 Vectors Indexes")
        print("4. S3 Vectors Bucket")
        print("5. Ordinary S3 Bucket and all object versions")
        print("6. IAM Role and its attached policies")

        print("\nTo execute, review this script and set:")
        print("EXECUTE_DELETION = True")

        return

    confirmation_text = (
        f"DELETE {S3_BUCKET_NAME}"
    )

    confirmation = input(
       f"\nType {confirmation_text} to permanently delete "
    "these resources: "
    )

    if confirmation != confirmation_text:
        print("Confirmation did not match. Cleanup cancelled.")
        return

    delete_data_source()
    delete_knowledge_base()
    delete_vector_resources()
    empty_s3_bucket()
    delete_s3_bucket()
    delete_iam_role()

    print("\n" + "=" * 60)
    print("AWS RAG PROJECT CLEANUP FINISHED")
    print("=" * 60)


if __name__ == "__main__":
    main()
