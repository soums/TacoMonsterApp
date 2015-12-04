# -*- coding: UTF8 -*-
from flask import Flask, request, redirect
import twilio.twiml

import requests
import postmates as pm
api = pm.PostmatesAPI("60e1b787-0166-4a41-a680-1a268ded50e6", "cus_JMrDSkWM3shq5k")

app = Flask(__name__)

@app.route('/') 
def hello_world():
    return 'Hello World!'

@app.route('/taco', methods=['GET', 'POST'])
def collect_delivery_address ():
 
    from_number = request.values.get('From', None)
    
    delivery_address = request.values.get('Body', None)
    pickup = '2288 Mission St, San Francisco, CA'
    response = requests.post('https://api.postmates.com/v1/customers/cus_JMrDSkWM3shq5k/delivery_quotes', 
    	auth=('60e1b787-0166-4a41-a680-1a268ded50e6', ''), 
    	data = {"pickup_address":pickup, "dropoff_address":delivery_address})
    print response
    print response.json()
    response_data=response.json()

    message=" "
    if response.status_code==200: 
    	fee=response_data['fee']/100.00
    	dropoff_eta=response_data['duration']
    	message=u"Your 🌮 delivery costs $%.02f and will arrive in %s minutes. 🌮 costs extra 💰" % (fee, dropoff_eta) 
    elif response.status_code==400: 
    	message="Your address must be in form '123 Jones St, San Francisco, CA'"

    resp = twilio.twiml.Response()
    resp.message(message)
 
    return str(resp)


if __name__ == '__main__':
	app.run(debug=True)
