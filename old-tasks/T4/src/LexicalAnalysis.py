from Engine import Engine
from Automatons.simulador_logica import AutomatoFinito
from FiniteAutomata import FiniteAutomata

class LexicalAnalysis(Engine):

	def __init__(self, name):
		super(LexicalAnalysis, self).__init__(name)
		self.reservedWords = []
		self.readRW("../data/reserved_words.txt")
		self.automata = None
		self.buffer = []
		self.bufferWord = []

	def readRW(self, inputFile):
		"""Reads a list of reserved words from a file for a given language"""
		with open(inputFile) as f:
			filelines = f.readlines()
			for line in filelines:
				words = line.split()
				for word in words:
					self.reservedWords.append(word)
	
	def event1Handler(self, event):
		"""Buffer a token and Create a FA to recognize it 
		"""
		if event["content"]["value"] != " " and event["content"]["value"] != "\n":
			#self.buffer.append(event["content"]["type"])
			self.buffer.append(event["content"])
			self.bufferWord.append(event["content"]["value"])
			if self.automata == None:
				if event["content"]["type"] == "letter":
					#self.automata = AutomatoFinito(False, name="identifier", nome_arquivo="../data/idAF.txt")
					self.automata = FiniteAutomata(name="NT", def_file="../data/idAF.txt", key="type")
				else:
					if event["content"]["type"] == "special" and event["content"]["value"] == "\xe2":
						#self.automata = AutomatoFinito(False, name="numerical", nome_arquivo="../data/numAF.txt")
						self.automata = FiniteAutomata(name="TERM", def_file="../data/quoted_symbolAF.txt", key="type")
					else:
						#self.automata = AutomatoFinito(False, name="symbol", nome_arquivo="../data/speAF.txt")
						self.automata = FiniteAutomata(name=event["content"]["value"], def_file="../data/speAF.txt", key="type")
		else:
			if len(self.buffer) != 0:
				self.insertNewEvent(0, 2, self.buffer)
		self.eventsList.pop(0)
		
		

	def event2Handler(self, event):
		"""Runs the automata and get its result

		"""
		#self.buffer.append("#")
		print self.buffer
		#self.automata.setInput(self.buffer)
		self.automata.setup(self.buffer, "word", self.verboseOptions)
		#result = self.automata.rodar()

		result = (self.automata.run(), self.buffer)
		#if result:
		#	result = self.automata.name

		print result

		last_id = self.eventsList[0]["id"] - 1
		self.insertNewEvent(last_id, 3, result)

		self.eventsList.pop(0)

	def event3Handler(self, event):
		word = []
		new_content = dict()
		for i in range(len(event["content"][1])):
			word.append(self.bufferWord[i])
		new_content["value"] = "".join(word) 
		if new_content["value"] in self.reservedWords:
			new_content["category"] = "symbol"
		else:
			new_content["category"] = self.automata.name

		self.bufferWord = []
		self.buffer = []
		self.automata = None

		last_id = self.eventsList[0]["id"] - 1
		self.insertNewEvent(last_id, 5, new_content)
		self.eventsList.pop(0)


	def event5Handler(self, event):
		print "Atom: "
		print "Value: ",
		print event["content"]["value"]
		print "Category: ",
		print event["content"]["category"]
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
		return True
