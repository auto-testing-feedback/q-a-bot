import os, json
from flask import Flask, render_template, request
app = Flask(__name__)

bots_dir = 'db/bots/'

@app.route('/')
def home():
    bots = []
    for file in os.listdir(os.fsencode(bots_dir)):
        filename = os.fsdecode(file)
        if '.json' in filename and '-data' not in filename:
            bot_file = open(bots_dir + filename)
            bot = json.loads(bot_file.read())
            
            data_file = open(bot['link'].replace('.json', '') + '-data.json', 'r+') 
            data = json.loads(data_file.read())
            
            bot['data'] = data
            bots.append(bot)
    return render_template('index.html', bots=bots, data=data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST'])
def create():
    return

@app.route('/mark_as_answer', methods=['POST'])
def mark_as_answer():
    data = request.form.to_dict(flat=False)
    print(data)
    return {}

def tojson_pretty_filter(value):
    return json.dumps(value, sort_keys=False, indent=4, separators=(',', ': '))
app.jinja_env.filters['tojson_pretty'] = tojson_pretty_filter

# converts ['str1', 'str2', 'str3'] to 'str1 str2 str3'
def to_pretty_array_filter(value):
    print(' '.join(value))
    return ' '.join(value) # placeholder to get question filter buttons working
app.jinja_env.filters['to_pretty_array'] = to_pretty_array_filter

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/api', methods=['GET'])
def api_router():
    pass
