#!/bin/bash

aws sns create-topic --name MyTopic_s211100

aws sns subscribe --topic-arn arn:aws:sns:us-east-1:323307001570:MyTopic_s211100 --protocol email --notification-endpoint j.ekhator@alustudent.com