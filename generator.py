import pickle
import csv
import re
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack

TRAIN_FILE	  = "train.csv"

########### Ancillary functions ###########

# From .csv file to array
def readCsv(fname, skipFirst = True, delimiter = ","):
	reader = csv.reader (open (fname, "rb"), delimiter = delimiter)
	rows = []
	for row in reader :
		if skipFirst :
			skipFirst = False
			continue
		rows.append(row)
	return rows

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
		f = [re.subn("ies( |$)", "y ", x)[0].strip() for x in f]
		f = [re.subn("s( |$)", " ", x)[0].strip() for x in f]
		f = [re.subn("ing( |$)", " ", x)[0].strip() for x in f]
		f = [x.replace("tard ", " ") for x in f]
			
		f = [re.subn(" [*$%&#@][*$%&#@]+"," xexp ", x)[0].strip() for x in f]
		f = [re.subn(" [0-9]+ "," DD ", x)[0].strip() for x in f]
		f = [re.subn("<\S*>","", x)[0].strip() for x in f]	
	else :
		for i in range(len(f)):
			sen = list()
			for w in nltk.word_tokenize(f[i]):
				sen.append(stemmer.stem(w))
			f[i] = " ".join(sen)

	return f
#############################################

########### Machine Learning Part ###########

# Machine learns for n-grams ( char or word )
def ngrams(train_sen, train_label, start, final, analyzer_char = False):
	analyzer_type = 'word'
	if analyzer_char:
		analyzer_type = 'char'
	train_sen = normalize(train_sen)

	# TF IDF --> frequent words are less important
	vtzer = TfidfVectorizer (ngram_range = (start, final), stop_words = 'english', analyzer = analyzer_type, sublinear_tf = True)

	X_train = vtzer.fit_transform (train_sen)
	Y_train = train_label
	return X_train, vtzer

# Machine learns for special cases
def specialCases(train_sen, train_label):
	g = [x.lower().replace("you are"," SSS ").replace("you're"," SSS ").replace(" ur ", " SSS ").split("SSS")[1:] for x in train_sen]

	f = []
	for x in g:
		fts = " "
		x = normalize(x)
		for y in x:
			w = y.strip().replace("?",".").split(".")
			fts = fts + " " + w[0]		
		f.append(fts)
	
	X_train, vtzer = ngrams(train_sen, train_label, 1, 1)
	return X_train, vtzer

# Returns model which consider significant cases
def learn(train_sen, train_label, vector_add = False):

	print "Unigram word learning..."
	X_train1, vtzer1 = ngrams(train_sen, train_label, 1, 1)
	print "Bigram word learning..."
	X_train2, vtzer2 = ngrams(train_sen, train_label, 2, 2)
	print "Trigram word learning..."
	X_train3, vtzer3 = ngrams(train_sen, train_label, 3, 3)   
	print "Quadrigram char learning..." 
	X_train4, vtzer4 = ngrams(train_sen, train_label, 4, 4, analyzer_char = True)  
	print "Quinquegram char learning..."  
	X_train5, vtzer5 = ngrams(train_sen, train_label, 5, 5, analyzer_char = True)  
	print "Special case learning..."
	X_train6, vtzer6 = specialCases(train_sen, train_label)

	# Sum of all model
	vtzers = [vtzer1, vtzer2, vtzer3, vtzer4, vtzer5, vtzer6]
	X_train = hstack([X_train1, X_train2, X_train3, X_train4, X_train5, X_train6])
	Y_train = train_label
	
	print "Construct LogisticRegression.."
	model = linear_model.LogisticRegression( C = 3 )
	model.fit(X_train, Y_train)
	return model, vtzers
###########################################

################ Main Part ################

if __name__ == "__main__":
	train_data = readCsv(TRAIN_FILE)

	train_sen = [x[2] for x in train_data]
	train_label = [x[0] for x in train_data]
	
	print("============================== Insult Comment Training ==============================");
	model, vtzers = learn(train_sen, train_label)

	model_file = open('model.pickle', 'wb')
	vtzers_file = open('vtzers.pickle', 'wb')
	pickle.dump(model, model_file)
	pickle.dump(vtzers, vtzers_file)

