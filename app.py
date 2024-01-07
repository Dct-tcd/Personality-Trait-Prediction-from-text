from flask import Flask, render_template, request, url_for, redirect
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from Model import Model,train_models
from Predict import Predictor
from Scraper_Face import  FBScraper, ExecFace , Grapher
from bson import json_util
import json
import yaml
import pickle
from flask import Flask, render_template, request
import csv
import os 
# import google_bard
# import openai
import openai
from openai.error import RateLimitError

openai.api_key = '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'
  

UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)

# prediction
@app.route("/", methods= ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            textpredict = request.form['text']
            print(textpredict, "text")
            with open('post.txt', 'a') as save:
                save.write(textpredict + '\n')
        except KeyError:
            # Handle the case where the 'text' field is not present in the form
            return render_template('error.html', message="Invalid form data")
        return redirect(url_for('facebook'))

    # Render the index.html template for both GET and successful POST requests
    return render_template('index.html')

# def predict_text():
#     if textpredict is not None:
#         p = Predictor()
#         global prediction
#         prediction = p.predict([textpredict])
#         return redirect(url_for('result'))
#     else:
#         return str("-----------No Text to Predict------------")

@app.route("/facebook/", methods= ['GET', 'POST'])
def facebook():     
    if request.method == 'POST':
        try:
            email = request.form['email']
            passw = request.form['passw']
            profile = request.form['profile']
            write_yaml(email, passw, profile)
            prediction  = ExecFace()
            return redirect(url_for('result'))
        except: 
            # prediction  = ExecFace()
            return redirect(url_for('result'))
    return render_template('facebook.html')

@app.route("/result/", methods= ['GET', 'POST'])
def result():
    # p = Predictor()
    # global prediction
    prediction = ExecFace()
    pred = prediction
    print(prediction,"pred")
    nombre = prediction.pop(0) 
    return render_template('result.html', pred = prediction, nom = nombre)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/answer/', methods=['GET','POST'])
def answer():
    prediction = Grapher()     
    answer = prediction
  
    # Generate bar chart
    bar_chart = generate_bar_chart(answer)

    # Generate line chart
    line_chart = generate_line_chart(answer)

    # Encode the images to base64
    bar_chart_base64 = encode_image_to_base64(bar_chart)
    line_chart_base64 = encode_image_to_base64(line_chart)

    return render_template('answer.html', bar_chart_base64=bar_chart_base64, line_chart_base64=line_chart_base64)


def generate_bar_chart(answer):
    # Extract numerical values for plotting
    selected_data = answer[1::3]
    numeric_values = [float(value) for value in selected_data if '.' in value]

    # Assign sequential x values
    x_values = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']
    y_values = numeric_values

    # Plot the bar graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x_values, y_values, color=['#1f78b4', '#ff7f00'], width=0.8)
    
    ax.set_xlabel('Traits', labelpad=15)
    ax.set_ylabel('Probability Scores', labelpad=15)
    ax.set_title('Bar Chart for Personality Traits')

    # Save the plot to a BytesIO object
    img_bytesio = BytesIO()
    fig.savefig(img_bytesio, format='png')
    img_bytesio.seek(0)

    # Close the plot to free up resources
    plt.close(fig)

    return img_bytesio

def generate_line_chart(answer):
    # Extract numerical values for plotting
    # selected_data = answer[1::3]
    numeric_values = [float(value) for value in answer[0::3] if '.' in value]
    print(numeric_values)
    # Define x-axis values for the Big Five traits
    big_five_traits = ['Openness', 'Conscientiousness', 'Extraversion', 'Agreeableness', 'Neuroticism']

    # Plotting the line chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(big_five_traits, numeric_values, marker='o')
    ax.set_xlabel('Big Five Traits')
    ax.set_ylabel('Trait Score')
    ax.set_title('Line Chart for Personality Traits')

    # Save the plot to a BytesIO object
    img_bytesio = BytesIO()
    fig.savefig(img_bytesio, format='png')
    img_bytesio.seek(0)

    # Close the plot to free up resources
    plt.close(fig)

    return img_bytesio

def encode_image_to_base64(image):
    # Encode the image to base64
    image_base64 = base64.b64encode(image.read()).decode('utf-8')
    return image_base64


def write_yaml(nemail, npassword, nprofile):
    data = dict(
    email= nemail, password= npassword, profile_url= nprofile)
    with open('.Fb_login_creds.yaml', 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
        


if __name__ == '__main__':
    app.run(debug=True)
