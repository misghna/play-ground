from aws_client import get_aws_session
import time

bucket_name = 's-camera'

camera_ip_str="169.254.88.77"

def camera_ip():
    return camera_ip_str
 
def get_device_id():
    """
    Retrieves the Raspberry Pi's unique serial number.

    Returns:
        str: The serial number as a string, or 'ERROR000000000' if not found.
    """
    serial = "ERROR000000000"
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if line.startswith('Serial'):
                    serial = line.strip().split(': ')[1]
                    break
    except Exception as e:
        print(f"An error occurred while retrieving the serial number: {e}")
    return serial

def write_log(text, session_token=None):
    device_id= get_device_id()
    timestamp_millis = int(time.time() * 1000)
    # Define the S3 object key (path)
    object_key = f'logs/{device_id}_{timestamp_millis}.log'

    # Create an S3 client
    s3_client = get_aws_session()

    try:
        # Upload the text string as an object to S3
        msg = f"{timestamp_millis},{device_id},{text}"
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=msg,
            ContentType='text/plain'
        )
        print(f"Text uploaded successfully to {bucket_name}/{object_key}.")
    except Exception as e:
        print(f"An error occurred: {e}")
