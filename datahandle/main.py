# coding:utf-8
import logging
import os
from flask import Flask
from gdrive import gettodayword
from flask import render_template
from flask import request
from flask import g
app = Flask(__name__)

@app.route('/')
def start():

#     file = open("testfile.txt","w") 
#      
#     file.write("and this is another line.") 
#     file.close() 
#     curlist = os.listdir("/home/shikaiwenchina")
    return "start OK"


@app.route('/settodayword', methods=['GET','POST'])
def settodayword():
    app.app_context().app
    return render_template('todayword.html')


myglobal = {}
myglobal["todayword"] = ""

# todayword = ""
@app.route('/dosettodayword', methods=['GET','POST'])
def dosettodayword():
    todayword = request.form["wordinfo"]
    myglobal["todayword"] = todayword
    return "1"

@app.route('/gettodayword', methods=['GET','POST'])
def gettodayword():
    return myglobal["todayword"]


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8000, debug=True)