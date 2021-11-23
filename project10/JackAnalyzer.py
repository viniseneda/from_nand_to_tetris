import sys
import os

symbol = ['{','}','(',')','[',']','.',',',';','+','-','*','/','&','|','<','>','=','~']
keyword = ['class','constructor','function','method','field','static','var','int','char','boolean','void','true','false','null','this','let','do','if','else','while','return']
op = ['+','-','*','/','&','|','<','>','=']
spaces = ['\n', ' ', '	']

if len(sys.argv) != 2:
	print(len(sys.argv))
	print("Use: test1.jack infile")
	quit()

class tokenizer:
	def __init__(self, file_name):
		file = open(file_name, "r")
		self.file = file
		self.line_counter = 0
		self.cursor = self.file.tell()
		self.current = self.file.read(1)
		self.line_counter = 0
		self.eof = False
	
	def read(self):
		self.current = self.file.read(1)
		if not self.current:
			self.eof = True
			return
		else:
			self.eof = False
		if self.current == "\n":
			self.line_counter += 1
		self.cursor = self.file.tell()


	def skip_comments(self):
		temp = self.cursor
		self.read()
		
		if self.current == "*":	
			while True:
				self.read()
				while self.current != "*":
					self.read()
				self.read()
				if self.current == "/":
					self.read()
					return;
		elif self.current == "/":
			while self.current != "\n":
				self.read()
			return
		else:
			self.file.seek(temp - 1)
			self.read()
			return

	def is_in(self, c, list):
		for item in list:
			if c == item:
				return True
		return False

	def def_label(self):
		if self.is_in(self.token, keyword):
			self.label = "keyword"
		elif self.token.isdigit():
			self.label = "integerConstant"
		else:
			self.label = "identifier"
		return

	def find_next(self):
		temp = []
		while True:
			if self.eof == True:
				break
			if self.current == "/":
				self.skip_comments()
				if self.current == "/":
					self.token = self.current
					self.read()
					self.label = "symbol"
					break
			if self.current == '"':
				self.read()			
				while self.current != '"' and self.current != '\n':
					temp.append(self.current)
					self.read()
				self.token = "".join(temp)
				self.label = "stringConstant"
				self.read()
				break
			if self.is_in(self.current, symbol) or self.is_in(self.current, spaces):
				if temp != []:
					self.token = "".join(temp)
					if not self.is_in(self.current, spaces):
						self.def_label()
						break
					self.read()
					self.def_label()
					break
				elif self.is_in(self.current, symbol) :
					self.token = self.current
					self.read()
					self.label = "symbol"
					break
				else:
					self.read()
			elif not self.is_in(self.current, spaces):
				temp.append(self.current)
				self.read()
		return

