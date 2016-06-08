from flask import Flask, request, render_template, redirect, url_for
from flask import make_response, send_from_directory
from werkzeug import secure_filename
import os

from pickle import load
from re import subn
from nltk import word_tokenize

from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import sys

# Natural language normalizing
def normalize(f, stemmer = None):
	f = [x.lower() for x in f]
	f = [x.replace("\\n"," ") for x in f]		
	f = [x.replace("\\t"," ") for x in f]		
	f = [x.replace("\\xa0"," ") for x in f]
	f = [x.replace("\\xc2"," ") for x in f]

	f = [x.replace(" u "," you ") for x in f]
	f = [x.replace(" em "," them ") for x in f]
	f = [x.replace(" da "," the ") for x in f]
	f = [x.replace(" yo "," you ") for x in f]
	f = [x.replace(" ur "," you ") for x in f]
	
	f = [x.replace("won't", "will not") for x in f]
	f = [x.replace("can't", "cannot") for x in f]
	f = [x.replace("i'm", "i am") for x in f]
	f = [x.replace(" im ", " i am ") for x in f]
	f = [x.replace("ain't", "is not") for x in f]
	f = [x.replace("'ll", " will") for x in f]
	f = [x.replace("'t", " not") for x in f]
	f = [x.replace("'ve", " have") for x in f]
	f = [x.replace("'s", " is") for x in f]
	f = [x.replace("'re", " are") for x in f]
	f = [x.replace("'d", " would") for x in f]

	# Stemming   
	if stemmer == None :  
		f = [subn("ies( |$)", "y ", x)[0].strip() for x in f]
		f = [subn("s( |$)", " ", x)[0].strip() for x in f]
		f = [subn("ing( |$)", " ", x)[0].strip() for x in f]
		f = [x.replace("tard ", " ") for x in f]
			
		f = [subn(" [*$%&#@][*$%&#@]+"," xexp ", x)[0].strip() for x in f]
		f = [subn(" [0-9]+ "," DD ", x)[0].strip() for x in f]
		f = [subn("<\S*>","", x)[0].strip() for x in f]	
	else :
		for i in range(len(f)):
			sen = list()
			for w in word_tokenize(f[i]):
				sen.append(stemmer.stem(w))
			f[i] = " ".join(sen)

	return f
#############################################

################# Test part #################
def testLModel(test_sen, model, vtzers):
	test_sen = normalize(test_sen)
	lst = list()
	for vtzer in vtzers:
		lst.append (vtzer.transform (test_sen))

	X_test = hstack(lst)
	pred = model.predict_proba(X_test)

	return pred[0][1]

#############################################

model_file = open('model.pickle', 'r')
vtzers_file = open('vtzers.pickle', 'r')
global modela
global vtzersa
print "Loading model..."
modela = load(model_file)
print "Loading vectorizers..."
vtzersa = load(vtzers_file)

app = Flask(__name__, template_folder='./')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/calculate')
def calculate():
	text = request.args.get('text', 0, type=str)
	result = testLModel([text], modela, vtzersa)
	ret = str(result*100)[:5]
	print text, ret
	return ret

@app.route('/test/<test_sen>')
def test(test_sen):
	ret = testLModel([test_sen], modela, vtzersa)
	print test_sen, ret
	
	return str(ret * 100)[:4] + '%'

<<<<<<< HEAD:detector.py
app.run(host='0.0.0.0', port=5000, debug=False)
=======
if __name__ == "__main__" :
	reload(sys)
	sys.setdefaultencoding('utf8')
	model_file = open('model.txt', 'r')
	vtzers_file = open('vtzers.txt', 'r')
	global modela
	global vtzersa
	modela = load(model_file)
	vtzersa = load(vtzers_file)
	app.run(host='0.0.0.0', port=5000, debug=True)
>>>>>>> 140106cab8068df4fd06015a26eede084962264e:app.py

