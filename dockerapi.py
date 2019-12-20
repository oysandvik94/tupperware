import docker
from collections import defaultdict

class DockerAPI:

	def __init__(self):
		self.client = docker.from_env()
		self.imageDict = defaultdict(list)

		for image in self.client.images.list():
			repoName = image.attrs["RepoDigests"][0].split("@sha")[0]
			tag = image.attrs["RepoTags"][0].strip(repoName + ':')
			self.imageDict[repoName].append((tag, image.id))

	def runImage(self, id):
		container = self.client.containers.run(id, detach=True)
		exit("Started container with id: " + container.short_id)