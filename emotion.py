# coding: utf-8
import boto3
import csv
import time
import cv2
import json

def visual():
	camera_port = 0
	camera = cv2.VideoCapture(camera_port)
	time.sleep(0.1)  # If you don't wait, the image will be dark
	return_value, image = camera.read()
	cv2.imwrite("photo.jpg", image)
	del(camera)

	with open('credentials.csv','r') as input:
		next(input)
		reader = csv.reader(input)
		for line in reader:
			access_key_id = line[2]
			secret_access_key = line[3]

	photo = "photo.jpg"

	client = boto3.client('rekognition',region_name='ap-south-1',aws_access_key_id = access_key_id,aws_secret_access_key=secret_access_key)

	with open(photo,'rb') as source_image:
		source_bytes = source_image.read()
	response = client.detect_faces(Image={'Bytes':source_bytes},Attributes=['ALL'])
	json_file = json.dumps(response,indent=4)
	with open('mood.json', 'w') as f:
				json.dump(response, f)
	print(response)

	return None

