import os, json
from .. import matcher
from flask import Flask, render_template, request
app = Flask(__name__)

bots_dir = 'db/bots/'
bot1_data = None

@app.route('/')
def home():
	bots = []
	i = 0
	for file in os.listdir(os.fsencode(bots_dir)):
		filename = os.fsdecode(file)
		if '.json' in filename and '-data' not in filename:
			bot_file = open(bots_dir + filename)
			bot = json.loads(bot_file.read())
			
			data_file = open(bots_dir + bot['link'].replace('.json', '') + '-data.json', 'r+') 
			data = json.loads(data_file.read())

			bot['data'] = data
			bots.append(bot)
	return render_template('index.html', bots=bots)

@app.route('/about', methods=['GET'])
def about():
	return render_template('about.html')

@app.route('/bot-raw/<bot_handle>', methods=['GET'])
def get_raw_bot_data(bot_handle):
	data_file = open('db/bots/' + bot_handle + '.json', 'r') 
	data = json.loads(data_file.read())
	return data

@app.route('/matcher-demo', methods=['GET'])
def matcher_demo():
	return render_template('matcher-demo.html')

@app.route('/matcher-demo/query', methods=['GET'])
def matcher_demo_query():
	bot1_data = json.loads(open('db/bots/bot-data.json', 'r+').read())

	title1 = request.args.get('title1')
	title2 = request.args.get('title2')
	content1 = request.args.get('content1')
	content2 = request.args.get('content2')

	f_title = matcher.compute_fuzzy_similarity(title1, title2) 
	f_content = matcher.compute_fuzzy_similarity(content1, content2) 
	s1 = f_title * matcher.title_impact + f_content * (1 - matcher.title_impact)
	
	s2 = 0
	
	is_question = '?' in title1 or '?' in content1
	is_learning = is_question and (title1.split(' ').length > 7 or content1.split(' ').length > 7)
	if is_question:
		for q in bot1_data['questions']:
			if 'logistics' in q['folders'] or 'other' in q['folders']:
				print(q['title'])
				a = matcher.compute_fuzzy_similarity(q['title'], title1)
				b = matcher.compute_fuzzy_similarity(q['title'], title2)
				if a > 50 or b > 50:
					is_learning = False	

	return {
		'fuzzy_similarity': s1,
		'cosine_similarity': s2,
		'is_learning': is_learning
	}

def tojson_pretty_filter(value):
    return json.dumps(value, sort_keys=False, indent=4, separators=(',', ': '))
app.jinja_env.filters['tojson_pretty'] = tojson_pretty_filter

# converts ['str1', 'str2', 'str3'] to 'str1 str2 str3'
def to_pretty_array_filter(value):
    print(' '.join(value))
    return ' '.join(value) # placeholder to get question filter buttons working
app.jinja_env.filters['to_pretty_array'] = to_pretty_array_filter