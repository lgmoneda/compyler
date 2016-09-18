from Engine import Engine

class FiniteAutomata(Engine):

	def __init__(self, name, def_file):
		super(FiniteAutomata, self).__init__(name)
		self.name = name
		self.submachines = []
		self.description = {"initial": None, 
						    "transitions" : None , 
							"finals" : None}
		self.description["transitions"] = []
		self.description["finals"] = []

		self.activity = {"current state": None,
						 "pointer" : None,
						 "left": [],
						 "next": []}

		self.config_FA(def_file)

	def config_FA(self, filename):
		"""Reads the finite automata description from a file 

		Args:
			filename: string with directory and filename
		Returns:
			None 

		"""
		with open(filename) as f:
			filelines = f.readlines()

			if str(filelines[0].split()[0][0]) == "*":
				self.description["finals"].append(filelines[0].split()[0][1:])
				self.description["initial"] = filelines[0].split()[0][1:]
			else:
				self.description["initial"] = filelines[0].split()[0]
			for line in filelines[1:]:
				words = line.split() 
				transition = dict()
				transition["current"]= words[0]
				transition["input"] = words[1] 
				if words[2][0] == "*": 
					transition["next"] = words[2][1:]
					if words[2][1:] not in self.description["finals"]:
						self.description["finals"].append(words[2][1:])
				else:
					transition["next"] = words[2]
				self.description["transitions"].append(transition) 
		self.activity["current state"] = self.description["initial"]

		tipos_eventos_af = ["Partida inicial", "Leitura de simbolo", 
					    "Cabecote p/ direita", "Atingiu algum estado final", 
					    "Erro", "FIM de simulacao"]

    #leitura simbolo
	def event1Handler(self, event):
		self.eventsList.pop(0)
		transition_found = False
		for transition in self.description["transitions"]:
				if transition.get('current') == self.activity["current state"] and transition.get('input') == event["content"]:
					self.activity["current state"] = transition.get('next')
					transition_found = True

		if transition_found == False:
			self.insertNewEventFirstOrLast(type_=4, content=event["content"], last=False)

		if len(self.eventsList) == 0:
			self.insertNewEventFirstOrLast(content=event["content"], type_=5)	

	def event2Handler(self, event):
		result = self.run()
		self.eventsList.pop(0)
		#return result

	#Erro
	def event4Handler(self, event):
		self.eventsList.pop(0)
		print "Finite Automata Error"
		return False

	#Fim simulacao
	def event5Handler(self, event):
		self.eventsList.pop(0)
		if self.activity["current state"] in self.description["finals"]:
			return True
		return False