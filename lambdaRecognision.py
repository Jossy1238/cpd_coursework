import json
import boto3

# Initialize Rekognition client
rekognition_client = boto3.client('rekognition')

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')

# Initialize SNS client
sns_client = boto3.client('sns')

# Specify the DynamoDB table names
entry_table_name = 'EntryDynamoDBTables211100'
vehicle_table_name = 'VehicleDynamoDBTables211100'


# SNS Topic ARN
topic_arn = "arn:aws:sns:us-east-1:323307001570:MyTopic_s211100"

def detect_labels_and_text(image_name):
    try:
        # Hardcode the bucket name
        bucket = 'my-bucket-s211100'

        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name
                }
            },
            MaxLabels=10,
            MinConfidence=70
        )

        labels = [label['Name'] for label in response['Labels']]

        text_response = rekognition_client.detect_text(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': image_name
                }
            }
        )

        detected_text = [text['DetectedText'] for text in text_response['TextDetections']]

        return labels, detected_text
    except Exception as e:
        print(f"Failed to detect labels and text: {e}")
        return [], []

def store_in_dynamodb(image_name, labels, detected_text):
    table = dynamodb.Table(entry_table_name)
    try:
        table.put_item(
            Item={
                'image_name': image_name,
                'Labels': labels,
                'DetectedText': detected_text
            }
        )
        print(f"Successfully stored data for image_name {image_name} in DynamoDB.")
    except Exception as e:
        print(f"Failed to store data in DynamoDB: {e}")
        

  # To Publish the message with a subject to the SNS topic
def notify_via_sns(message, subject):
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent to SNS topic {topic_arn}. Message ID: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send notification to SNS topic {topic_arn}: {e}")

def scan_vehicle_table(detected_text):
    table = dynamodb.Table(vehicle_table_name)
    response = table.scan()
    items = response['Items']
    match_found = False

    # Convert detected_text to a single string
    detected_text_str = ' '.join(detected_text)

    for item in items:
        if item['vehicle_id'] in detected_text_str:
            if item['Blacklisted']:
                # Log message for blacklisted vehicle
                
                message = f"Vehicle with ID {item['vehicle_id']} has been flagged as blacklisted."
                subject = "Alert: There is a Blacklisted Vehicle Detected"
                notify_via_sns(message, subject)
                match_found = True
            else:
                print(f"A match was identified for vehicle ID {item['vehicle_id']}, however, it is not listed as blacklisted.")
                match_found = True

    if not match_found:
        # Send SNS message indicating no match was found
        message = "There is no match for this entry."
        subject = "Alert: No Match Detected"
        notify_via_sns(message, subject)

        

def handler(event, context):
    try:
        body = json.loads(event['Records'][0]['body'])
        image_name = body['Records'][0]['s3']['object']['key']

        labels, detected_text = detect_labels_and_text(image_name)

        print(f"Detected Labels: {labels}")
        print(f"Detected Text: {detected_text}")
        
        # Store the results in DynamoDB
        store_in_dynamodb(image_name, labels, detected_text)

        # Scan the vehicle table for matches
        scan_vehicle_table(detected_text)

    except Exception as e:
        print(f"Failed to process SQS message: {e}")

    return {
        'statusCode': 200,
        'body': 'Message processing completed successfully'
    }
