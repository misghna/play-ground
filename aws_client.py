import boto3

bucket_name = 's-camera'
access_key = ''
secret_key = ''
session_token = ''  # Optional, if using temporary credentials

def get_aws_session():    
    session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )

    # Create an S3 client
    return session.client('s3')
