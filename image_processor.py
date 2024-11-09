import cv2
import boto3
import schedule
import time
from datetime import datetime
from util import camera_ip
from aws_client import get_aws_session
from botocore.exceptions import NoCredentialsError
from util import get_device_id
from util import write_log
import requests
import socket

# AWS S3 credentials and bucket information
bucket_name = 's-camera'
device_id = get_device_id()
# Axis camera URL
axis_camera_url = f"http://{camera_ip()}/jpg/image.jpg"


def capture_image_from_axis() -> bytes:

    auth_header = 'Digest username="root", realm="AXIS_B8A44FBE3641", nonce="rfzFw5AlBgA=67b5b06cbb1f3a58df46db7d9da7381973a4432f", uri="/axis-cgi/param.cgi", algorithm=MD5, response="f1e8f807813bc2f0f303ff5e3d77bf97", qop=auth, nc=0000004d, cnonce="d94b70e736de23a3"'
    headers = {
        'Authorization': auth_header
    }
    
    # Send the GET request with authorization headers
    print("capturing image ..")
    response = requests.get(axis_camera_url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        print(f"Received image of {len(response.content)} bytes.")
        return response.content  # Return the byte array of the image
    else:
        print("error getting image ..")
        response.raise_for_status()  # Raise an error if the request failed

def upload_image_to_s3(image_bytes):

    # Create an S3 client
    s3_client = get_aws_session()

    # Generate filename based on current UTC date and time (MMDDYYYYTHHMM format)
    timestamp = datetime.utcnow().strftime("%m%d%YT%H%M")
    object_name = f"devId-8732/imgs/{timestamp}.jpg"  # Prepend the desired folder path

    try:
        # Upload the image to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=image_bytes,
            ContentType='image/jpeg'
        )
        print(f"Image uploaded successfully as {object_name}.")
    except NoCredentialsError:
        print("Error: AWS credentials not available.")
    except Exception as e:
        write_log("Error: occurred during image upload")
        print(f"An error occurred during upload: {e}")

def capture_and_upload():
    try:
        image_bytes = capture_image_from_axis()
        if image_bytes:
            upload_image_to_s3(image_bytes)
        else:
            write_log("Error: No image captured; skipping upload.")
            print("No image captured; skipping upload.")
    except Exception as e:
        write_log("Error: during capture and upload!")
        print(f"An error occurred in capture_and_upload: {e}")

# Schedule the task to run every 15 minutes at 00, 15, 30, and 45 minutes past the hour
schedule.every().hour.at(":04").do(capture_and_upload)
schedule.every().hour.at(":15").do(capture_and_upload)
schedule.every().hour.at(":30").do(capture_and_upload)
schedule.every().hour.at(":45").do(capture_and_upload)

def run_scheduler():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print("error running scheduler")

