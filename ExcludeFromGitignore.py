#!/usr/bin/env python3
import os, os.path
import subprocess
import json

def get_git_ignores(path):
	# Sublime Text does not support subprocess.run
	proc = subprocess.Popen(
		["git", "clean", "--dry-run", "-dX"],
		stdout=subprocess.PIPE,
		stderr=subprocess.DEVNULL,
		cwd=path)

	try:
		output, _ = proc.communicate(timeout=5)
	except TimeoutExpired:
		proc.kill()
		_, _ = proc.communicate()
		raise RuntimeError("Could not get git ignored files")

	if proc.returncode != 0: return None

	output = output.decode()
	res = []
	prefix = 'Would remove '
	for line in output.split('\n'):
		if not line.startswith(prefix): continue
		res.append(line[len(prefix):])
	return res

folder_excl = 'folder_exclude_patterns'
file_excl = 'file_exclude_patterns'
extra_folder_excl = 'extra_folder_exclude_patterns'
extra_file_excl = 'extra_file_exclude_patterns'

def process_project_data(project_data, base_path):
	new_folders = []

	for folder_data in project_data['folders']:
		abs_path = os.path.join(base_path, folder_data['path'])
		git_ignores = get_git_ignores(abs_path)
		if git_ignores is None:
			new_folders.append(folder_data)
			continue

		folder_excludes = set()
		file_excludes = set()
		for ignore in git_ignores:
			if ignore.endswith('/'):
				folder_excludes.add(ignore[:-1])
			else:
				file_excludes.add(ignore)

		if extra_folder_excl not in folder_data:
			folder_data[extra_folder_excl] = folder_data.get(folder_excl, [])
		if extra_file_excl not in folder_data:
			folder_data[extra_file_excl] = folder_data.get(file_excl, [])

		_ = folder_data.pop(folder_excl, None)
		_ = folder_data.pop(file_excl, None)

		folder_excludes.update(folder_data[extra_folder_excl])
		file_excludes.update(folder_data[extra_file_excl])

		folder_data[folder_excl] = sorted(folder_excludes)
		folder_data[file_excl] = sorted(file_excludes)

		new_folders.append(folder_data)

	project_data['folders'] = new_folders
	return project_data

def atomic_ish_write(target, callback):
	temp_file = target + '.tmp'
	with open(temp_file, 'w') as temp:
		callback(temp)
		temp.flush()
		os.fsync(temp.fileno())
	os.rename(temp_file, target)

def main():
	import argparse
	parser = argparse.ArgumentParser(description="Update Sublime Text exclusions from git ignored files")
	parser.add_argument('project_file', metavar='PROJECT', type=str, help='The project file to update')

	args = parser.parse_args()

	with open(args.project_file, 'r') as project_file:
		project_data = json.load(project_file)

	base_path = os.path.dirname(args.project_file)
	new_project_data = process_project_data(project_data, base_path)
	atomic_ish_write(args.project_file,
		lambda project_file: json.dump(new_project_data, project_file, indent='\t'))

if __name__ == '__main__':
	main()
else:
	import sublime
	import sublime_plugin

	class ExcludeFromGitignoreCommand(sublime_plugin.WindowCommand):
		def description(self):
			return "Exclude files from current project based on git ignored files"

		def is_enabled(self):
			project_file = self.window.project_file_name()
			return project_file is not None

		def is_visible(self):
			return self.is_enabled()

		def run(self):
			project_file = self.window.project_file_name()
			if project_file is None: return
			project_data = self.window.project_data()
			new_project_data = process_project_data(project_data, os.path.dirname(project_file))
			self.window.set_project_data(new_project_data)