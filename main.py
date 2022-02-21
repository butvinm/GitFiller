"""
Main module of filler.
Manage parsing, filling, repositories creating and pushing.

"""

import os

from utils import parser
from utils import pusher


RAW_DATA_PATH = './fill_data/raw_data'
PREPARED_DATA_PATH = './fill_data/prepared_data'


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
	print('Parse raw data files')
	output = parser.parse_raw_files()
	print('Parsing output:\n', output)

	# for all successfully prepared data
	# create repo (if it does not exist),
	# copy first different file from prepared data to repo
	# commit and push it
	counter = 0
	for repo in os.listdir(PREPARED_DATA_PATH):
		if counter == count:
			print(f'Commits limit reached: {counter} commits pushed')
			break
		try:
			print(f'Process {repo}')
			output = pusher.create_repo(repo)
			print(f'Creating repository output:\n', output)
			output = pusher.add_file(repo)
			print(f'Adding file output:\n', output)
			output = pusher.push(repo)
			print(f'Pushing output:\n', output)
		except Exception as exc:
			print('Error:', exc)
		else:
			counter += 1


if __name__ == '__main__':
	simple_push()
