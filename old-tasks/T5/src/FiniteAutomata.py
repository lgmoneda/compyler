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


		### To build the language syntax recognizer T5
		self.stack = []
		self.state = 0
		self.state_counter = 1
		#self.outfile = outfile
		self.createdAutomata = []
		self.stack.append((self.state, self.state_counter))

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
		print "Event: ",
		print event
		#print self.description
		#print self.activity
		
		#print(self.eventsList)
		#raw_input()
		#print(event["content"][self.key])
		### Void transitions:

		#print self.activity["current state"]
		#print 
		for transition in self.description["transitions"]:
				if transition.get('current') == self.activity["current state"]: 
					if transition.get('input') == event["content"][self.key] and transition_found == False:
						self.activity["current state"] = transition.get('next')
						print("Consumindo simbolo!")
						transition_found = True
						#self.eventsList.pop(0)

						### To build the language syntax recognizer T5
						
						#print(self.createdAutomata)
						
						self.state_counter += 1
						print(self.stack)
						#raw_input()

						if self.name == "grammar":
							print(self.createdAutomata)
							#raw_input()
							if event["content"][self.key] == "NT":
								self.scopes = []
								self.state_counter = 0
								#self.outfile = outfile
								self.createdAutomata = []

								self.state_counter += 1
								self.createdAutomata.append(event["content"]["value"])
								#self.createdAutomata.append("0")
								self.createdAutomata.append(str(self.state))
							if event["content"][self.key] == "=":
								self.stack.append((self.state, self.state_counter - 1))
								#pass
							if event["content"][self.key] == ".":
								self.createdAutomata.append(str(self.state) + " vazio *1")
								#self.createdAutomata.append("@")

								seen = []
								for item in self.createdAutomata:
									if item not in seen:
										seen.append(item)

								self.createdAutomata = seen
								
								### Treating void transitions
								there_are_voids = True
								#while(there_are_voids):
									#there_are_voids = False

								### Absorvendo estado final
								
								repeat = 1
								while(repeat > 0):
									for item in self.createdAutomata[2:]:
										if item.split(" ")[1] == "vazio":
											there_are_voids = True
											split = item.split(" ")
											from_ = split[0]
											get_to_from = split[-1]
											if get_to_from[0] == "*":
												for i in range(2, len(self.createdAutomata)):
												 	if self.createdAutomata[i].split(" ")[-1] == from_:
														self.createdAutomata[i] =  self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " *" + from_
														print(self.createdAutomata[i])
														repeat += 1
														#raw_input()
									repeat -= 1

								### Absorvendo transicoes
								"""
								repeat = 1
								while(repeat > 0):
									exclude = []
									for item in reversed(self.createdAutomata[2:]):
										if item.split(" ")[1] == "vazio":
											there_are_voids = True
											split = item.split(" ")
											from_ = split[0]
											get_to_from = split[-1]
											print("Item que gerou substituicao: ")
											print(item)
											for i in range(2, len(self.createdAutomata)):
												if self.createdAutomata[i].split(" ")[0] == get_to_from[-1]:
													self.createdAutomata.append(from_ + " " + self.createdAutomata[i].split(" ")[1] + " " + self.createdAutomata[i].split(" ")[-1])
													#self.createdAutomata[i] = from_ + " " + self.createdAutomata[i].split(" ")[1] + " " + self.createdAutomata[i].split(" ")[-1]
													#print("substituindo: ")
													#print(from_)
													#print("A substituicao: ")
													print(self.createdAutomata[i])
													#exclude.append(i)
													#repeat +=1
									#for ex in exclude:
									#	self.createdAutomata.pop(ex)
									repeat -= 1

								"""

								
								### Acima funcionando
								"""
								for item in self.createdAutomata[2:]:
									if item.split(" ")[1] == "vazio":
										there_are_voids = True
										split = item.split(" ")
										from_ = split[0]
										get_to_from = split[-1]
										print("Item que gerou substituicao: ")
										print(item)
										for i in range(2, len(self.createdAutomata)):
											if self.createdAutomata[i].split(" ")[0] == get_to_from[-1]:
												self.createdAutomata[i] = from_ + " " + self.createdAutomata[i].split(" ")[1] + " " + self.createdAutomata[i].split(" ")[-1]
												print("substituindo: ")
												print(from_)
												print("A substituicao: ")
												print(self.createdAutomata[i])
												raw_input()
											if self.createdAutomata[i].split(" ")[-1] == get_to_from[-1]:
												self.createdAutomata[i] = self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " " + from_
												print("substituindo: ")
												print(from_)
												print("A substituicao: ")
												print(self.createdAutomata[i])
												raw_input()
											if get_to_from[0] == "*" and self.createdAutomata[i].split(" ")[-1] == from_:
												self.createdAutomata[i] =  self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " *" + from_
											#	print("substituindo: ")
											#	print(from_)
											#	print("A substituicao: ")
											#	print(self.createdAutomata[i])
												raw_input()
								"""
								"""												
								for item in self.createdAutomata[2:]:
									if item.split(" ")[1] == "vazio":
										split = item.split(" ")
										from_ = split[0]
										get_to_from = split[-1]
										print("Item que gerou substituicao: ")
										print(item)
										for i in range(2, len(self.createdAutomata)):
											if self.createdAutomata[i].split(" ")[0] == from_:
												self.createdAutomata[i] = get_to_from[-1] + " " + self.createdAutomata[i].split(" ")[1] + " " + self.createdAutomata[i].split(" ")[-1]
												print("substituindo: ")
												print(from_)
												print("A substituicao: ")
												print(self.createdAutomata[i])
												#raw_input()
											if self.createdAutomata[i].split(" ")[-1] == from_:
												self.createdAutomata[i] =  self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " " + get_to_from
												print("substituindo: ")
												print(from_)
												print("A substituicao: ")
												print(self.createdAutomata[i])
												#raw_input()

								
								for item in self.createdAutomata[2:]:
									if item.find("vazio"):
										split = item.split(" ")
										from_ = split[0]
										get_to_from = split[-1]
										if get_to_from[0] == "*":
											for i in range(2, len(self.createdAutomata)):
												if  self.createdAutomata[i].split(" ")[-1] == from_:
													#self.createdAutomata[i] =  self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " *" + from_
													self.createdAutomata.append(self.createdAutomata[i].split(" ")[0] + " " + self.createdAutomata[i].split(" ")[1] + " *" + from_)
										else:
											for item2 in self.createdAutomata[2:]:
												#print item2
												if item2.split(" ")[0] == get_to_from:
													self.createdAutomata.append(from_ + " " + item2.split(" ")[1] + " " + item2.split(" ")[2])
								"""
								

								"""
								### Deleting all void transitions
								new_createdAutomata = []
								
								to_pop = []
								for i in range(len(self.createdAutomata)):
									if self.createdAutomata[i].find("vazio") < 0:
										to_pop.append(i)
								
								new_createdAutomata = []
								for i in range(len(self.createdAutomata)):
									if i in to_pop:
										new_createdAutomata.append(self.createdAutomata[i])		
								self.createdAutomata = list(new_createdAutomata)
								#self.createdAutomata.pop(to_pop)
								"""
								
								#new_createdAutomata.append("@")
								self.createdAutomata.append("@")
								text_file = open("../data/APs/" + self.createdAutomata[0] + ".txt", "w")
								#for line in new_createdAutomata:
								for line in self.createdAutomata:
									text_file.write(line)
									text_file.write("\n")
								text_file.close()

								self.state = 0
								self.state_counter = 1
								self.stack = []

						elif self.name == "exp":
							print(self.createdAutomata)
							#print(self.eventsList)
							#raw_input()
							if event["content"][self.key] == "NT":
								self.createdAutomata.append(str(self.state) + 
															" " + 
															str(event["content"]["value"])
															+ " " + str(self.state_counter - 1))
								self.state = self.state_counter - 1
							if event["content"][self.key] == "TERM":

								#self.state = self.state_counter - 1
								without_quotes = str(event["content"]["value"][3:-3]) 
								self.createdAutomata.append(str(self.state) + 
															" " + 
															without_quotes
															+ " " + str(self.state_counter - 1))
								
								self.state = self.state_counter - 1
							if event["content"][self.key] == "(":
								self.stack.append((self.state, self.state_counter - 1))
								#self.state = self.state_counter
							if event["content"][self.key] == ")":

								print "Situacao: "
								print event["content"][self.key]
								print event["content"]["value"]
								print self.state_counter
								print self.state

								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)
								self.state = self.stack[-1][1]
								self.stack.pop(-1) 
								self.state_counter -= 1

								print "Situacao: "
								print event["content"][self.key]
								print event["content"]["value"]
								print self.state_counter
								print self.state
								#raw_input()
							if event["content"][self.key] == "{":
								self.stack.append((self.state_counter - 1, self.state_counter - 1))

								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)

								self.state = self.state_counter - 1
							if event["content"][self.key] == "}":
								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								### aas
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)
								self.state = self.stack[-1][1]
								#self.state = next_state
								#self.state = 3333
								self.stack.pop(-1) 

								### 
								#self.state_counter -= 1
							if event["content"][self.key] == "[":
								self.stack.append((self.state, self.state_counter - 1))
								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)
							if event["content"][self.key] == "]":
								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)
								self.state = self.stack[-1][1]
								self.stack.pop(-1) 
								self.state_counter -= 1
							if event["content"][self.key] == "|":
								if self.stack[-1][1] == 1:
									next_state = "*1"
								else:
									next_state = str(self.stack[-1][1])
								self.createdAutomata.append(str(self.state) + 
															" vazio " + 
															next_state)
								self.state = self.stack[-1][0]
								self.state_counter -= 1

						if self.name == "grammar" or self.name == "exp":
							print "Situacao: "
							print event["content"][self.key]
							print event["content"]["value"]
							print self.state_counter
							print self.state
							#raw_input()

					else:
						pass
						"""
						#Call submachine
						for submachine in self.submachines:
							if transition.get('input') == submachine.name and transition_found == False:
								
								self.insertNewEventFirstOrLast(
									type_=3, content=event["content"], last=False)
								self.insertNewEventFirstOrLast(
									type_=3, content=transition.get('input'), last=False)

								self.activity["current state"] = transition.get('next')
								transition_found = True
								#self.eventsList.pop(0)
						### T5
						if transition.get("input") == "vazio" and transition_found == False:
							print("ENTREI AQUI VAZIO")
							self.activity["current state"] = transition.get('next')
							transition_found = True
							self.insertNewEventFirstOrLast(type_=1, content=event["content"], last=False)
						"""
		
		if transition_found == False:		
			for transition in self.description["transitions"]:
					if transition.get('current') == self.activity["current state"] and transition_found == False: 
						#Call submachine
						for submachine in self.submachines:
							if transition.get('input') == submachine.name:
								
								self.insertNewEventFirstOrLast(
									type_=3, content=event["content"], last=False)
								self.insertNewEventFirstOrLast(
									type_=3, content=transition.get('input'), last=False)

								self.activity["current state"] = transition.get('next')
								transition_found = True
								#self.eventsList.pop(0)
						### T5
						if transition.get("input") == "vazio" and transition_found == False:
							print("ENTREI AQUI VAZIO")
							self.activity["current state"] = transition.get('next')
							transition_found = True
							self.insertNewEventFirstOrLast(type_=1, content=event["content"], last=False)


		if transition_found == False:
			self.insertNewEventFirstOrLast(type_=1, content=event["content"], last=False)
			self.insertNewEventFirstOrLast(type_=4, content=event["content"], last=False)

		if len(self.eventsList) == 0:	
			transition_found = False
			print(self.activity)
			for transition in self.description["transitions"]:
				if transition.get('current') == self.activity["current state"]:
					if transition.get("input") == "vazio" and transition_found == False:
						self.activity["current state"] = transition.get('next')
						transition_found = True

			print(self.activity)
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
			#nextInput.append(event_)
		nextMachine.setup(nextInput, self.granularity, self.verboseOptions)
		nextMachine.activity["current state"] = nextMachine.description["initial"] 
		#nextMachine.setEventsList(self.eventsList)

		### T5

		nextMachine.stack = self.stack
		nextMachine.state = self.state
		nextMachine.state_counter = self.state_counter

		result = nextMachine.run() 

		###
		self.state = nextMachine.state
		self.state_counter = nextMachine.state_counter
		self.stack = nextMachine.stack

		self.createdAutomata += nextMachine.createdAutomata

		#print "Result ",
		#print result
		print "Returning to the " + self.name + " machine."
		if result: 
			self.setEventsList(nextMachine.getOutput())
			#print self.eventsList
		else:
			self.eventsList = []
			return False


	#Sem transicao, limpo os eventos e termino
	def event4Handler(self, event):
		#print "estado corrente: ",
		#print self.activity["current state"]
		self.eventsList.pop(0)
		#print "No transition found."
		self.outputs = copy.deepcopy(self.eventsList)
		self.eventsList = []
		self.insertNewEventFirstOrLast(content=event["content"], type_=5)

	#Fim simulacao
	def event5Handler(self, event):
		self.eventsList.pop(0)
		if self.activity["current state"] in self.description["finals"]:
			return True
		return False