#!/bin/bash

# Set variables
LOCAL_IMAGE_FOLDER="Images/"
EC2_USER="ubuntu"
EC2_PUBLIC_IP="54.204.166.18"
EC2_IMAGE_DESTINATION="/home/ubuntu/image-folder"

# Upload images to EC2 instance
echo "Uploading images from $LOCAL_IMAGE_FOLDER to EC2..."
scp -i labsuser.pem -r "$LOCAL_IMAGE_FOLDER" $EC2_USER@$EC2_PUBLIC_IP:$EC2_IMAGE_DESTINATION

# Check if the upload was successful
if [ $? -eq 0 ]; then
    echo "Images uploaded successfully to EC2 instance."
else
    echo "Failed to upload images to EC2 instance."
fi
