import os, time, json, argparse
import piazza_api

parser = argparse.ArgumentParser(description='q-a-bot')
args = parser.parse_args()

def pull_data():
	config = json.loads(open('config.json').read())
	piazza = piazza_api.Piazza()
	piazza.user_login(config['login']['email'], config['login']['password'])

	data_file = open('db/corpus-raw.json', 'r+')
	data = json.loads(data_file.read())
	
	for target in config['targets']:
		piazza_term = piazza.network(target)
		piazza_term_stats = piazza_term.get_statistics()

		data[target] = [] 

		total = piazza_term_stats['total']['questions']
		i = 1
		while i <= total:
			success = False
			while True:
				piazza_post = None
				try:
					piazza_post = piazza_term.get_post(i)
				except piazza_api.exceptions.RequestError as exception:
					if 'could not get post' in str(exception).lower():
						i += 1
						continue
					else:
						print('too fast, waiting...')
						time.sleep(60)
				print('got post {}/{} from {} ({}/{})'.format(i, total, target, config['targets'].index(target) + 1, len(config['targets'])))
				time.sleep(1)
				data[target].append(piazza_post)
				break
			i += 1
			data_file.seek(0) # erase the contents of the file
			data_file.truncate()
			json.dump(data, data_file, indent=4) # write new data to file

if __name__ == '__main__':
	pull_data()