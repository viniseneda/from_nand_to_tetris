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

class labelGen:
		def __init__(self):
			self.number = 0
		def new(self):
			temp = self.number
			self.number += 1
			return "".join(["L", str(temp)])
			
class table_finder:
	def __init__(self, name):
		dic = {"var":"local", "arg":"argument", "field":"this", "static":"static"}
		if  class_table.positionFinder(name) == "NOT" and sub_table.positionFinder(name) == "NOT":
			class_table.print()
			print(name, "NOT IN SYMBOL TABLE")
			quit()
		if class_table.positionFinder(name) == "NOT":
			self.kind = dic[sub_table.kindOf(name)]
			self.index = sub_table.indexOf(name)
			self.type = sub_table.typeOf(name)
		else:
			self.kind = dic[class_table.kindOf(name)]
			self.index = class_table.indexOf(name)
			self.type = class_table.typeOf(name)

class vmwriter:
	def writePush(segment, inte):
		print(" ".join(["push", segment, str(inte)]))
		out.write(" ".join(["push", segment, str(inte), "\n"]))

	def writePop(segment, inte):
		print(" ".join(["pop", segment, str(inte)]))
		out.write(" ".join(["pop", segment, str(inte), "\n"]))

	def writeArithmetic(command):
		dic = {"+":"add" , "-":"sub", "&":"and", "|":"or", "~":"not", "=":"eq", ">":"gt", "<":"lt", "neg":"neg"}
		if command == "*":
			vmwriter.writeCall("Math.multiply", 2)
		elif command == "/":
			vmwriter.writeCall("Math.divide", 2)
		else:
			print(" ".join([dic[command]]))
			out.write(" ".join([dic[command], "\n"]))
	
	def writeLabel(label):
		print(" ".join(["label", label]))
		out.write(" ".join(["label", label, "\n"]))

	def writeGoto(label):
		print(" ".join(["goto", label]))
		out.write(" ".join(["goto", label, "\n"]))

	def writeIf(label):
		print(" ".join(["if-goto", label]))
		out.write(" ".join(["if-goto", label, "\n"]))
	
	def writeCall(segment, inte):
		print(" ".join(["call", segment, str(inte)]))
		out.write(" ".join(["call", segment, str(inte), "\n"]))

	def writeFunction(segment, inte):
		print(" ".join(["function", segment, str(inte)]))
		out.write(" ".join(["function", segment, str(inte), "\n"]))

	def writeReturn():
		print(" ".join(["return"]))
		out.write(" ".join(["return", "\n"]))

