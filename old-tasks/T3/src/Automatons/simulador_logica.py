class Simulador(object):
	"""docstring for Simulador"""
	def __init__(self, route=True):
		super(Simulador, self).__init__()
		self.route = route
		
	def showOptionsWait(self):
		print "Escolha entre as opcoes: "
		print "(a) Escolher Dispositivo",
		if self.route: 
			print "(b) Desligar rastro ", 
		else: 
			print "(b) Ligar rastro ", 
		print "(c) Terminar simulacao"
		user_input = raw_input()
		return self.treatEvent(user_input)
	
	def treatEvent(self, event):
		if event == "a":
			self.chooseDev()
		if event == "b":
			if self.route:
				self.route = False
			else:
				self.route = True
		if event == "c":
			print "Terminando as simulacoes, volte sempre!"
			return True
		if event == "d":
			self.startAFSim()
		if event == "e":
			self.startAPSim()
		if event == "f":
			self.startMTSim()
		return False

	def chooseDev(self):
		print "Escolha entre as opcoes: "
		print "(d) Automato Finito (e) Automato de Pilha Estruturado (f) Maquina de Turing ",
		user_input = raw_input()
		self.treatEvent(user_input)

		user_input = raw_input()

	def defDispositivo(self):
		filename = raw_input("Digite o nome do arquivo: ")
		file_object = open(filename, "r")
		print file_object

	def startAFSim(self):
		AF = AutomatoFinito(self.route)
		AF.askForInput()
		AF.rodar()

	def startAPSim(self):
		AP = AutomatoPilha(self.route)
		AP.askForInput()
		AP.rodar()

	def startMTSim(self):
		MT = MaquinaTuring(self.route)
		MT.askForInput()
		MT.rodar()


