
import boto3

# AWS configuration
region = "us-east-1"

# Existing Knowledge Base
knowledge_base_id = "E1RNVKEBQF"

# Create AWS session
session = boto3.Session(region_name=region)

# Create Bedrock Agent Runtime client
bedrock_agent_runtime = session.client("bedrock-agent-runtime")

print("=" * 60)
print("       INSURANCE POLICY - RAG RETRIEVAL")
print("=" * 60)

print("Ask questions about your insurance policy.")
print("Type 'exit' to quit.")

# Keep asking questions until the user exits
while True:

    # Get question from user
    query = input("\nYour question: ").strip()

    # Check whether user wants to exit
    if query.lower() == "exit":
        print("\nThank you for using Insurance RAG Chatbot!")
        break

    # Check for empty input
    if not query:
        print("Please enter a question.")
        continue

    try:
        # Retrieve relevant information from Knowledge Base
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={
                "text": query
            }
        )

        # Extract retrieval results
        results = response["retrievalResults"]

        print("\n" + "-" * 60)
        print("RETRIEVED INFORMATION")
        print("-" * 60)

        if not results:
            print("No relevant information found.")
            continue

        # Display retrieved document chunks
        for index, result in enumerate(results, start=1):

            print(f"\nResult {index}")

            print("Score:", result.get("score"))

            print("Text:", result["content"].get("text", "No text found"))

            print("Source:", result.get("location", {}))

            print("-" * 60)

    except Exception as error:
        print("Error retrieving information:", error)
