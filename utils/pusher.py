"""This modules provides such git actions as init and push.
It also realize repository filling from prepared data. 

"""

import os
import shutil


REPOS_FULL_PATH = os.path.join(os.getcwd(), 'repos')
PREPARED_DATA_PATH = './fill_data/prepared_data'

# remote repositories assignments for local repos names
REMOTE_URLS = {
	'puzzles': 'https://github.com/mamsdeveloper/python_puzzles_practice',
	'web_exercises': 'https://github.com/mamsdeveloper/python_web_practise.git'
}


def _file_filter(file: str) -> int:
	"""Custom function for sorting files by them numbers

	Args:
		file (str): file path

	Returns:
		int: file number if it in path else -1

	"""

	name = os.path.splitext(file)[0]
	if name.isdigit():
		return int(name)
	else:
		return -1


def create_repo(repo: str) -> str:
	"""Create new directory {repo} in ./repos, initialize repository 
	and add remote if it setted in REMOTE_URLS

	Args:
		repo (str): local repository name
		remote_url (str): url of remote repository

	"""
	if not repo in REMOTE_URLS:
		raise KeyError(f'Remote url for {repo} does not exist in REMOTE_URLS')

	repo_path = (os.path.join(REPOS_FULL_PATH, repo))
	# create repository directory
	try:
		os.mkdir(repo_path)
	except FileExistsError:
		pass

	# init repository if does not exist
	if not os.path.exists(os.path.join(repo_path, '.git')):
		remote_url = REMOTE_URLS[repo]
		cmd_stream = os.popen(
			f'cd "{repo_path}" & git init & git remote add {repo} {remote_url}')
		output = cmd_stream.read()
		cmd_stream.close()
	else:
		output = 'Repository already exists'

	return output


def add_file(repo: str):
	"""Copy first non-consisted file to repository from prepared data

	Args:
		repo (str): local repository name

	Returns:
		str: file adding result 

	"""

	# target repository
	repo_path = (os.path.join(REPOS_FULL_PATH, repo))
	files_in_target = set(os.listdir(repo_path))
	# folder with prepared files
	source_path = (os.path.join(PREPARED_DATA_PATH, repo))
	files_in_source = set(os.listdir(source_path))
	# find first file in prepared data that does not consist in repository
	different_files = files_in_source.difference(files_in_target)
	if different_files:
		file = sorted(different_files, key=_file_filter)[0]
		shutil.copy(os.path.join(source_path, file), repo_path)
		output = f'Successfully add {file} to {repo}'
	else:
		output = f'No files in {repo}'

	return output


def push(repo: str, commit: str = None) -> str:
	"""Push repository to master branch

	Args:
		repo (str): local repository name
		commit (str): commmit message, if not setted commit with last file name
	
	Returns:
		str: output of command

	"""

	repo_path = (os.path.join(REPOS_FULL_PATH, repo))
	if commit is None:
		files_in_target = set(os.listdir(repo_path))
		commit = sorted(files_in_target, key=_file_filter)[-1]
		commit += ' solved'

	cmd_stream = os.popen(
		f'cd {repo_path} & git fetch {repo} master & git add . & git commit -m "{commit}" & git push {repo} master')
	output = cmd_stream.read()
	cmd_stream.close()

	return output
