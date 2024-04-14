import json
import boto3

# Initialize S3 and SQS clients
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')

def handler_for_lambda(event, context):
    # Retrieve messages from the SQS queue
    for record in event['Records']:
        # Extract message body containing image file name from SQS record
        try:
            message_body = json.loads(record['body'])
            image_file = message_body['image_file']

            # Replace these variables with the appropriate values from EC2_s211100.py
            # Example: bucket_name = 'myS3Buckets211100'
            bucket_name = 'my-bucket-s211100'

            # Upload image file to S3 bucket
            s3_client.upload_file(image_file, bucket_name, image_file)

            print(f"Uploaded image file '{image_file}' to S3 bucket '{bucket_name}'")
        except Exception as e:
            print(f"Failed to process SQS message: {e}")

    return {
        'statusCode': 200,
        'body': 'Message processing completed successfully'
    }
