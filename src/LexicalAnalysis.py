from Engine import Engine
from Automatons.simulador_logica import AutomatoFinito

class LexicalAnalysis(Engine):

	def __init__(self, name):
		super(LexicalAnalysis, self).__init__(name)
		self.reservedWords = []
		self.readRW("../data/reserved_words.txt")
		self.automata = None
		self.buffer = []
		self.bufferWord = []

	def readRW(self, inputFile):
		with open(inputFile) as f:
			filelines = f.readlines()
			for line in filelines:
				words = line.split() 
				for word in words:
					self.reservedWords.append(word)
	
	def event1Handler(self, event):
		#print self.eventsList
		print self.buffer
		print event["content"]
		if event["content"]["value"] != " " and event["content"]["value"] != "\n":
			print self.buffer
			self.buffer.append(event["content"]["type"])
			self.bufferWord.append(event["content"]["value"])
			if self.automata == None:
				if event["content"]["type"] == "letter":
					self.automata = AutomatoFinito(False, name="identifier", nome_arquivo="../data/idAF.txt")
				else:
					if event["content"]["type"] == "numerical":
						self.automata = AutomatoFinito(False, name="numerical", nome_arquivo="../data/numAF.txt")
					else:
						self.automata = AutomatoFinito(False, name="symbol", nome_arquivo="../data/speAF.txt")
			#self.eventsList.pop(0)

		else:
			if len(self.buffer) != 0:
				self.insertNewEvent(0, 2, self.buffer)
		self.eventsList.pop(0)
		
		

	def event2Handler(self, event):
		self.buffer.append("#")
		print "Buffer"
		print self.buffer[0]
		self.automata.setInput(self.buffer)
		result = self.automata.rodar()
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
			new_content["type"] = "symbol"
		else:
			new_content["type"] = self.automata.name

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
		print event["content"]["type"]
		self.outputs.append(event["content"])
		self.eventsList.pop(0)
