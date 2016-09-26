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
	#Transforma tudo em evento 2 at
	def event1Handler(self, event):



	#Reconhece o tipo de elemento que chegou
	def event2Handler(self, event):

		#Terminal

		#Nao-Terminal

		#Final de regra

		#Agrupamento

		#Agrupamento entre chaves
		pass