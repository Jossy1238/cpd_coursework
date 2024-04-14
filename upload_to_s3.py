import boto3
import os

def upload_folder_to_s3(local_folder, bucket_name):
    """
    Uploads a folder and its contents to an S3 bucket.
    
    Args:
        local_folder (str): Path to the local folder to upload.
        bucket_name (str): Name of the S3 bucket.
    """
    s3 = boto3.client('s3')
    
    try:
        for root, dirs, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                s3_key = os.path.relpath(local_path, local_folder)
                s3.upload_file(local_path, bucket_name, s3_key)
        print("Folder uploaded successfully to S3 bucket.")
    except Exception as e:
        print(f"Error uploading folder to S3 bucket: {e}")

# Set AWS credentials (either through environment variables or AWS configuration file)
# os.environ['AWS_ACCESS_KEY_ID'] = 'your_access_key_id'
# os.environ['AWS_SECRET_ACCESS_KEY'] = 'your_secret_access_key'
# os.environ['AWS_DEFAULT_REGION'] = 'your_aws_region'

# Set variables
local_folder = "/home/ec2-user/my-images"
bucket_name = "my-bucket-s211100"

# Upload folder to S3
upload_folder_to_s3(local_folder, bucket_name)