class symbolTable:
	def __init__(self):
		self.table = {"name":[], "type":[], "kind":[], "index":[]}
		
	def startSubroutine(self):
		self.table = {"name":[], "type":[], "kind":[], "index":[]}

	def indexFinder(self, kind):
		i = 0
		for item in self.table["kind"]:
			if item == kind:
				i += 1
		return i
	
	def print(self):
		for item in self.table:
			temp = []
			for thing in self.table[item]:
				print(thing)
	
	def positionFinder(self, name):
		i = 0
		for item in self.table["name"]:
			if item == name:
				return i
			else:
				i += 1
		return "NOT"

	def numOf(self, element):
		temp = 0
		for item in self.table["kind"]:
			if item == element:
				temp += 1
		return temp

	def kindOf(self, name):
		temp = self.positionFinder(name)
		return self.table["kind"][temp]

	def typeOf(self, name):
		temp = self.positionFinder(name)
		return self.table["type"][temp]

	def indexOf(self, name):
		temp = self.positionFinder(name)
		return self.table["index"][temp]

	def define(self, name, type, kind):
		temp = self.indexFinder(kind)
		self.table["name"].append(name)
		self.table["type"].append(type)
		self.table["kind"].append(kind)
		self.table["index"].append(temp)

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
	def cond(boole):
		if boole:
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
		t.find_next()
		class_table.startSubroutine()
		compilationEngine.cond(t.token == "class")
		class_name = t.token
		compilationEngine.cond(t.label == "identifier")
		compilationEngine.cond(t.token == "{")
		compilationEngine.compile_classVarDec()
		compilationEngine.subroutineDec(class_name)
		compilationEngine.cond(t.token == "}")
		
	def coma_var(a, type, kind): #parse the (, varName)*
		if t.token != ",":
			return
		elif a == 0:
			compilationEngine.cond(t.token == ",")
			name = t.token
			compilationEngine.cond(t.label == "identifier")
			class_table.define(name, type, kind)
			compilationEngine.coma_var(0, type, kind)
		else:
			compilationEngine.cond(t.token == ",")
			name = t.token
			compilationEngine.cond(t.label == "identifier")
			sub_table.define(name, type, kind)
			compilationEngine.coma_var(1, type, kind)

	def compile_classVarDec():
		if t.token != "static" and t.token != "field":
			return
		else:
			kind = t.token
			compilationEngine.cond(t.token == "static" or "field")
			type = t.token
			compilationEngine.cond(compilationEngine.type())
			name = t.token
			compilationEngine.cond(t.label == "identifier")
			class_table.define(name, type, kind)
			compilationEngine.coma_var(0, type, kind)
			compilationEngine.cond(t.token == ";")
			compilationEngine.compile_classVarDec()
	
	def subroutineDec(class_name):
		if t.token != "constructor" and t.token != "function" and t.token != "method":
			return
		else:
			sub_table.startSubroutine()
			routine_type = t.token
			compilationEngine.cond(t.token == "constructor" or t.token == "function" or t.token == "method")
			compilationEngine.cond(t.token == "void" or compilationEngine.type())
			sub_name = t.token
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.cond(t.token == "(")
			if routine_type == "method":
				sub_table.define("this", "address", "arg")
			compilationEngine.parameterList() #has the arguments to the symbol table
			compilationEngine.cond(t.token == ")")
			compilationEngine.subroutineBody(class_name, sub_name, routine_type)
			compilationEngine.subroutineDec(class_name)

	def subroutineBody(class_name, sub_name, routine_type):
		compilationEngine.cond(t.token == "{")
		compilationEngine.varDec()
		vmwriter.writeFunction("".join([class_name, ".", sub_name]), sub_table.numOf("var"))
		if routine_type == "constructor":
				vmwriter.writePush("constant", class_table.numOf("field"))
				vmwriter.writeCall("Memory.alloc", 1)
				vmwriter.writePop("pointer", 0)
		elif routine_type == "method":
			vmwriter.writePush("argument", 0)
			vmwriter.writePop("pointer", 0)
		compilationEngine.statements(class_name)
		compilationEngine.cond(t.token == "}")

	def varDec():
		if t.token != "var":
			return
		kind = t.token
		compilationEngine.cond(t.token == "var")
		type = t.token
		compilationEngine.cond(compilationEngine.type())
		name = t.token
		compilationEngine.cond(t.label == "identifier")
		sub_table.define(name, type, kind)
		compilationEngine.coma_var(1, type, kind)
		compilationEngine.cond(t.token == ";")
		compilationEngine.varDec()
	
	def coma_type_var(): #parse the ( , type var)
		if t.token != ",":
			return
		else:
			compilationEngine.cond(t.token == ",")
			type = t.token
			compilationEngine.cond(compilationEngine.type())
			name = t.token
			kind = "arg"
			compilationEngine.cond(t.label == "identifier")
			sub_table.define(name, type, kind)
			compilationEngine.coma_type_var()
			
	def parameterList():
		if not compilationEngine.type():
			return
		else:
			type = t.token
			compilationEngine.cond(compilationEngine.type())
			name = t.token
			kind = "arg"
			compilationEngine.cond(t.label == "identifier")
			sub_table.define(name, type, kind)
			compilationEngine.coma_type_var()