class AutomatoFinito():

	tipos_eventos_af = ["Partida inicial", "Leitura de simbolo", 
					    "Cabecote p/ direita", "Atingiu algum estado final", 
					    "Erro", "FIM de simulacao"]

	def __init__(self, route, name=None, nome_arquivo=None, entrada=None):
		self.name = name
		self.route = route
		self.iters = 0
		self.automato = {"inicial": None, 
						 "transicoes" : None , 
						 "finais" : None}
		self.automato["transicoes"] = []
		self.automato["finais"] = []

		self.simulador_af = {"estado_corrente": None,
							 "cabecote" : None,
							 "esquerda": [],
							 "direita": []}

		self.askForDescription(nome_arquivo)
		self.events_from_last_simulation = []

		if entrada != None:
			self.simulador_af["direita"] = entrada

	def askForDescription(self, automato_arquivo=None):
		if automato_arquivo == None: 
			automato_arquivo = raw_input("Insira o nome do arquivo com a descricao do automato finito: ")

		with open(automato_arquivo) as f:
			filelines = f.readlines()

			if str(filelines[0].split()[0][0]) == "*":
				self.automato["finais"].append(filelines[0].split()[0][1:])
				self.automato["inicial"] = filelines[0].split()[0][1:]
			else:
				self.automato["inicial"] = filelines[0].split()[0]
			for line in filelines[1:]:
				words = line.split() 
				transicao = dict()
				transicao["atual"]= words[0]
				transicao["entrada"] = words[1] 
				if words[2][0] == "*": 
					transicao["proximo"] = words[2][1:]
					if words[2][1:] not in self.automato["finais"]:
						self.automato["finais"].append(words[2][1:])
				else:
					transicao["proximo"] = words[2]
				self.automato["transicoes"].append(transicao) 


	def askForInput(self):
		entrada_arquivo = raw_input("Insira o nome do arquivo com a ENTRADA para o dispositivo: ")
		with open(entrada_arquivo) as f:
					filelines = f.readlines()
					for line in filelines:
						words = line.split() 
						for word in words:
							self.simulador_af["direita"].append(word)


	def imprimir(self, instante):
		print "--------------------------------"
		if self.name != None: print "Maquina: " + self.name
		print "Instante: " + str(instante)
		print "Estado Corrente: " + str(self.simulador_af["estado_corrente"])
		print "Cabecote: " + str(self.simulador_af["cabecote"])
		print "Cadeia a esquerda: ",
		if len(self.simulador_af["esquerda"]) != 0:
			for simbolo in self.simulador_af["esquerda"][:]:
				print simbolo,
		else:
			print "Vazio",
		print "\nCadeia a direita: ",
		if len(self.simulador_af["direita"]) != 0:
			for simbolo in self.simulador_af["direita"]:
				print simbolo,
			print "\n",
		else:
			print "Vazio"

	def setDescription(self, descrip):
		self.automato = descrip

	def setSimAF(self, simaf):
		self.simulador_af = simaf

	def setInput(self, input_):
		self.simulador_af["direita"] = input_

	def rodar(self, submaqs=None, i=0):
		if self.simulador_af["estado_corrente"] == None:
			self.simulador_af["estado_corrente"] = self.automato["inicial"]

		if self.name == None:
			self.simulador_af["cabecote"] = self.simulador_af["direita"][0]
			self.simulador_af["direita"].pop(0)

		#Modifiquei isso para funcionar, talvez quebre o AP, de qualquer forma, refatorar tudo.
		if self.name != None:
			self.simulador_af["cabecote"] = self.simulador_af["direita"][0]
			self.simulador_af["direita"].pop(0)
			
			#self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[0] + " (" + self.name + ")")
			#print "--> Evento: " + self.events_from_last_simulation[-1]
		else:
			self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[0])
			print "--> Evento: " + self.events_from_last_simulation[-1]
		self.imprimir(i)
		fim = False
		legal = True

		while self.simulador_af["cabecote"] != "#" and legal: 
			i += 1
			self.iters = i
			legal = False
			#movimentando cabecote
		
			for transicao in self.automato["transicoes"]:
				if transicao.get('atual') == self.simulador_af["estado_corrente"] and transicao.get('entrada') == self.simulador_af["cabecote"]:
					self.simulador_af["estado_corrente"] = transicao.get('proximo')
					legal = True
					self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[1] + " (" + self.simulador_af["cabecote"] + ")")
					print "--> Evento: " + self.events_from_last_simulation[-1]

					self.simulador_af["esquerda"].append(self.simulador_af["cabecote"])
					self.simulador_af["cabecote"] = self.simulador_af["direita"][0]
					self.simulador_af["direita"].pop(0)
					self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[2])
					print "--> Evento: " + self.events_from_last_simulation[-1]
					if self.route:
						self.imprimir(i)
					break
			

			if not legal and submaqs != None:
				for transicao in self.automato["transicoes"]:
					if transicao.get('atual') == self.simulador_af["estado_corrente"]:
						if transicao.get('entrada') in submaqs:
							return {"from": self.name, "to": transicao.get('entrada'), "state": transicao.get('proximo')}

		print "\n"
		if not legal:
			if self.simulador_af["estado_corrente"] in self.automato["finais"] and self.name != None:
				print "A maquina " + self.name + " terminou em um estado de aceitacao: " + self.simulador_af["estado_corrente"]
				self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[3] + " (" + self.simulador_af["estado_corrente"] + ")")
				print "--> Evento: " + self.events_from_last_simulation[-1]
				ok = True
			else:
				print "Entrada invalida, fim da simulacao"
				self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[4])
				print "--> Evento: " + self.events_from_last_simulation[-1]
				ok = False
		else:
			if self.simulador_af["estado_corrente"] in self.automato["finais"]: 
				print "Terminou em um estado de aceitacao: " + self.simulador_af["estado_corrente"]
				self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[3] + " (" + self.simulador_af["estado_corrente"] + ")")
				print "--> Evento: " + self.events_from_last_simulation[-1]
				ok = True
			else:
				print "Terminou em estado nao terminal. Nao aceita."
				ok = False
			
		if self.name == None:
			self.events_from_last_simulation.append(AutomatoFinito.tipos_eventos_af[5])
			print "--> Evento: " + self.events_from_last_simulation[-1]
			user_input = raw_input("(s) Para imprimir lista de eventos ocorridos na simualacao (n) para simplesmente terminar: ")
			if user_input == "s":
				for event in self.events_from_last_simulation:
					print event 
			print "Aperte ENTER para continuar..."
		return (ok, self.simulador_af["esquerda"], self.simulador_af["direita"])


