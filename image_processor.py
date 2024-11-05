import cv2
import boto3
import schedule
import time
from datetime import datetime
from botocore.exceptions import NoCredentialsError
from util import get_device_id
from aws_client import get_aws_session
import socket

bucket_name = 's-camera'
device_id = get_device_id()
# Axis camera URL
axis_camera_ip = '192.168.1.223'
axis_camera_url = 'http://{axis_camera_ip}/mjpg/video.mjpg'


def write_log(text, session_token=None):
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


def check_tcp_connection(ip, port, timeout=5):
    # Check if a TCP connection to the specified IP and port can be established.
    try:
        with socket.create_connection((ip, port), timeout):
            return True
    except (socket.timeout, socket.error):
        write_log("Error: connecting to camera")
        print("Error: connecting to camera")
        return False
    
def capture_image_from_axis():
    # Initialize video capture from the Axis camera
    if(not check_tcp_connection(axis_camera_ip,80)):
       return None
    # Initialize video capture from the Axis camera
    cap = cv2.VideoCapture(axis_camera_url)
    if not cap.isOpened():
        write_log("Error: Unable to open camera image")
        print("Error: Unable to open video stream.")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret:
        write_log("Error: Unable to capture image")
        print("Error: Unable to capture image.")
        return None

    # Encode the frame as JPEG
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        write_log("Error: Failed to encode image")
        print("Error: Failed to encode image.")
        return None

    return encoded_image.tobytes()
    

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
schedule.every().hour.at(":00").do(capture_and_upload)
schedule.every().hour.at(":15").do(capture_and_upload)
schedule.every().hour.at(":30").do(capture_and_upload)
schedule.every().hour.at(":45").do(capture_and_upload)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