#statments

	def statements(class_name):
		if t.token != "let" and t.token != "if" and t.token != "while" and t.token != "do" and t.token != "return":
			return
		else:
			if t.token == "let":
				compilationEngine.let_statment(class_name)
			elif t.token == "if":
				compilationEngine.if_statment(class_name)
			elif t.token == "while":
				compilationEngine.while_statment(class_name)
			elif t.token == "do":
				compilationEngine.do_statment(class_name)
			elif t.token == "return":
				compilationEngine.return_statment(class_name)
			compilationEngine.statements(class_name)	
			
	def let_statment(class_name):
		compilationEngine.cond(t.token == "let")
		temp = t.token
		compilationEngine.cond(t.label == "identifier")
		if t.token == "[":
			compilationEngine.cond(t.token == "[")
			compilationEngine.expression(class_name)
			a = table_finder(temp)
			vmwriter.writePush(a.kind, a.index)
			vmwriter.writeArithmetic("+") 
			compilationEngine.cond(t.token == "]")
			compilationEngine.cond(t.token == "=")
			compilationEngine.expression(class_name) 
			vmwriter.writePop("temp", 0)
			vmwriter.writePop("pointer", 1)
			vmwriter.writePush("temp", 0)
			vmwriter.writePop("that", 0)
			compilationEngine.cond(t.token == ";")
		else:
			compilationEngine.cond(t.token == "=")
			compilationEngine.expression(class_name) 
			compilationEngine.cond(t.token == ";")
			a = table_finder(temp) 
			vmwriter.writePop(a.kind, a.index)

	def if_statment(class_name):
		label1 = label.new()
		label2 = label.new()
		compilationEngine.cond(t.token == "if")
		compilationEngine.cond(t.token == "(")
		compilationEngine.expression(class_name) 
		vmwriter.writeArithmetic("~")
		vmwriter.writeIf(label2)
		compilationEngine.cond(t.token == ")")
		compilationEngine.cond(t.token == "{")
		compilationEngine.statements(class_name)
		vmwriter.writeGoto(label1)
		compilationEngine.cond(t.token == "}")
		vmwriter.writeLabel(label2)
		if t.token == "else":
			compilationEngine.cond(t.token == "else")
			compilationEngine.cond(t.token == "{")
			compilationEngine.statements(class_name)
			compilationEngine.cond(t.token == "}")
		vmwriter.writeLabel(label1)

	def while_statment(class_name):
		label1 = label.new()
		label2 = label.new()
		vmwriter.writeLabel(label1)
		compilationEngine.cond(t.token == "while")
		compilationEngine.cond(t.token == "(")
		compilationEngine.expression(class_name)
		vmwriter.writeArithmetic("~")
		vmwriter.writeIf(label2) 
		compilationEngine.cond(t.token == ")")
		compilationEngine.cond(t.token == "{")
		compilationEngine.statements(class_name)
		vmwriter.writeGoto(label1)
		compilationEngine.cond(t.token == "}")
		vmwriter.writeLabel(label2)
	
	def do_statment(class_name):
		compilationEngine.cond(t.token == "do")
		nclass_name = t.token
		compilationEngine.cond(t.label == "identifier") #subroutineCall
		if t.token == ".":
			n = 0
			compilationEngine.cond(t.token == ".") #print the dot "."
			if sub_table.positionFinder(nclass_name) != "NOT" or class_table.positionFinder(nclass_name) != "NOT": #look if is at s_table
				a = table_finder(nclass_name) 
				vmwriter.writePush(a.kind, a.index)
				nclass_name = a.type
				n = 1
			function_name = t.token
			compilationEngine.cond(t.label == "identifier")
			compilationEngine.cond(t.token == "(")
			counter = compilationEngine.expressionList(0, class_name)
			counter = counter + n
			compilationEngine.cond(t.token == ")")
			vmwriter.writeCall("".join([nclass_name, ".", function_name]), counter)
		elif t.token == "(":
			vmwriter.writePush("pointer", 0)
			compilationEngine.cond(t.token == "(")
			counter = compilationEngine.expressionList(0, class_name)
			compilationEngine.cond(t.token == ")")
			vmwriter.writeCall("".join([class_name, ".", nclass_name]), counter + 1)
		compilationEngine.cond(t.token == ";")
		vmwriter.writePop("temp", 0) 

	def return_statment(class_name):
		compilationEngine.cond(t.token == "return")
		if t.token != ";":
			compilationEngine.expression(class_name)
			vmwriter.writeReturn()
		else:
			vmwriter.writePush("constant", 0)
			vmwriter.writeReturn()
		compilationEngine.cond(t.token == ";")