class compilationEngine:	
	def xml_labels(state, label):
		if state == "open":
			print("".join(["<", label, "> "]), end = "")
			out.write("".join(["<", label, "> \n"]))
		elif state == "op":
			print("".join(["<", label, "> "]), end = "")
			out.write("".join(["<", label, "> "]))
		else:
			print("".join([" </", label, ">"]))
			out.write("".join([" </", label, ">\n"]))
		return
		
	def xml_whole_token():
		compilationEngine.xml_labels("op", t.label)
		print(t.token, end = "")
		if t.token == "<":
			out.write("&lt;")
		elif t.token == ">":
			out.write("&gt;")
		elif t.token == "&":
			out.write("&amp;")
		else:
			out.write(t.token)
		compilationEngine.xml_labels("close", t.label)
		return
	
	def cond(boole):
		if boole:
			compilationEngine.xml_whole_token()
			if t.eof == False:
				t.find_next()
			return
		else:
			print("ERROR IN LINE:", t.line_counter)
			print(t.token)
			quit()

	def type():
		return t.token == "int" or  t.token =="char" or  t.token == "boolean" or t.label == "identifier"

	def compile_class(self):
		compilationEngine.xml_labels("open", "class")
		print()
		t.find_next()
		compilationEngine.cond(t.token == "class")
		compilationEngine.cond(t.label == "identifier")
		compilationEngine.cond(t.token == "{")
		compilationEngine.compile_classVarDec()
		compilationEngine.subroutineDec()
		compilationEngine.cond(t.token == "}")
		compilationEngine.xml_labels("close", "class")	
		
	def coma_var(): #parse the (, varName)*
		if t.token != ",":
			return
		else:
			compilationEngine.cond(t.token == ",")
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.coma_var()

	def compile_classVarDec():
		if t.token != "static" and t.token != "field":
			return
		else:
			compilationEngine.xml_labels("open", "classVarDec")
			print()
			compilationEngine.cond(t.token == "static" or "field")
			compilationEngine.cond(compilationEngine.type())
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.coma_var()
			compilationEngine.cond(t.token == ";")
			compilationEngine.xml_labels("close", "classVarDec")
			compilationEngine.compile_classVarDec()
	
	def subroutineDec():
		if t.token != "constructor" and t.token != "function" and t.token != "method":
			return
		else:
			compilationEngine.xml_labels("open", "subroutineDec")
			print()
			compilationEngine.cond(t.token == "constructor" or t.token == "function" or t.token == "method")
			compilationEngine.cond(t.token == "void" or compilationEngine.type())
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.cond(t.token == "(")
			compilationEngine.xml_labels("open", "parameterList")
			compilationEngine.parameterList()
			compilationEngine.xml_labels("close", "parameterList")
			compilationEngine.cond(t.token == ")")
			compilationEngine.subroutineBody()
			compilationEngine.xml_labels("close", "subroutineDec")
			compilationEngine.subroutineDec()

	def subroutineBody():
		compilationEngine.xml_labels("open", "subroutineBody")
		compilationEngine.cond(t.token == "{")
		compilationEngine.varDec()
		compilationEngine.statements()
		compilationEngine.cond(t.token == "}")
		compilationEngine.xml_labels("close", "subroutineBody")

	def varDec():
		if t.token != "var":
			return
		compilationEngine.xml_labels("open", "varDec")
		compilationEngine.cond(t.token == "var")
		compilationEngine.cond(compilationEngine.type())
		compilationEngine.cond(t.label == "identifier")
		compilationEngine.coma_var()
		compilationEngine.cond(t.token == ";")
		compilationEngine.xml_labels("close", "varDec")
		compilationEngine.varDec()
	
	def coma_type_var(): #parse the ( , type var)
		if t.token != ",":
			return
		else:
			compilationEngine.cond(t.token == ",")
			compilationEngine.cond(compilationEngine.type())
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.coma_type_var()
			
	def parameterList():
		if not compilationEngine.type():
			return
		else:
			compilationEngine.cond(compilationEngine.type())
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.coma_type_var()

#statments

	def statements():
		compilationEngine.xml_labels("open", "statements")
		compilationEngine.statementsRec()
		compilationEngine.xml_labels("close", "statements")

	def statementsRec():
		if t.token != "let" and t.token != "if" and t.token != "while" and t.token != "do" and t.token != "return":
			return
		else:
			if t.token == "let":
				compilationEngine.xml_labels("open", "letStatement")
				compilationEngine.let_statment()
				compilationEngine.xml_labels("close", "letStatement")
			elif t.token == "if":
				compilationEngine.xml_labels("open", "ifStatement")
				compilationEngine.if_statment()
				compilationEngine.xml_labels("close", "ifStatement")
			elif t.token == "while":
				compilationEngine.xml_labels("open", "whileStatement")
				compilationEngine.while_statment()
				compilationEngine.xml_labels("close", "whileStatement")
			elif t.token == "do":
				compilationEngine.xml_labels("open", "doStatement")
				compilationEngine.do_statment()
				compilationEngine.xml_labels("close", "doStatement")
			elif t.token == "return":
				compilationEngine.xml_labels("open", "returnStatement")
				compilationEngine.return_statment()
				compilationEngine.xml_labels("close", "returnStatement")
			compilationEngine.statementsRec()	
			
	def let_statment():
		compilationEngine.cond(t.token == "let")
		compilationEngine.cond(t.label == "identifier")
		if t.token == "[":
			compilationEngine.cond(t.token == "[")
			compilationEngine.expression() 
			compilationEngine.cond(t.token == "]")
		compilationEngine.cond(t.token == "=")
		compilationEngine.expression() 
		compilationEngine.cond(t.token == ";")

	def if_statment():
		compilationEngine.cond(t.token == "if")
		compilationEngine.cond(t.token == "(")
		compilationEngine.expression() 
		compilationEngine.cond(t.token == ")")
		compilationEngine.cond(t.token == "{")
		compilationEngine.statements()
		compilationEngine.cond(t.token == "}")
		if t.token == "else":
			compilationEngine.cond(t.token == "else")
			compilationEngine.cond(t.token == "{")
			compilationEngine.statements()
			compilationEngine.cond(t.token == "}")

	def while_statment():
		compilationEngine.cond(t.token == "while")
		compilationEngine.cond(t.token == "(")
		compilationEngine.expression() 
		compilationEngine.cond(t.token == ")")
		compilationEngine.cond(t.token == "{")
		compilationEngine.statements()
		compilationEngine.cond(t.token == "}")
	
	def do_statment():
		compilationEngine.cond(t.token == "do")
		compilationEngine.cond(t.label == "identifier") #subroutineCall
		if t.token == ".":
			compilationEngine.cond(t.token == ".") #print the dot "."
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.cond(t.token == "(")
			compilationEngine.expressionList()
			compilationEngine.cond(t.token == ")")
		elif t.token == "(":
			compilationEngine.cond(t.token == "(")
			compilationEngine.expressionList()
			compilationEngine.cond(t.token == ")")
		compilationEngine.cond(t.token == ";")

	def return_statment():
		compilationEngine.cond(t.token == "return")
		if t.token != ";":
			compilationEngine.expression()
		compilationEngine.cond(t.token == ";")

