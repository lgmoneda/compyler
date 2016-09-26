from Engine import Engine

class WirthToPushdown(Engine):

	def __init__(self, name):
		super(WirthToPushdown, self).__init__(name)
		self.state_count = 0
		self.current_state = 0
		self.next_state = 0
		
		#self.automata = PushdownAutomata("Pushdown Automata for Wirth Grammar", "../data/wirth_grammarAP.txt", "category") 
		#self.buffer = []
		#self.bufferWord = []
	
	#Comeco de regra 
	#Consome o que sera definido e o =
	def event1Handler(self, event):




	def event2Handler(self, event):