##expression

	def expression(class_name):
		compilationEngine.term(class_name)
		if t.is_in(t.token, op):
			temp =  t.token
			compilationEngine.cond(True)
			compilationEngine.expression(class_name)
			vmwriter.writeArithmetic(temp)

	def term(class_name):
		if t.label == "stringConstant":
			string = t.token
			size = len(string)
			compilationEngine.cond(t.label == "stringConstant") 
			vmwriter.writePush("constant", size)
			vmwriter.writeCall("String.new", 1)
			c = 0
			while c < size:
				vmwriter.writePush("constant", ord(string[c])) 
				vmwriter.writeCall("String.appendChar", 2)
				c += 1
			
		elif t.label == "integerConstant":
			vmwriter.writePush("constant", t.token)
			compilationEngine.cond(t.label == "integerConstant")
		elif t.token == "true" or t.token == "false" or t.token == "null" or t.token == "this":
			if t.token == "false" or t.token == "null":
				vmwriter.writePush("constant", 0)
			elif t.token == "true":
				vmwriter.writePush("constant", 1)
				vmwriter.writeArithmetic("neg")
			elif t.token == "this":
				vmwriter.writePush("pointer", 0)
			compilationEngine.cond(True)
		elif t.label == "identifier": 
			temp = t.token
			compilationEngine.cond(t.label == "identifier")
			if t.token == "[":
				compilationEngine.cond(t.token == "[")
				compilationEngine.expression(class_name)
				a = table_finder(temp)
				vmwriter.writePush(a.kind, a.index)
				vmwriter.writeArithmetic("+")
				vmwriter.writePop("pointer", 1)
				vmwriter.writePush("that", 0)
				compilationEngine.cond(t.token == "]")
			elif t.token == ".":
				compilationEngine.cond(t.token == ".") #print the dot "."
				function_name = t.token
				u = 0
				if sub_table.positionFinder(temp) != "NOT" or class_table.positionFinder(temp) != "NOT": #look if is at s_table
					a = table_finder(temp) 
					vmwriter.writePush(a.kind, a.index)
					temp = a.type
					u = 1
				compilationEngine.cond(t.label == "identifier") #subroutineCall (has another instance at do statment)
				compilationEngine.cond(t.token == "(")
				counter = compilationEngine.expressionList(0, class_name)
				counter += u
				vmwriter.writeCall("".join([temp, ".", function_name]), counter)
				compilationEngine.cond(t.token == ")")
			elif t.token == "(":
				compilationEngine.cond(t.token == "(")
				counter = compilationEngine.expressionList(0, class_name)
				vmwriter.writeCall("".join([class_name, ".", temp]), counter)
				compilationEngine.cond(t.token == ")")
			else:
				a = table_finder(temp)
				vmwriter.writePush(a.kind, a.index)
		elif t.token == "(":
			compilationEngine.cond(t.token == "(")
			compilationEngine.expression(class_name)
			compilationEngine.cond(t.token == ")")
		elif t.token == "~" or t.token == "-":
			temp = t.token
			compilationEngine.cond(True)
			compilationEngine.term(class_name)
			if temp == "-":
				vmwriter.writeArithmetic("neg")
			else:
				vmwriter.writeArithmetic(temp)

	def expressionList(counter, class_name):
			if t.token != ")":
				counter += 1
			compilationEngine.expression(class_name)
			if t.token == ",":
				compilationEngine.cond(t.token == ",")
				counter = compilationEngine.expressionList(counter, class_name)
			return counter	

#Checks if directory and compile every file

lista = []
class_table = symbolTable()
sub_table = symbolTable()
label = labelGen()

if sys.argv[1].find(".jack") == -1:
	files = os.listdir(sys.argv[1])
	for item in files:
		if item.find(".jack") != -1:
			lista.append("".join([sys.argv[1],"/", item]))

else:
	t = tokenizer(sys.argv[1])
	temp = "".join([sys.argv[1].split(".")[0], ".vm"])
	out = open(temp, "w")
	comp = compilationEngine()
	comp.compile_class()
	quit()

for thing in lista:
	t = tokenizer(thing)
	temp = "".join([thing.split(".")[0], ".vm"])
	out = open(temp, "w")
	comp = compilationEngine()
	comp.compile_class()
