import streamlit as st
import streamlit as st
import streamlit.components.v1 as components

from flask import Flask, request, jsonify
import requests
import json

st.title("Atom (Currency converter chat bot)")


# Creating flask app
app = Flask(__name__)


def fetch_conversion_factor(source,destination):

    url = "https://api.apilayer.com/currency_data/live?source={}&currencies={}".format(source,destination)

    payload = {}
    headers= {
    "apikey": "yLUCp0RirJjm6tfrJdEVMyXxp8P3F0la"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.text
    #result = '{"success": true,"timestamp": 1682156283,"source": "USD","quotes": {"USDINR": 82.04085}}'


    extracted = json.loads(result)
    print('ext:',extracted)
    return extracted["quotes"][source+destination]

@app.route("/",methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = round((float(amount) * float(cf)),2)
    bot_response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    print("bot_response:",bot_response)
    print("{} {} is {} {}".format(amount,source_currency,final_amount,target_currency))

    return jsonify(bot_response)


if __name__ == '__main__':
    app.run()



