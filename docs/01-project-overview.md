# 01 – Project Overview

## Project Name
RAG Chatbot using Amazon Bedrock Knowledge Bases and S3 Vectors

## 1. Objective

Build a simple Retrieval-Augmented Generation (RAG) solution using AWS services and Python Boto3.

The project automates the creation of an Amazon Bedrock Knowledge Base backed by Amazon S3 Vectors.

A sample insurance policy document will be uploaded to Amazon S3 and ingested into the Knowledge Base.

## 2. Technology Stack

- Python
- Boto3 (AWS SDK for Python)
- Amazon S3
- Amazon S3 Vectors
- Amazon Bedrock Knowledge Bases
- Amazon Titan Text Embeddings V2

## 3. Project Workflow

1. Configure AWS connectivity using Boto3.
2. Create an Amazon S3 bucket.
3. Upload a sample insurance policy document.
4. Create an S3 Vector bucket and vector index.
5. Create an Amazon Bedrock Knowledge Base.
6. Configure the S3 data source.
7. Start document ingestion.
8. Test document retrieval.

## 4. Expected Outcome

A working AWS Knowledge Base that can retrieve relevant information from a sample insurance policy document.

All AWS resources will be created programmatically using Python Boto3.

## 5. Cost Management

This is a small hands-on project using a single sample document.

AWS resources will be deleted after testing to avoid ongoing resource charges.

## 6. Repository

The source code and documentation will be maintained in GitHub.
