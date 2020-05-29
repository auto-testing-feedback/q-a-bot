import json
from .. import matcher
from flask import Blueprint, jsonify, render_template
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

api = Blueprint('api', __name__, template_folder='templates')
corpus_raw = json.loads(open('db/corpus-raw.json').read())
corpus_processed = open('db/corpus-processed.json', 'r+')
corpus_processed = json.loads(corpus_processed.read())['corpus']

corpus = corpus_processed

@api.route('/trigger_update')
def trigger_update():
	exec(open('main/pull_data.py').read())
	exec(open('main/update_corpus.py').read())
	return '', 200 

@api.route('/corpus_stats', methods=['GET'])
def get_corpus_stats():
	stats = {
		'total_posts': len(corpus),
		'by_term': {}
	}
	for post in corpus:
		if post['term'] not in stats['by_term']:
			stats['by_term'][post['term']] = 0
		stats['by_term'][post['term']] += 1
	return json.dumps(stats) 

@api.route('/corpus_terms', methods=['GET'])
def get_corpus_terms():
	terms = []
	for post in corpus:
		if post['term'] not in terms:
			terms.append(post['term'])
	return json.dumps(terms)

@api.route('/term_folders/<term>', methods=['GET'])
def get_term_folders(term):
	folders = {'other': 0} 
	for post in corpus:
		if post['term'] == term:
			for folder in post['folders']:
				if folder not in folders:
					folders[folder] = 0
				folders[folder] += 1
	return json.dumps(folders)

@api.route('/<term>/titles/', methods=['GET'])
def get_term_post_titles(term):
	posts = []
	for post in corpus:
		if post['term'] == term:
			posts.append(post)
	return json.dumps(posts)

@api.route('/<term>/<post_id>', methods=['GET'])
def get_term_post(term, post_id):
	post_id = int(post_id)
	for post in corpus:
		if post['term'] == term:
			if post['id'] == post_id:
				return json.dumps(post)
	return '', 404

@api.route('/report/<term>/<post_id>', methods=['GET'])
def get_post_report(term, post_id):
	report_post = None
	for post in corpus:
		if post['term'] == str(term):
			if post['id'] == int(post_id):
				report_post = post
	report = {
		'post': report_post,
		'similar': []
	}
	# most similar posts
	for post in corpus:
		if post == report_post:
			continue
		if len(set(report_post['folders']).intersection(post['folders'])) > 0:
			st = matcher.get_similarity(report_post['title'], post['title'])
			sb = matcher.get_similarity(report_post['body'], post['body'])
			s = st * matcher.beta + sb * (1 - matcher.beta)
			if s > 0:
				post_copy = post.copy()
				post_copy['s'] = s
				report['similar'].append(post_copy)
	report['similar'] = sorted(report['similar'], key=lambda i: i['s'], reverse=True)
	report['similar'] = report['similar'][0:5]
	return render_template('report.html', report=report) 

@api.route('/similarities', methods=['GET'])
def get_similarities():
	ss = []
	for i in range(7, len(corpus) - 1):
		for j in range(i + 1, len(corpus)):
			if len(set(corpus[i]['folders']).intersection(corpus[j]['folders'])) > 0:
				st = matcher.get_similarity(corpus[i]['title'], corpus[j]['title'])
				sb = matcher.get_similarity(corpus[i]['body'], corpus[j]['body'])
				s = st * matcher.beta + sb * (1 - matcher.beta)
				ss.append({
					't1': corpus[i]['term'],
					'i1': corpus[i]['id'],
					't2': corpus[j]['term'],
					'i2': corpus[j]['id'],
					's': s
				})
	ss = sorted(ss, key=lambda i: i['s'], reverse=True)
	return json.dumps(ss)

@api.route('/figure1', methods=['GET'])
def get_figure1():
	return jsonify({'src': ''}) 