"""
Main module of filler.
Manage parsing, filling, repositories creating and pushing.

"""

import os
from http.client import HTTPSConnection
import sys
from time import sleep

from utils import parser, pusher

RAW_DATA_PATH = './fill_data/raw_data'
PREPARED_DATA_PATH = './fill_data/prepared_data'


def log(*values):
	"""log values and write them to log file"""

	print(*values)
	with open('log.log', 'a') as f:
		for v in values:
			f.write(str(v) + '\n')


def check_connection() -> bool:
	"""Check internet connection

	Returns:
		bool: state of internet convection

	"""

	conn = HTTPSConnection('8.8.8.8', timeout=10)
	try:
		conn.request('HEAD', '/')
		return True
	except Exception:
		return False
	finally:
		conn.close()


def simple_push(count: int = None):
	"""The easiest way to fill yor github everyday is 
	create bat or sh script that runing this function.

	Check if new raw files added, parse them, 
	create repositories for each prepared data if it needed,
	add file and push to remote repository.
	
	Args:
		count (int): count of pushing commits, by default without limitation

	"""

	# parse files from fill_data/raw_data
	# and put prepared data to fill_data/raw_data
	log('Parse raw data files')
	output = parser.parse_raw_files()
	log('Parsing output:\n', output)

	# for all successfully prepared data
	# create repo (if it does not exist),
	# copy first different file from prepared data to repo
	# commit and push it
	counter = 0
	for repo in os.listdir(PREPARED_DATA_PATH):
		if counter == count:
			log(f'Commits limit reached: {counter} commits pushed')
			break
		try:
			log(f'Process {repo}')
			output = pusher.create_repo(repo)
			log(f'Creating repository output:\n', output)
			output = pusher.add_file(repo)
			log(f'Adding file output:\n', output)
			output = pusher.push(repo)
			log(f'Pushing output:\n', output)
		except Exception as exc:
			log('Error:', exc)
		else:
			counter += 1


if __name__ == '__main__':
	# wait for probably wi-fi internet connection
	sleep(10)
	pushes_count = int(sys.argv[1]) if len(sys.argv) > 1 else None
	if check_connection():
		simple_push(pushes_count)
	else:
		log('Pushing denied. Bad internet connection')
