import itertools,os,re

"""
	To test purpose we have set logger in the module.
	In production scenario log to a file instead of console
"""
#logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
#logger = logging.getLogger('core')
#consoleHandler = logging.StreamHandler()
#consoleHandler.setFormatter(logFormatter)
#logger.addHandler(consoleHandler)
#logger.setLevel(logging.DEBUG)

class word_tracker(object):
	"""
	Description: Class to track word count and other stats 
	"""
	
	def __init__(self, word):
		self.cache = {word: {
				'count': 1,
				'occurrence': [word]
			}} 
		self.count_to_word_dict = {1: [word]}
		self.min_count = 1
		self.max_count = 1
		
	def _update_count_to_word(self, word, current_count = 0, new_count = 1):
		if current_count > 0:
			self.count_to_word_dict[current_count].remove(word)
		word_count = self.count_to_word_dict.get(new_count)
		if word_count:
			word_count.append(word)
		else:
			self.count_to_word_dict.update({new_count: [word]})
		self.max_count = max(self.max_count, new_count)
		
	def update_tracker(self, word):
		word_cache = self.cache.get(word)
		if word_cache:
			self._update_count_to_word(word, word_cache['count'], 
								word_cache['count'] + 1)			
			word_cache['count'] = word_cache['count'] + 1
			word_cache['occurrence'].append(word)
		else:
			self.cache.update({word: {
				'count': 1,
				'occurrence': [word]
			}})
			self._update_count_to_word(word)			
	
	def get_word_count(self):
		return sorted(self.count_to_word_dict.keys, reverse=True)
		
class stats_reporter(object):
	"""
	Description: Class to report the top word count stats 
	"""
	
	def __init__(self, parser, no_of_top_words = 10, verbose = False):
		self.parse = parser
		self.no_of_top_words = no_of_top_words
		self.verbose = verbose
		
	def print_report(self):
		# Sort in descending order. Do not return empty word_trackers.
		word_trackers = [x for x in sorted(self.parse.cache.values(), 
							key=lambda x: 
							x.max_count if x else 0, 
							reverse=True) if x]
		if word_trackers:
			for word_count in [y for y in 
							itertools.islice([x for x in 
											range(word_trackers[0].max_count
											,0,-1)], 
											self.no_of_top_words)]:
				for word_tracker in word_trackers:
					word_with_count = word_tracker.count_to_word_dict.get(word_count)
					if word_with_count:
						print ("Count: %s Words: %s"%(word_count, 
													word_with_count))
			#print("Top %s word:"%(self.no_of_top_words))
			#for w_t in itertools.islice(word_trackers, self.no_of_top_words):
			#	if w_t.occurence:
			#		if self.verbose:
			#			print("Word: %s Count: %s : Occurrences: %s"
			#				%(w_t.occurence[0],w_t.count,w_t.occurence))
			#		else:
			#			print("Word: %s Count: %s"%(w_t.occurence[0],
			#														w_t.count))
			#	else:
			#		print("Word: %s Count: %s : Occurrences: %s"
			#				%("Unknown",w_t.count,w_t.occurence))					
		else:
			print("No words found...")
		print("Ignored words %s"%(str(self.parse.ingored_words)))
			
class parser(object):
	"""
	Description: Class to parse the blobs 
	"""
	def __init__(self, logger, custom_regex = None):
		#{'a': word_tracker() ... 'z': word_tracker()}
		self.cache = dict(pair for d in 
						[{y: None} for y in 
						[x for x in 
						map(chr,range(ord('a'),ord('z')+1))]]  
						for pair in d.items())
		self.ingored_words = []
		self.regex = custom_regex or "([\w][\w]*'?\w?)"
		self.logger = logger
		
	def get_cache(self):
		"""
		Description: Return word cache
		Returns: Returns word cache 
		"""
		return self.cache
		
	def _update_cache(self, word):
		"""
		Description: Update word cache with given word
		Returns: None
		"""
		
		if self._is_valid_word(word):
			w_t = self.cache.get(word[0].lower())
			if w_t:
				w_t.update_tracker(word)
			else:
				w_t = word_tracker(word)
				self.cache[word[0].lower()] = w_t
		else:
			self.ingored_words.append(word)
		
	def _is_valid_word(self, word):
		"""
		Description: Validates the word. Add any rule
			Rule 1: Word should not be empty
			Rule 2: Word should start with char a - char z (Upper/Lower)
			... Add any rule here
		Returns: True/False
		"""
		#Get words starting with a alpha character
		if not word:
			return False
		#Word starts with letter a-z. Lower case compare
		if ord(word[0].lower()) in range(ord('a'),ord('z')+1):
			return True
		else:
			return False
				
			
	def parse_blob(self, blob):
		"""
		Description: Parses the given blob data
		Raises: Exception: Blob empty
		Returns: Parsed tokenized words from the blob
		"""
		if not blob:
			raise Exception("Blob empty: %s"(blob))
		words = re.compile(self.regex).findall(blob)
		self.logger.debug("Word parsed by regex: %s"%str(words))
		#Words are case insensitive.
		for word in words:
			self._update_cache(word)
			
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

