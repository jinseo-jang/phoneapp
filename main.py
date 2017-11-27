import os, time
from flask import Flask, request, jsonify, json
import json
from twilio import twiml
from twilio.rest import Client
# from twilio.rest.resources import Call
from twilio.twiml.voice_response import VoiceResponse, Say, Gather
from configobj import ConfigObj

cfg=ConfigObj('config.ini')
SID = cfg['TWILIO']['SID']
AUTH_TOKEN = cfg['TWILIO']['AUTH_TOKEN']
TWILIO_NUMBER = cfg['TWILIO']['TWILIO_NUMBER']
BASE_URL = cfg['WEBSERVER']['BASE_URL']

app = Flask(__name__)

@app.route('/')
def index():
    """Returns standards text response to show app is working."""
    print ("test")
    return str("Bottle app up and running!")

@app.route('/callstatus', methods=['POST'])
def call_status():
    print (request.headers['Content-Type'])
    callsid=request.form['CallSid']
    callstatus=request.form['CallStatus']
    tonumber=request.form['To']
    print ("===========================================================")
    message='Callsid: {} | ToNumber: {} | Callstatus: {} |'.format(callsid,tonumber,callstatus)
    print (message) 
    response = VoiceResponse()
    response.say(message)
    return str(response), 200, {'Content-Type': 'text/xml'}

@app.route('/message', methods=['GET','POST'])
def message():
    name ="엠피 어플리케이션이 다운 되었어요. 조치 해주세요."
    response = VoiceResponse()    
    response.say(name, voice='alice',language='ko-KR')
    response.hangup()
    return str(response)

@app.route('/make-call/<phone_no>', methods=['GET'])
def make_call(phone_no):
    client = Client(SID, AUTH_TOKEN)
    calls = client.calls.create(
        to=phone_no,
        from_=TWILIO_NUMBER,
        url=BASE_URL +'/message',
        status_callback=BASE_URL + '/callstatus',
        status_callback_method="POST",
        status_callback_event=["initiated", "ringing", "answered", "completed"])

    return str('phoned call to' + phone_no +'!')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)