class MaquinaTuring(AutomatoFinito):
	tipos_eventos_af = ["Partida inicial", "Leitura de simbolo", 
					    "Cabecote p/ direita", "Atingiu algum estado final", 
					    "Erro", "FIM de simulacao"]

	tipos_eventos_mt = AutomatoFinito.tipos_eventos_af + ["Gravacao de simbolo", "Cabecote p/ esquerda", 
					    								  "Atingiu o estado H", "Bloqueio"]

	def __init__(self, route):
		AutomatoFinito.__init__(self, route)

	def askForDescription(self, automato_arquivo=None):
		automato_arquivo = raw_input("Insira o nome do arquivo com a descricao da Maquina de Turing: ")
		with open(automato_arquivo) as f:
			filelines = f.readlines()
			self.automato["finais"].append("h")
			if str(filelines[0].split()[0][0]) == "*":
				self.automato["finais"].append(filelines[0].split()[0][1:])
				self.automato["inicial"] = filelines[0].split()[0][1:]
			else:
				self.automato["inicial"] = filelines[0].split()[0]
			for line in filelines[1:]:
				words = line.split() 
				transicao = dict()
				transicao["atual"]= words[0]
				transicao["entrada"] = words[1] 
				transicao["proximo"] = words[2]
				transicao["elemento_b"] = words[3]
				#print transicao
				self.automato["transicoes"].append(transicao) 
			print self.automato


	def askForInput(self):
		entrada_arquivo = raw_input("Insira o nome do arquivo com a ENTRADA para a Maquina de Turing: ")
		with open(entrada_arquivo) as f:
					filelines = f.readlines()
					for line in filelines:
						words = line.split() 
						for word in words:
							self.simulador_af["esquerda"].append(word)
		print self.simulador_af

	def rodar(self):
		self.simulador_af["estado_corrente"] = self.automato["inicial"]
		self.simulador_af["cabecote"] = self.simulador_af["esquerda"][-1]
		self.simulador_af["esquerda"].pop(-1)

		i = 0
		self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[0])
		print "--> Evento: " + self.events_from_last_simulation[-1]
		self.imprimir(i)
		fim = False
		legal = True
		bloqueio = False
		while not fim and legal and not bloqueio: 
			i += 1
			legal = False
			#movimentando cabecote
		 
			for transicao in self.automato["transicoes"]:
				if transicao.get('atual') == self.simulador_af["estado_corrente"] and transicao.get('entrada') == self.simulador_af["cabecote"]:
					self.simulador_af["estado_corrente"] = transicao.get('proximo')
					legal = True
					self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[1] + " (" + self.simulador_af["cabecote"] + ")")
					print "--> Evento: " + self.events_from_last_simulation[-1]

					#Acao do elemento b
					if transicao.get('elemento_b') == 'r':
						if self.simulador_af["cabecote"] == "#" and len(self.simulador_af["direita"]) == 0:
							bloqueio = True
							self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[9])
						else:
							self.simulador_af["esquerda"].append(self.simulador_af["cabecote"])
							self.simulador_af["cabecote"] = self.simulador_af["direita"][0]
							self.simulador_af["direita"].pop(0)
							self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[2])
					else:
						if transicao.get('elemento_b') == 'l':
							if self.simulador_af["cabecote"] == "#" and len(self.simulador_af["esquerda"]) == 0:
								bloqueio = True
								self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[9])
							else:
								self.simulador_af["direita"].insert(0, self.simulador_af["cabecote"])
								self.simulador_af["cabecote"] = self.simulador_af["esquerda"][-1]
								self.simulador_af["esquerda"].pop(-1)
								self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[7])
						else:
							self.simulador_af["cabecote"] = transicao.get('elemento_b')
							self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[6])
							
					print "--> Evento: " + self.events_from_last_simulation[-1]
					if self.simulador_af["estado_corrente"] == "h":
						fim = True
					break

			if self.route:
				self.imprimir(i)

		print "\n"
		if not legal:
			self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[4])
			print "--> Evento: " + self.events_from_last_simulation[-1]
			print "Entrada invalida, fim da simulacao"
		else:
			if self.simulador_af["estado_corrente"] in self.automato["finais"]: 
				self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[8])
				print "--> Evento: " + self.events_from_last_simulation[-1]
			else:
				print "Terminou em estado nao terminal. Nao aceita."
		self.events_from_last_simulation.append(MaquinaTuring.tipos_eventos_mt[5])
		print "--> Evento: " + self.events_from_last_simulation[-1]
		user_input = raw_input("(s) Para imprimir lista de eventos ocorridos na simualacao (n) para simplesmente terminar: ")
		if user_input == "s":
			for event in self.events_from_last_simulation:
				print event 
		print "Aperte ENTER para continuar..."




