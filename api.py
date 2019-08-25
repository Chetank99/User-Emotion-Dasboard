# coding: utf-8
from flask import Flask,request,redirect, render_template,url_for,jsonify
import boto3
import csv
import time
import cv2
import json


from emotion import visual
from face import compute,disp

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    visual()
    vals = disp()

    return render_template('index.html',vals=vals)

@app.route('/detailed.html')
def main():
   return render_template('detailed.html')

@app.route('/info.html')
def info():
   with open('mood.json') as f:
        data = json.load(f)
   face = data["FaceDetails"][0]
   
   specs = face['Eyeglasses']['Value']
   sun_glasses = face['Sunglasses']['Value']
   beard = face['Beard']['Value']
   mustache = face['Mustache']['Value']
   age = (face['AgeRange']['Low'] + face['AgeRange']['High'])/2
   gender = face['Gender']['Value']
   eyes = face['EyesOpen']['Value']
   mouth = face['MouthOpen']['Value']

   return render_template('info.html',specs=specs,sun_glasses=sun_glasses,beard=beard,mustache=mustache,age=age,gender=gender,eyes=eyes,mouth=mouth)



if __name__ == '__main__':
   app.run(debug = True)
