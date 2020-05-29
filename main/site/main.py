from flask import Flask, Blueprint, render_template
from . import api

app = Flask(__name__)
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def index():
	return render_template('index.html') 

@app.route('/nlp-demo')
def nlp_demo():
	return render_template('nlp-demo.html') 

@app.route('/about')
def about():
	return render_template('about.html')