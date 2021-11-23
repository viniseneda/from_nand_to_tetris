import sys
import dic
import os

bootstrap = [["@SP"],["M=256"],["call", "Sys.init"]]

if len(sys.argv) != 2:
	print(len(sys.argv))
	print("Use: test1.py + infile.asm or folder")
	quit()

class translator:
	def __init__(self, file_name):
		file = open(file_name, "w")
		self.file = file
		self.counter = 0
		self.m = 0

	def print_replace(self, line):
		if isinstance(line, list):
			y = line[0]
			self.m = 0
			if y == "a":
				print("".join(["@", str(self.parser.b)]))
				self.file.write("".join(["@", str(self.parser.b), "\n"]))
			elif y == "b":
				print("".join(["@", str(self.s_name), ".", self.parser.b]))
				self.file.write("".join(["@", str(self.s_name), ".", self.parser.b, "\n"]))
			elif y == "c":
				print("".join(["@", str(int(self.parser.b) + line[1])]))
				self.file.write("".join(["@", str(int(self.parser.b) + line[1]), "\n"]))
			elif y == "d":
				print("".join(["@END", str(self.counter)]))
				self.file.write("".join(["@END", str(self.counter), "\n"]))
				self.m = 1
			elif y == "e":
				print("".join(["(END", str(self.counter), ")"]))
				self.file.write("".join(["(END", str(self.counter), ")", "\n"]))
				self.m = 1
			elif y == "f":
				print("".join(["(", str(self.parser.a), ")"]))
				self.file.write("".join(["(", str(self.parser.a), ")", "\n"]))
			elif y == "g":
				print("".join(["@", str(self.parser.a)]))
				self.file.write("".join(["@", str(self.parser.a), "\n"]))
			elif y == "h":
				print("".join(["(", str(self.return_address), str(self.counter), ")"]))
				self.file.write("".join(["(", str(self.return_address), str(self.counter), ")", "\n"]))
				self.m = 1	
			elif y == "i":
				print("".join(["@", str(self.return_address), str(self.counter)]))
				self.file.write("".join(["@", str(self.return_address), str(self.counter), "\n"]))
				self.m = 1
			elif y == "j":
				print("".join(["@", str(int(self.parser.b) + line[1])]))
				self.file.write("".join(["@", str(int(self.parser.b) + line[1]), "\n"]))
		else:
			print(line)
			self.file.write("".join([line,"\n"]))


	def translate(self, parser, s_name):
		self.parser = parser
		self.s_name = s_name
		self.return_address = "".join([self.parser.a, ".", "return"])
		if self.parser.task == "function":
			self.print_replace(["f"])
			for x in range(int(self.parser.b)):
				for line in dic.dict[parser.task]:
					self.print_replace(line)
		elif parser.a == "not" or parser.b == "not" or self.parser.task == "call":
			for line in dic.dict[parser.task]:
				self.print_replace(line)
		else:
			for line in dic.dict[parser.task][parser.a]:
				self.print_replace(line)
		if self.m == 1:
			self.counter += 1

class parser:
	def __init__(self, file_name):
		file = open(file_name, "r")
		self.file = file

	def find_line(self):
		file = self.file
		line = file.readline()
		while line.find('//') == 0 or line.find('\n') == 0:
			line = file.readline()
		self.file = file

		line = line.split("//")[0]
		part = line.split()
		if len(part) == 3:
			self.task = part[0]
			self.a = part[1]
			self.b = part[2]
		elif len(part) == 1:
			self.task = part[0]
			self.a = "not"
			self.b = "not"
		elif len(part) == 2:
			self.task = part[0]
			self.a = part[1]
			self.b = "not"
		else:
			return("&&&")
class main:
	def __init__(self):
		if sys.argv[1].find(".vm") == -1:
			self.files = os.listdir(sys.argv[1])
			self.translator = translator("".join([sys.argv[1],"/", sys.argv[1].split(".")[0], ".asm"]))
			print("".join([sys.argv[1], ".asm"]))
			self.file_name = "bootstrap.vm"
			self.item = "bootstrap.vm"
			self.process_file()
			for item in self.files:
				if item.find(".vm") != -1:
					self.item = item
					self.file_name = "".join([sys.argv[1],"/", item])
					self.process_file()
		else:
			self.item = sys.argv[1]
			self.translator = translator("".join([sys.argv[1].split(".")[0], ".asm"]))
			self.file_name = sys.argv[1]
			self.process_file()

	def process_file(self):
		self.s_name = self.item.split(".")[0]
		par = parser(self.file_name)
		while par.find_line() != "&&&":
			print(par.task, par.a, par.b)
			self.translator.translate(par, self.s_name)
			print()

d = main()



		
		
