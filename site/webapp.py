import os, json
from flask import Flask, render_template 
app = Flask(__name__)

@app.route('/')
def home():
    bots = []
    for file in os.listdir(os.fsencode('bots')):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            bots.append(json.loads(open('bots/' + filename, 'r').read()))
    return render_template('index.html', bots=bots)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create', methods=['POST'])
def create():
    return

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

