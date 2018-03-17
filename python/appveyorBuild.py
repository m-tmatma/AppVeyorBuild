#!/usr/bin/python

import sys

def get_bit_bucket_branch(username, reposname):
	import json
	import urllib

	branches = []
	url = 'https://api.bitbucket.org/2.0/repositories/' + username + '/' + reposname + '/refs/branches'
	data = urllib.urlopen(url).read()

	jsonData = json.loads(data)
	for v in jsonData['values']:
		branches.append(v['name'])

	return branches

def get_github_branch(username, reposname):
	import json
	import urllib

	branches = []
	url = 'https://api.github.com/repos/' + username + '/' + reposname + '/branches'
	data = urllib.urlopen(url).read()

	jsonData = json.loads(data)
	for v in jsonData:
		branches.append(v['name'])

	return branches

def build_branches(api_key):
	try:
		import appveyor_client
	except ImportError:
		print "please run 'pip install --user appveyor-client'"
		sys.exit(1)

	client = appveyor_client.AppveyorClient(api_key)
	projects = client.projects.get()
	for project in projects:
		repositoryName   = project['repositoryName']
		accountName      = project['accountName']
		repositoryType   = project['repositoryType']
		project_slug     = project['slug']
		[username, reposname] = repositoryName.split("/")
		if repositoryType == 'bitBucket':
			branches = get_bit_bucket_branch(username, reposname)
		elif repositoryType == 'gitHub':
			branches = get_github_branch(username, reposname)
		else:
			continue

		for branch in branches:
			print repositoryType, username, reposname, project_slug, branch
			client.builds.start(accountName, project_slug, branch, None )

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "usage: " + sys.argv[0] + " <api key>"
		print ""
		print "<api key> can be get from https://ci.appveyor.com/api-token"
		sys.exit(1)

	api_key = sys.argv[1]
	build_branches(api_key)
