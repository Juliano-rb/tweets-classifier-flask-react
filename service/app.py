from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import joblib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
# from flask_cors import CORS
import re
import requests

# Removendo as tags htmls:
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Removendo alguns caracteres especiais como colchetes
def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

# Função que remove os caracteres especiais:
def remove_special_characters(text, remove_digits=True):
    pattern=r'[^a-zA-z0-9\s]'
    text=re.sub(pattern,'',text)
    return text


# Função que limpa o texto
def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    text = remove_special_characters(text)
    return text
def get_tweet_text(tweetId):
	url = "https://api.twitter.com/1.1/statuses/show.json"
	querystring = {"id":tweetId}
	payload = ""

	headers = {
		"cookie": "personalization_id=%22v1_2vEY7v%2FJY03piVVQMK%2FCuQ%3D%3D%22; guest_id=v1%253A161754684942468911",
		"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRSuAAAAAAACe%2BbZ4OUwymktmjfoz91YvnuF9Y%3DRkIKfoLgZmBzU2Z2ZVXePooIzUDS2gf5YuDoIFZb9z4DdXTaNs"
	}

	response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
	response_json = response.json()
	return response_json['text']

flask_app = Flask(__name__)
# CORS(flask_app)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "Tweets Sentiment Classifier", 
		  description = "Predict the sentiment of tweets")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params', 
				  {'tweet': fields.String(required = True, 
				  							   description="Text containing the id of a tweet", 
    					  				 	   help="TweetId cannot be blank")})

classifier = joblib.load('classifier_tweets.joblib')
vectorizer = joblib.load('count_vectorizer.joblib')


@name_space.route("/")
class MainClass(Resource):

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)		
	def post(self):
		try: 
			formData = request.json
			print(formData)
			#print('review:', formData['review'])
			#data = [val for val in formData.values()]
			tweet_text = get_tweet_text(formData['tweet'])
			print(tweet_text)
			data = [denoise_text(tweet_text)]
			data =  vectorizer.transform(data)          
			prediction = classifier.predict(data)
			label = { 0: "Negative", 2: "Positive"}
			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Prediction: " + label[prediction[0]] + " (" + str(np.round(np.max(classifier.predict_proba(data)),2)*100) + "%)"
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})