class AutomatoPilha():
	def __init__(self, route):
		self.route = route
		self.iters = 0
		self.nMaqs = 0
		self.Maqs = []
		self.nameMaqs = []
		self.pilha = []
		self.simulador_ap = {"estado_corrente": None,
					 "cabecote" : None,
					 "esquerda": [],
					 "direita": []}
		self.askForDescription()

	def askForDescription(self):
		automato_arquivo = raw_input("Insira o nome do arquivo com a descricao do Automato de Pilha: ")
		with open(automato_arquivo) as f:
			self.nMaqs = int(f.next())
			for i in range(self.nMaqs):
				nome = f.next()[:-1]
				self.nameMaqs.append(nome)
				linha = f.next()
				text_file = open("AF_temporario.txt", "w")
				while linha != "@\n":
					text_file.write(linha)
					linha = f.next()
				text_file.close()
				self.Maqs.append(AutomatoFinito(self.route, nome, "AF_temporario.txt"))			

			
	def askForInput(self):
		entrada_arquivo = raw_input("Insira o nome do arquivo com a ENTRADA para o Automato de Pilha: ")
		with open(entrada_arquivo) as f:
					filelines = f.readlines()
					for line in filelines:
						words = line.split() 
						for word in words:
							self.simulador_ap["direita"].append(word)


	def rodar(self):
		#Inicia empilhando a maquina principal com o estado inicial
		inicial = {"maquina": self.Maqs[0].name, "estado": self.Maqs[0].automato["inicial"]}
		self.pilha.append(inicial)

		self.simulador_ap["cabecote"] = self.simulador_ap["direita"][0]
		self.simulador_ap["direita"].pop(0)

		self.Maqs[0].setSimAF(self.simulador_ap)
		print "Iniciando simulacao com maquina " + self.Maqs[0].name
		#while len(self.pilha) != 0:
		#while self.simulador_ap["cabecote"] != "#" and  len(self.pilha) != 0:
		while len(self.pilha) != 0:
			for p in self.pilha:
					print p

			maquina_da_vez = self.pilha[-1]["maquina"]
			simulador_AF = self.simulador_ap
			simulador_AF["estado_corrente"] = self.pilha[-1]["estado"]

			for maquina in self.Maqs:
				if maquina.name == maquina_da_vez:
					maquina.setSimAF(simulador_AF)
					#print "Evento -> Chamada de maquina: " + maquina.name
					if simulador_AF["estado_corrente"] == None:
						print "--> Evento: Chamada de maquina: " + maquina.name
					else:
						print "--> Evento: Retomando execucao da maquina: " + maquina.name
					retorno = maquina.rodar(self.nameMaqs, i=self.iters)
					self.simulador_ap = maquina.simulador_af
					self.iters += maquina.iters - self.iters
			if type(retorno) is dict:
				self.pilha[-1]["estado"] = retorno["state"]				
				call = {"maquina": retorno["to"], "estado": None}
				self.pilha.append(call)
				
			if retorno == False:
				print "Simulacao do Automato de Pilha finalizada, cadeia nao aceita"
				return False
			if retorno == True:
				self.pilha = self.pilha[:-1]
				print "--> Evento: Retorno de submaquina"

		if retorno == True: print "Simulacao finalizada com sucesso, cadeia aceita"
		print "Pressione ENTER para continuar"
		return True
		

#def main():
#simulador = Simulador()
#end = False
#while not end:
#	end = simulador.showOptionsWait()
