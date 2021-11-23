import sys
import dic

if len(sys.argv) != 2:
	print(len(sys.argv))
	print("Use: test1.py infile")
	quit()

class translator:
	def __init__(self, file_name):
		file = open(file_name, "w")
		self.file = file
		self.counter = 0
		self.m = 0
	def print_replace(self, line, i):
		if isinstance(line, list):
			if line[1] == 0:
				print(line[0], i, sep="")
				self.file.write("".join([line[0], i, "\n"]))
				self.m = 0
			elif line[1] == 1:
				print(line[0], self.counter, sep="")
				self.file.write("".join([line[0], str(self.counter),"\n"]))
				self.m = 1
			elif line[1] == 2:
				print(line[0], self.counter, ")", sep="")
				self.file.write("".join([line[0], str(self.counter), ")","\n"]))
				self.m = 1
			else:
				print("i:", int(i), "line[1]", line[1])
				#da pra otimizar o push pointer tbm, fazendo a soma aqui antes
				print(line[0], (int(i) + line[1]), sep="")
				self.file.write("".join([line[0], str(int(i) + line[1]),"\n"]))
				self.m = 0
		else:
			print(line)
			self.file.write("".join([line,"\n"]))
	def translate(self, parser):
		if parser.b == "not":
			for line in dic.dict[parser.task]:
				self.print_replace(line, 0)
		else:
			i = parser.b
			for line in dic.dict[parser.task][parser.a]:
				self.print_replace(line, i)
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

		part = line.split()
		if len(part) > 1:
			self.task = part[0]
			self.a = part[1]
			self.b = part[2]
		elif len(part) == 1:
			self.task = part[0]
			self.a = "not"
			self.b = "not"
		else:
			return("&&&")


test = parser(sys.argv[1])
x = sys.argv[1].split(".")
translator = translator("".join([x[0], ".asm"]))

while test.find_line() != "&&&":
	print(test.task, test.a, test.b)
	translator.translate(test)
	print()


#descobrir como parar de ler no final do arquivo
