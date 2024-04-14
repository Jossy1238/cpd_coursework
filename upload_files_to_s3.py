import boto3
import os
import time

def upload_files_to_s3(bucket_name, local_directory):
    # Initialize the S3 client
    s3_client = boto3.client('s3')
    # List all files in the specified local directory
    for file_name in os.listdir(local_directory):
        # Construct the full file path
        file_path = os.path.join(local_directory, file_name)

        # Construct the S3 key
        s3_key = file_name

        # Upload the file
        try:
            s3_client.upload_file(file_path, bucket_name, s3_key)
            print(f"File {file_name} uploaded successfully to {bucket_name}.")
        except Exception as error:
            print(f"Error uploading {file_name} to {bucket_name}: {error}")

        # Wait for 30 seconds before uploading the next file
        time.sleep(30)

# Call the function with my specific bucket name and local directory
upload_files_to_s3('my-bucket-s211100', '/home/ubuntu/image-folder/Images')