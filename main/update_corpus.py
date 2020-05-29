import os, time, json, argparse
import pprint
import piazza_api
import matcher

def update_corpus():
	data = json.loads(open('db/corpus-raw.json').read())
	corpus_file = open('db/corpus-processed.json', 'r+')
	corpus = {'corpus' : []} 

	matcher.corpus = corpus['corpus']

	for target_id in data:
		for post in data[target_id]:
			if 'history' not in post:
				continue

			title = post['history'][0]['subject']
			body = post['history'][0]['content']
			responses = []
			answered = False

			for response in post['children']:
				if response['type'] in ['i_answer', 's_answer']:
					answered = (response['type'] == 'i_answer' or len(response['tag_endorse']) > 0) or answered
				if 'subject' in response:
					responses.append({'body': matcher.clean(response['subject'])})
				elif 'history' in response:
					responses.append({'body': matcher.clean(response['history'][0]['content'])})

			corpus['corpus'].append({
				'id': post['nr'],
				'term': target_id,
				'title': matcher.clean(title),
				'folders': post['folders'], 
				'body': matcher.clean(body),
				'responses': responses,
				'answered': answered
			})

	corpus_file.seek(0) # erase the contents of the file
	corpus_file.truncate()
	json.dump(corpus, corpus_file, indent=4) # write new data to file

if __name__ == '__main__':
	update_corpus()