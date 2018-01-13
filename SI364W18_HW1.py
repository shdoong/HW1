## HW 1
## SI 364 W18
## 1000 points

#################################
#Code below to fix encoding errors on Windows
#  -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
from flask import Flask, request
import api_key_info


import requests
import json
import pprint

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
# Used News API, https://newsapi.org/ (for problem 4) and class notes/code as reference
# Did not work with anybody

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and
# go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask
app = Flask(__name__)
app.debug = True

#Problem 1
@app.route('/class')
def hello_to_you():
	return '<h1>Welcome to SI 364!</h1>'

#Problem 2
@app.route('/movie/<nameofmovie>')
def movie(nameofmovie):
	r = requests.get('https://itunes.apple.com/search?', params= {'term':nameofmovie, 'media':'movie', 'limit':1}) 
	response_dict = json.loads(r.text)
	return (str(response_dict))

#Problem 3
@app.route('/question')
def enterData():
	s = """<!DOCTYPE html>
		<html>
		<body>
		<form action = "/result" method = "POST">
		  Enter your favorite number:<br>
		  <input type="text" name="numb">
		  <br>
		  <input type="submit" value="Submit">
		</form>
		</body>
		</html>"""
	return s

@app.route('/result', methods = ['POST', 'GET'])
def displayData():
	if request.method == 'POST':
		return "Double your favorite number is {}".format(int(request.form['numb']) * 2)

#Problem 4
@app.route('/problem4form', methods = ['GET', 'POST'])

def form():
	s = """<!DOCTYPE html>
		<html>
		<body>
		<form method = "POST">
		  What topic would you like to search top headlines for?<br>
		  <input type="text" name="phrase">
		  <br>

		  Which source would you like to search from?<br>
		  <input type="checkbox" name="source", value = "bbc-news"> BBC News
		  <br>
		  <input type="checkbox" name="source", value = "abc-news"> ABC News
		  <br>
		  <input type="checkbox" name="source", value = "cnn"> CNN
		  <br>
		  <input type="checkbox" name="source", value = "associated-press"> Associated Press
		  <br>
		  <input type="checkbox" name="source", value = "the-wall-street-journal"> The Wall Street Journal
		  <br>
		  <input type="checkbox" name="source", value = "buzzfeed"> BuzzFeed
		  <br>
		  <input type="submit" value="Submit">
		</form>
		</body>
		</html>"""

	if request.method == "POST":
		sources_info = request.form.getlist('source')
		resp = []
		API_KEY = api_key_info.api_key
		for x2 in sources_info:
			try:
				param = {'apiKey':API_KEY, 'q':request.form['phrase'],'sources':x2}
				r = requests.get('https://newsapi.org/v2/top-headlines?', params=param)
				response = json.loads(r.text)
				if response['totalResults'] != 0:
					response2 = '<br>'.join(['<strong>Source: </strong>' + x2 + '<br>' + '<strong>Title: </strong>' + x['title'] + '<br>' + '<strong>Description: </strong>' + x['description'] + '<br>' + '<strong>URL: </strong>' + x['url'] + '<br>' for x in response['articles']])
				else:
					response2 = 'No Top Headlines from ' + str(x2) + ' for ' + request.form['phrase']  
			except:
				response2 = "Error"
			resp.append(response2)
		return s + '<br><strong><h2>Top Headlines for ' + request.form['phrase'] + '</strong></h2>' + '<br>'.join(resp)
	else:
		return s

if __name__ == '__main__':
	app.run()


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' 
#you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', 
#you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the 
#animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, 
#and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }

## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, 
#you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>".
# For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". 
#Careful about types in your Python code!
## You can assume a user will always enter a number only.


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, 
# and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the 
# submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). 
# The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
