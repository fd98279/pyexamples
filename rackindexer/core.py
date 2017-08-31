import os,re

class parser(object):
	def parse_blob(self, blob):
		"""
		Description: Parses the given blob data
		Raises: Exception: Blob empty
		Returns: Parsed tokenized words from the blob
		"""
		if not blob:
			raise Exception("Blob empty: %s"(blob))
		print(re.compile("([\w][\w]*'?\w?)").findall(blob))

	def parse_dir(self, directory):
		"""
		Description: Parses all blob data in the files in 
			given directory
		Raises: Exception: Directory not found
		Returns: Parsed tokenized words from blobs from all 
			the files in the given directory
		"""
		if not (directory or os.path.exists(directory)):
			raise Exception("Directory not found: %s"(directory))
		print(directory)
		self.parse_files(self.get_filepaths(directory))

	def parse_files(self, files):
		"""
		Description: Parses all blob data in the given files
		Raises: Exception: Files not found
		Returns: Parsed tokenized words from blobs from all 
			the given files
		"""
		if not (files or all([os.path.exists(f) for f in files])):
			raise Exception("Files not found: %s"(str(files)))
		for f in files:
			with open(f) as f:
				[self.parse_blob(x.strip()) for x in f.readlines()]
		
	def _get_filepaths(self, directory):
		"""
		Description: Get all the files in the given directory
		"""
		file_paths = []
		for root, directories, files in os.walk(directory):
			for filename in files:
				filepath = os.path.join(root, filename)
				file_paths.append(filepath)
		return file_paths

