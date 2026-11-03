# 03 – Environment Configuration

## 1. Development Environment

| Component | Configuration |
|---|---|
| Operating System | macOS |
| Programming Language | Python 3 |
| AWS SDK | Boto3 |
| AWS Region | us-east-1 |
| Virtual Environment | .venv |

## 2. Python Environment Setup

Created an isolated Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Dependencies

Created `requirements.txt` with the following dependency:

```text
boto3
```

Installed dependencies:

```bash
python -m pip install -r requirements.txt
```

## 4. AWS Authentication

Configured Boto3 to use existing AWS CLI credentials.

No AWS access keys or secret credentials are stored in the project.

## 5. AWS Connectivity Verification

Created `src/aws_connection.py` to verify AWS authentication using AWS STS.

Used the following API:

```python
sts = session.client("sts")
response = sts.get_caller_identity()
```

**Result:** Successfully connected to the AWS account and retrieved the caller identity.