from Engine import Engine
import copy

class FiniteAutomata(Engine):
	"""Finite Automata model

	Attributes:
		name: string identifier
		submachines: a list of other automatas
		description: a dict with information about initial state, possible
					 transitions and final states.
		activity: a dict with running information
	Args:
		name: string to identify the automata
		def_file: string with the filename that descripts the automata


	"""

	def __init__(self, name, def_file, key):
		super(FiniteAutomata, self).__init__(name)
		self.key = key
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

	def setSubmachines(self, submachines):
		self.submachines = submachines

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
		print "Evento: "
		print event["content"]

		#print self.activity["current state"]
		#print 
		for transition in self.description["transitions"]:
				if transition.get('current') == self.activity["current state"]: 
					if transition.get('input') == event["content"][self.key]:
						self.activity["current state"] = transition.get('next')
						transition_found = True
						#self.eventsList.pop(0)
					else:
						#Call submachine
						for submachine in self.submachines:
							if transition.get('input') == submachine.name:
								self.insertNewEventFirstOrLast(
									type_=3, content=transition.get('input'), last=False)
								self.activity["current state"] = transition.get('next')
								transition_found = True
								#self.eventsList.pop(0)


		if transition_found == False:
			self.insertNewEventFirstOrLast(type_=1, content=event["content"], last=False)
			self.insertNewEventFirstOrLast(type_=4, content=event["content"], last=False)

		if len(self.eventsList) == 0:
			self.insertNewEventFirstOrLast(content=event["content"], type_=5)	

	#Chamada de submaquina
	def event3Handler(self, event):
		self.eventsList.pop(0)
		nextInput = []
		for submachine in self.submachines:
			if submachine.name == event["content"]: 
				nextMachine = copy.deepcopy(submachine)
		for event_ in self.eventsList:
			nextInput.append(event_["content"])
		nextMachine.setup(nextInput, self.granularity, self.verboseOptions)
		nextMachine.activity["current state"] = nextMachine.description["initial"] 
		#nextMachine.setEventsList(self.eventsList)
		result = nextMachine.run() 
		print "Result ",
		print result
		if result: 
			self.setEventsList(nextMachine.getOutput())
			#print self.eventsList
		else:
			self.eventsList = []
			return False


	#Sem transicao, limpo os eventos e termino
	def event4Handler(self, event):
		print "estado corrente: ",
		print self.activity["current state"]
		self.eventsList.pop(0)
		print "No transition found"
		self.outputs = copy.deepcopy(self.eventsList)
		self.eventsList = []
		self.insertNewEventFirstOrLast(content=event["content"], type_=5)

	#Fim simulacao
	def event5Handler(self, event):
		self.eventsList.pop(0)
		if self.activity["current state"] in self.description["finals"]:
			return True
		return False