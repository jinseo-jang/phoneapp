from twilio.rest import TwilioRestClient
from configobj import ConfigObj
import time
import sys

cfg=ConfigObj('config.ini')
sid = cfg['twilio']['sid']
auth_token = cfg['twilio']['auth_token']
twilio_number = cfg['twilio']['twilio_number']

def make_call(url, to):
    client = TwilioRestClient(sid, auth_token)    
    call = client.calls.create(to=to,from_=twilio_number,url=url)

    for i in range(0,10):
        print (i)
        time.sleep(5)
        callinfo = client.calls.get(sid)
        print (callinfo.status)

if __name__ == "__main__":
    url = sys.argv[1]
    to = sys.argv[2]
    make_call(url, to)