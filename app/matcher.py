import re
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

N = 1000 # ??? research needs to be done here

stop_words = set(stopwords.words('english'))

def clean(string):
    string = string.encode('ascii', 'ignore').decode('ascii') 
    string = BeautifulSoup(string, features="html.parser").get_text()
    for i in "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n":
        string = string.replace(i, '')
    string = string.lower()
    new_string = ""
    for word in string.split(' '): # remove single character words
        if len(word) > 1:
            new_string += word + ' '
    return new_string

def questions_match(idf_data, q1, q2):
    # vectorize tf-idf values
    t1 = get_tf_idf_table(idf_data, q1['content'])
    t2 = get_tf_idf_table(idf_data, q2['content'])
    similarity = 0
    for word in t1:
        if word not in t2:
            continue
        similarity += t1[word] * t2[word]
    print(similarity)
    return similarity > N

def get_tf_table(string):
    tf_table = {}
    split_string = string.split(' ') # split string into words
    word_count = len(split_string)
    for word in split_string:
        if word in stop_words or len(word) < 2:
            continue
        if word not in tf_table:
            tf_table[word] = 0
        tf_table[word] += 1 / word_count
    return tf_table
  
def get_tf_idf_table(idf_data, sentence):
    tf_idf_table = {}
    tf_table = get_tf_table(sentence)
    for word in sentence.split(' '):
        if word not in tf_table or word not in idf_data:
            tf_idf_table[word] = 0
            continue
        tf_idf_table[word] = tf_table[word] * idf_data[word]
    return tf_idf_table