import requests
import json
import base64
from flask import Flask, render_template, request, redirect, url_for
import os
import config

app = Flask(__name__)

# direct to main.html
@app.route('/')
def main():
    #  if the image is already in the static folder, delete it
    if os.path.exists('static/result.jpg'):
        os.remove('static/result.jpg')

    return render_template('main.html')

@app.route('/result',  methods=['GET'])
def redirect_to_main():
    return redirect(url_for('main'))

# direct to result.html
@app.route('/result',  methods=['POST'])
def result():
    # get the image from the form
    image = request.files['image']
    # convert image to base64 string
    encoded_string = base64.b64encode(image.read()).decode('utf-8')
    # send image to api
    data = {'image': encoded_string}
    headers = {'Content-type': 'application/json'}
    response = requests.post(config.api_url, data=json.dumps(data), headers=headers)
    # get the result from api
    resp = eval(response.text)
    # get the image from api
    img_display = base64.b64decode(resp['image'][2:-1])
    # convert img_display to image to send to html
    # get the mfg date from api
    mfg_date = resp['mfg_date']
    # get the exp date from api
    exp_date = resp['expiry_date']
    # save the image to a file
    with open("static/result.jpg", "wb") as fh:
        fh.write(img_display)
    # direct to result.html
    return render_template('/result.html',mfg_date=mfg_date, exp_date=exp_date)

if __name__=='__main__':
    app.run(debug = False)