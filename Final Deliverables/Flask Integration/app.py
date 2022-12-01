import numpy as np
from flask import Flask, request, jsonify, render_template
import inputScript
import json
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "tRhJXIhDiMk3TOZ9wpQAHTKaM-oCQnQAXG_vETNNmjWt"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

#load model
app = Flask(__name__)

@app.route('/')
def predict():
    return render_template('index.html',result="")
@app.route('/',methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    url = request.form['url']
    print(url)
    checkprediction = inputScript.main(url)
    payload_scoring = {"input_data": [{"fields": ['having_IPhaving_IP_Address', 'URLURL_Length', 'Shortining_Service',
       'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
       'having_Sub_Domain', 'SSLfinal_State', 'Domain_registeration_length',
       'Favicon', 'port', 'HTTPS_token', 'Request_URL', 'URL_of_Anchor',
       'Links_in_tags', 'SFH', 'Submitting_to_email', 'Abnormal_URL',
       'Redirect', 'on_mouseover', 'RightClick', 'popUpWidnow', 'Iframe',
       'age_of_domain', 'DNSRecord', 'web_traffic', 'Page_Rank',
       'Google_Index', 'Links_pointing_to_page', 'Statistical_report'], "values":checkprediction}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/1711a43f-2f99-41a9-bc34-6c8faf7aef78/predictions?version=2022-11-22', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    predictions=response_scoring.json()
    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]
    if(pred==1):
        output="Your are safe!!  This is a Legitimate Website"
    else:
        output="You are on the wrong site. Be cautious!"
    return render_template('index.html', result=output,url=url)
if __name__ == "__main__":
    app.run( debug=True)