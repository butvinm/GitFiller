"""This module parse raw data from fill_data/raw_data by special regex patterns.
It also format document with autopep8.
Created files are stored in fill_data/prepared_data

"""


import os
import re

import autopep8

RAW_DATA_PATH = './fill_data/raw_data'
PREPARED_DATA_PATH = './fill_data/prepared_data'

# for removing from patterns
ARGS_PATTERN = r'~.+?(?=~|$)'
# for comment pattern matches
COMMENTED = r'~commented'


"""Fill data creating from raw data by gradually matching it's pattern and concatenate them.

Example:
	If we have such FILES_TO_PATTERN:
		{file_name: [r'PATTERN_0' + COMMENTED, r'PATTERN_1']}

	Text from raw file 'file_name' will be reformat to many files:
	fill_data\\prepared_data\\file_name:
		'0.py':
			'
				'''PATTERN_0_MATCH'''
				PATTERN_1_MATCH
			' 
		'1.py':
			'
				'''PATTERN_0_MATCH'''
				PATTERN_1_MATCH
			'
		...

"""

FILES_TO_PATTERNS = {
	'100_exercises.txt': [
		r'(Question).+((\n|.)+?)(?=Hint|Solution)' + COMMENTED, 
		r'(?<=Solution)((\n|.)+?)(?=#-)'
	],
	'puzzles.txt': [
		r'(?<=-#\n)\d+\.((.|\n)+?)(?=Solution)' + COMMENTED,
		r'(?<=^Solution)((.|\n)+?)(?=#-)'
	],
	'sqlite_exercises.txt': [
		r'(?<=-#\n)\d+\.((.|\n)+?)(?=Solution)' + COMMENTED,
		r'(?<=^Solution)((.|\n)+?)(?=#-)'
	],
	'web_exercises.txt': [
		r'(?<=-#\n)\d+\.((.|\n)+?)(?=Solution)' + COMMENTED,
		r'(?<=^Solution)((.|\n)+?)(?=#-)'
	]
}


def parse_file(file_name: str) -> list[str]:
	"""Parse given file with special rules (read at the begining of module)
	and split on many prepared content
	 
	Args:
		file_name (str): name of file with raw data in fill_data/raw_data directory 

	Returns:
		list[str]: splitted and transformed file content

	"""
	
	prepared_contents = []
	# FileNotFoundError will be hooked in files_parse loop
	with open(os.path.join(RAW_DATA_PATH, file_name), 'r') as f:
		raw_text = f.read()
	
	# KeyError will be hooked in files_parse loop
	patterns = FILES_TO_PATTERNS[file_name]
	
	matches = []
	args = []
	for pattern in patterns:
		clear_pattern = re.sub(ARGS_PATTERN, '', pattern, re.MULTILINE)
		matches += [re.finditer(clear_pattern, raw_text, re.MULTILINE)]
		args += [re.findall(ARGS_PATTERN, pattern)]

	matches_blocks = zip(*matches)
	for block in matches_blocks:
		content = ''
		for match, match_args in zip(block, args):
			for m in match.group():
				content += m	
			if COMMENTED in match_args:
				content = f'"""\n{content}"""\n\n\n'

		content = autopep8.fix_code(content)
		prepared_contents += [content]

	return prepared_contents



def parse_raw_files() -> str:
	"""Parse all files in ./file_data/raw_data
	and create prepared data in ./file_data/prepared_data

	Returns:
		str: info about parsing

	"""

	output = ''
	raw_files = os.listdir(RAW_DATA_PATH)
	for file in raw_files:
		content_folder = os.path.splitext(file)[0] 
		content_folder_path = os.path.join(PREPARED_DATA_PATH, content_folder)
		if os.path.exists(content_folder_path):
			output += f'Directory {content_folder} already exist. Delete it if you want parse it again\n'
			continue

		try:
			prepared_contents = parse_file(file)
		except KeyError:
			output += f'Not pattern for {file}. Please add it\n'
			continue
		except FileNotFoundError:
			output += f'Can not find {file} in raw data\n'
			continue

		os.mkdir(content_folder_path)
		for i in range(len(prepared_contents)):
			file_name = f'{i}.py'
			path = os.path.join(
				PREPARED_DATA_PATH, 
				content_folder, 
				file_name
			)
			with open(path, 'w') as f:
				f.write(prepared_contents[i])
		
		output += 'Successfully prepared: {content_folder}\n'
		
	return output

# if __name__ == '__main__':
# 	parse_raw_files()
