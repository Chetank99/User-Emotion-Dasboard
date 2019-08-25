# coding: utf-8
import boto3
import csv
import time
import cv2
import json
import requests
from clarifai.rest import ClarifaiApp

def compute():
    data_json = open('mood.json')
    data=json.load(data_json)

    face = data["FaceDetails"][0]

    lower_age = face['AgeRange']['Low']
    upper_age = face['AgeRange']['High']

    smile = face['Smile']
    if (smile['Value']== True):
        smily = 'Smiling Customer'
    else:
        smily = 'Customer not Smiling'

    feel = face['Emotions']

    emo_positive = []
    for i in range(0,8):
        if feel[i]['Type'] in ('HAPPY','CALM','SURPRISED'):
            emo_positive.append(feel[i]['Confidence'])
    
    emo_negative = []
    for i in range(0,8):
        if feel[i]['Type'] in ('DISGUSTED','ANGRY','SAD'):
            emo_negative.append(feel[i]['Confidence'])

    emo_score = [emo_positive[0]+emo_positive[1]+emo_positive[2],emo_negative[0]+emo_negative[1]+emo_negative[2]]

    if(emo_score[0] < emo_score[1]):
        feedback = 'Negative'
    else:
        feedback = 'Positive'
    
    gender = face['Gender']['Value']

    dev = ClarifaiApp(api_key='b22d386602114f2cbbca44b0f2b06ce0')
    model = dev.models.get('demographics')
    response = model.predict_by_filename('photo.jpg')
    temp = response['outputs'][0]
    race_json = json.dumps(temp)
    race_json = json.loads(race_json.replace("\'", '"'))
    race = race_json['data']['regions'][0]['data']['face']['multicultural_appearance']['concepts'][0]['name']

    temp = {
    "feed": feedback,
    "smile": smily,
    "gender": gender,
    "lower": lower_age,
    "upper": upper_age,
    "race": race
    }

    op_file = json.dumps(temp)
    results = json.loads(op_file.replace("\'", '"'))

    with open('disp.json', 'w') as f:
            json.dump(results, f,indent=4)

    return None

def disp():
    compute()
    with open('disp.json') as f:
        data = json.load(f)
    disp_vals = [data['feed'],data['smile'],data['gender'],data['lower'],data['upper'],(data['lower']+data['upper'])/2,data['race']]

    return disp_vals

    




