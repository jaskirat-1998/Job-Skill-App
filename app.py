from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
from helper import get_top_n_job_ids, get_job_data, get_wordcloud_data, class_skills, get_download_data

app = Flask(__name__)


# Page redirects

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/skill')
def skill():
    return render_template('skill.html')


@app.route('/job')
def job():
    return render_template('job.html')


@app.route('/wordcloud')
def wordcloud():
    return render_template('wordcloud.html')

# APIs

@app.route("/job_data", methods=['POST'])
def job_data_api():
    '''
    This API accepts a POST request with parameter skill (the json format should be {'skills':'python, R'} ).
    The API returns the job posting data based on the skills entered
    '''
    jsondata = request.get_json()
    skills = jsondata['skills']
    result = get_job_data(get_top_n_job_ids(skills,100))
    return json.dumps(result), 200

@app.route("/wordcloud", methods=['POST'])
def wordcloud_api():
    '''
    This API accepts a POST request with parameter skill (the json format should be {'skills':'python, R'} ).
    The API returns the word cloud data based on the skills entered
    '''
    jsondata = request.get_json()
    print(jsondata)
    skills = jsondata['skills']
    result = get_wordcloud_data(skills)
    return jsonify(result), 200

@app.route("/class_skills", methods=['POST'])
def class_skill_api():
    '''
    This API accepts a POST request with parameter class (the json format should be {'class':'software_engineer'} ).
    The API returns the top 10 skills mentioned in the job postings for that job class
    '''
    jsondata = request.get_json()
    class_ = jsondata['class']
    result = class_skills[class_]
    return json.dumps(result), 200


@app.route('/download', methods=['POST'])
def download_csv():
    '''
    This API accepts a POST request 
    The API returns the json data that is in csv format
    '''
    return json.dumps(get_download_data()), 200 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
