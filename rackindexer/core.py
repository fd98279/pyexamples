import itertools,os,re

class word_tracker(object):
	"""
	Description: Tracks word count for words starting with the same letter
		For letters with hot spots (some letters have more words than other 
		letters: for e.g a vs z we can further enhance this word tracker 
		logic for letters with hot spots. 
		Right now all words are tracked similar.
	"""
	
	def __init__(self, word):
		# Cache count and occurrence for each letter
		self.cache = {word: {
				'count': 1, # Count 
				'occurrence': [word] # List of letters with the same count
			}} 
		self.count_to_word_dict = {1: [word]}
		self.min_count = 1 # for words starting with this letter min count
		self.max_count = 1 # for words starting with this letter max count
		
	def _update_count_to_word(self, word, current_count = 0, new_count = 1):
		"""
		Description: Updates min and max count for each word  
		"""
		
		if current_count > 0:
			self.count_to_word_dict[current_count].remove(word)
		word_count = self.count_to_word_dict.get(new_count)
		if word_count:
			word_count.append(word)
		else:
			self.count_to_word_dict.update({new_count: [word]})
		self.max_count = max(self.max_count, new_count)
		
	def update_tracker(self, word):
		"""
		Description: Updates cache for the words starting with this letter  
		"""
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
		
class parser(object):
	"""
	Description: Class to parse the blobs 
	"""
	def __init__(self, logger, custom_regex = None, special_chars_to_remove = 
				[]):
		# {'a': word_tracker() ... 'z': word_tracker()}
		# Create a word_tracker class for each letter
		self.cache = dict(pair for d in 
						[{y: None} for y in 
						[x for x in 
						map(chr,range(ord('a'),ord('z')+1))]]  
						for pair in d.items())
		self.ingored_words = []
		# [\w]:  Match Word 
		# [\w]*: Match 1-More Word
		# '?:    Match 0 or 1 '
		# \w?:   Match 0 or 1 Word
		# Tested at: http://regexr.com/
		self.regex = custom_regex or "([\w][\w]*'?\w?)"
		self.logger = logger
		self.special_chars_to_remove = special_chars_to_remove
		
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
		
		#Handle any special characters
		for char in self.special_chars_to_remove:
			blob = blob.replace(char, " ")
		
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
		self.parse_files(self._get_filepaths(directory))

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
			with open(f, encoding="utf8") as f:
				[self.parse_blob(x.strip()) for x in f.readlines() if x.strip()]
		
	def _get_filepaths(self, directory):
		"""
		Description: Get all the files in the given directory
		"""
		file_paths = []
		for root, directories, files in os.walk(directory):
			for filename in files:
				filepath = os.path.join(root, filename)
				file_paths.append(filepath)
		self.logger.debug("Processing files in the directory: %s"%str(
			file_paths))				
		return file_paths

class stats_reporter(object):
	"""
	Description: Report words with top count 
	"""
	
	def __init__(self, parser, logger, no_of_top_words = 10):
		self.parse = parser
		self.no_of_top_words = no_of_top_words
		self.logger = logger
		
	def print_report(self):
		# Sort all word_trackers in a descending order of max count
		# There are 26 word_trackers for each letter a..z
		# Some word_trackers could be empty, i.e no words starting with 
		# that letter
		print("Top %s words..."%(self.no_of_top_words))		
		word_trackers = [x for x in sorted(self.parse.cache.values(), 
							key=lambda x: 
							x.max_count if x else 0, 
							reverse=True) if x]
		if word_trackers:
			# Get an iterator from the highest max_count of all word trackers
			# to 0 
			_no_of_top_words = self.no_of_top_words 
			for word_count in [x for x in range(word_trackers[0].max_count
											,0,-1)]:
				# Break the loop if we have printed required number of words
				if _no_of_top_words == 0:
					break;
				# Go through each word tracker and print the words 
				# matching the count
				for word_tracker in word_trackers:
					word_with_count = word_tracker.count_to_word_dict.get(
						word_count)
					if word_with_count:
						print ("%s - Count: %s Words: %s"%(_no_of_top_words,
														word_count, 
													word_with_count))
						_no_of_top_words = _no_of_top_words - 1
		else:
			print("No words found...")
					
		self.logger.debug("Ignored words %s"%(
			str(self.parse.ingored_words).encode('ascii','ignore')))
