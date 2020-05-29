import math, re, string, json
import nltk
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

alpha = 0.5
beta = 0.2

corpus_file = open('db/corpus-processed.json', 'r+')
corpus = json.loads(corpus_file.read())['corpus']

stop_words = set(nltk.corpus.stopwords.words('english'))
link_words = ['http', '.com']
remove_words = ['\u2019', '\u00a0']

def clean(text):
	text = BeautifulSoup(text, features='html.parser').text
	return text 

def process(text):
	text = text.lower()
	text = BeautifulSoup(text, features='html.parser').get_text()
	old_text = text
	text = []
	for word in re.split(' |\n', old_text):
		text.append(word)
	text = ' '.join(text)
	return text 

def compute_tf_table(sentence):
	tf_table = {} 
	split_sentence = sentence.split(' ')
	length = len(split_sentence)
	for word in split_sentence:
		if word not in tf_table:
			 tf_table[word] = 0
		tf_table[word] += 1 / length
	return tf_table

def compute_idf(word):
	df = 0
	for document in corpus:
		if word in document['title'] or word in document['body']:
			df += 1
	return math.log(len(corpus) / (df + 1))

def compute_tf_idf_table(sentence):
	tf_idf_table = compute_tf_table(sentence)
	for word in tf_idf_table:
		tf_idf_table[word] *= compute_idf(word)
	return tf_idf_table

def compute_tf_idf(word, sentence):
	return compute_tf_idf_table(sentence)[word]

def tf_idf_similarity(text1, text2):
	t1 = compute_tf_idf_table(text1)
	t2 = compute_tf_idf_table(text2)
	similarity = 0
	for word in t1:
		if word in t2:
			similarity += t1[word] * t2[word]
	return similarity

def fuzzy_similarity(text1, text2):
	return fuzz.partial_ratio(text1, text2) / 100 

def get_similarity(text1, text2):
	return tf_idf_similarity(text1, text2) * alpha + fuzzy_similarity(text1, text2) * (1 - alpha) 