##expression

	def expression():
		compilationEngine.xml_labels("open", "expression")
		compilationEngine.loop()
		compilationEngine.xml_labels("close", "expression")

	def loop():
		compilationEngine.term()
		if t.is_in(t.token, op):
			compilationEngine.cond(True)
			compilationEngine.loop()

	def term():
		compilationEngine.xml_labels("open", "term")
		if t.label == "stringConstant":
			compilationEngine.cond(t.label == "stringConstant")
		elif t.label == "integerConstant":
			compilationEngine.cond(t.label == "integerConstant")
		elif t.token == "true" or t.token == "false" or t.token == "null" or t.token == "this":
			compilationEngine.cond(True)
		elif t.label == "identifier":
			compilationEngine.cond(t.label == "identifier")
			if t.token == "[":
				compilationEngine.cond(t.token == "[")
				compilationEngine.expression()
				compilationEngine.cond(t.token == "]")
			elif t.token == ".":
				compilationEngine.cond(t.token == ".") #print the dot "."
				compilationEngine.cond(t.label == "identifier") #subroutineCall (não consegui colocar numa fução só)
				compilationEngine.cond(t.token == "(")
				compilationEngine.expressionList()
				compilationEngine.cond(t.token == ")")
			elif t.token == "(":
				compilationEngine.cond(t.token == "(")
				compilationEngine.expressionList()
				compilationEngine.cond(t.token == ")")
		elif t.token == "(":
			compilationEngine.cond(t.token == "(")
			compilationEngine.expression()
			compilationEngine.cond(t.token == ")")
		elif t.token == "~" or t.token == "-":
			compilationEngine.cond(True)
			compilationEngine.term()
		compilationEngine.xml_labels("close", "term")

	def expressionList():
			compilationEngine.xml_labels("open", "expressionList")
			if t.token != ")":
				compilationEngine.expressionL()
			compilationEngine.xml_labels("close", "expressionList")

	def expressionL():
			compilationEngine.expression()
			if t.token == ",":
				compilationEngine.cond(t.token == ",")
				compilationEngine.expressionL()	

#Checks if directory and compile every file

lista = []
if sys.argv[1].find(".jack") == -1:
	files = os.listdir(sys.argv[1])
	for item in files:
		if item.find(".jack") != -1:
			lista.append("".join([sys.argv[1],"/", item]))

else:
	t = tokenizer(sys.argv[1])
	temp = "".join([sys.argv[1].split(".")[0], ".xml"])
	out = open(temp, "w")
	comp = compilationEngine()
	comp.compile_class()
	quit()

for thing in lista:
	t = tokenizer(thing)
	temp = "".join([thing.split(".")[0], ".xml"])
	out = open(temp, "w")
	comp = compilationEngine()
	comp.compile_class()
	


