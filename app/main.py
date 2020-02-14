import os, json, argparse
import piazza_api
from bot import *

parser = argparse.ArgumentParser(description='q-a-bot')
parser.add_argument('--clean', action='store_true')
parser.add_argument('--update_only', action='store_true')
args = parser.parse_args()

bots_dir = 'db/bots/'

def main():
    for file in os.listdir(os.fsencode(bots_dir)):
        filename = os.fsdecode(file)
        if '.json' in filename and '-data' not in filename:
            bot = json.loads(open(bots_dir + filename).read())
            update(bot, erase=args.clean)

if __name__ == '__main__':
    main()
