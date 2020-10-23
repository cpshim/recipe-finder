# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, render_template, request, redirect, url_for, jsonify
from google.cloud import storage
from werkzeug.utils import secure_filename
import base64
import json
import requests
import os
import os.path

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'RU hack 2020-d51bbb47001c.json'

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route("/upload", methods=['GET', 'POST'])
def imagesubmit():
    if request.form.get('submit') == 'submit':
        f = request.files['image']
        image_content = f.read()
        base64string = base64.b64encode(image_content).decode('ascii')


        payload = {
                    "requests": [
                        {
                        "image": {
                            "content": base64string
                        },
                        "features": [
                            {
                            "maxResults": 5,
                            "type": "LABEL_DETECTION"
                            }
                        ]
                        }
                    ]
                }

        r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDznLTP06V-vRpwp6HN_hguKi1aRCQCA5A", json=payload)
        b = r.json()

        ingredients = ""
        for i in b["responses"]:
            for j in i["labelAnnotations"]:
                ingredients = ingredients + j["description"] + ","
        
        ingredients = "&ingredients=" + ingredients[:-1]

        apiRequest = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=44442630cdde49dc974fafce1a6ff239"
        numberOfResults = int(request.form['amount'])
        number = "&number=" + str(numberOfResults)
        strings = apiRequest + ingredients + number
        c = requests.get(strings)
        a = c.json()
        return render_template('results.html', data=a, num=numberOfResults)
    return render_template('upload.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/faq')
def faq():
	return render_template('about.html')

@app.route('/searchbyingredients', methods=['GET', 'POST'])
def searchByIngredients():
    if request.method == 'POST':
        ingredients = "&ingredients=" + request.form['ingredients']
        ingredients = ingredients.replace(" ", "")
        apiRequest = "https://api.spoonacular.com/recipes/findByIngredients?apiKey=44442630cdde49dc974fafce1a6ff239"
        numberOfResults = int(request.form['amount'])
        number = "&number=" + str(numberOfResults)
        strings = apiRequest + ingredients + number
        r = requests.get(strings)
        b = r.json()
        return render_template("results.html", data = b, num = numberOfResults)
    return render_template("search.html")


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
