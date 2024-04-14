import boto3

# Create EC2 instance
ec2_client = boto3.client('ec2')

# Define parameters for the EC2 instance
ec2_parameters = {
    'ImageId': 'ami-080e1f13689e07408',
    'InstanceType': 't2.micro',
    'KeyName': 'labsuser',
    'MaxCount': 1,
    'MinCount': 1,
    'SubnetId': 'subnet-04670beee297d04c4',  # Specify the subnet ID here
    'TagSpecifications': [
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'MyInstanceNames211100'
                }
            ]
        }
    ]
}

try:
    response = ec2_client.run_instances(**ec2_parameters)
    instance_id = response['Instances'][0]['InstanceId']
    print(f"EC2 instance created with ID: {instance_id}")
except Exception as e:
    print(f"Error creating EC2 instance: {str(e)}")

if __name__ == "__main__":
    s3_bucket_name = 'my-bucket-s211100'
    queue_arn = 'arn:aws:sqs:us-east-1:323307001570:MySQSQueues211100'

    # Create S3 bucket
    s3_client = boto3.client('s3')
    try:
        s3_client.create_bucket(Bucket=s3_bucket_name)
        print(f"S3 Bucket '{s3_bucket_name}' created")
    except Exception as e:
        print(f"Error creating S3 bucket: {str(e)}")

    # Store SQS queue ARN in S3 bucket
    try:
        response = s3_client.put_object(
            Bucket=s3_bucket_name,
            Key='queue_arn.txt',
            Body=queue_arn.encode()
        )
        print(f"Queue ARN stored in S3 bucket {s3_bucket_name}")
    except Exception as e:
        print(f"Error storing Queue ARN in S3 bucket: {str(e)}")

   # Set up notification configuration for S3 bucket and SQS
try:
    response = s3_client.put_bucket_notification_configuration(
        Bucket='my-bucket-s211100',
        NotificationConfiguration={
            'QueueConfigurations': [
                {
                    'QueueArn': queue_arn,
                    'Events': ['s3:ObjectCreated:*']
                }
            ]
        }
    )
    print("Notification configuration created for the bucket")
except Exception as e:
    print(f"Error setting up notification configuration: {str(e)}")