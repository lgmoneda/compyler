from Engine import Engine
from Automatons.simulador_logica import AutomatoFinito
from FiniteAutomata import FiniteAutomata
from PushdownAutomata import PushdownAutomata

class SyntacticEngine(Engine):

	def __init__(self, name):
		super(SyntacticEngine, self).__init__(name)
		self.automata = PushdownAutomata("Pushdown Automata for Wirth Grammar", "../data/wirth_grammarAP.txt", "category") 
		self.buffer = []
		self.bufferWord = []

	
	def event1Handler(self, event):
		"""Buffer a token and Create a FA to recognize it 
		"""
		for event_ in self.eventsList:
			self.buffer.append(event_["content"])
		self.automata.setup(self.buffer, self.granularity, self.verboseOptions)
		#print self.granularity
		#print self.verboseOptions
		result = (self.automata.run(), self.buffer)
		self.setOutput(self.automata.getOutput())
		#self.outputs.append(self.buffer)
		self.eventsList = []
		if result[0]:
			print "The given grammar is in Wirth notation."
		else:
			print "The given grammar is NOT in Wirth notation."
		return result[0]
		

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

		return result
