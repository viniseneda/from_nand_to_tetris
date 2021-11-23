import sys

if len(sys.argv) != 3:
	print("use: assembler imput output")
	exit()

# first we define lists with the rules 
COMP = [["0", "0101010"],["1", "0111111"],["-1", "0111010"],["D", "0001100"],["A", "0110000"],["!D", "0001101"],["!A", "0110001"],["-D", "0001111"],["-A", "0110011"],["D+1", "0011111"],["A+1", "0110111"],["D-1", "0001110"],["A-1", "0110010"],["D+A", "0000010"],["D-A", "0010011"],["A-D", "0000111"],["D&A", "0000000"],["D|A", "0010101"],["M", "1110000"],["!M", "1110001"],["-M", "1110011"],["M+1", "1110111"],["M-1", "1110010"],["D+M", "1000010"],["D-M", "1010011"],["M-D", "1000111"],["D&M", "1000000"],["D|M", "1010101"]]

DEST = [["0", "000"],["M", "001"],["D", "010"],["MD", "011"],["A", "100"],["AM", "101"],["AD", "110"],["AMD", "111"]]

JUMP = [["0", "000"],["JGT", "001"],["JEQ", "010"],["JGE", "011"],["JLT", "100"],["JNE", "101"],["JLE", "110"],["JMP", "111"]]

SYMBOL = [["R0", 0],["R1", 1],["R2", 2],["R3", 3],["R4", 4],["R5", 5],["R6", 6],["R7", 7],["R8", 8],["R9", 9],["R10", 10],["R11", 11],["R12", 12],["R13", 13],["R14", 14],["R15", 15],["SCREEN", 16384],["KBD", 24576],["SP", 0],["LCL", 1],["ARG", 2],["THIS", 3],["THAT", 4]]



OUT = []

# convert 0 comand to binary
def convert_at(x):
	size = len(x)
	if x[1:size].isdigit():
		binary = "{0:b}".format(int(x[1:size]))
		out = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",]
		for i in range(len(binary)):
			if 15 - i > 0:
				out[15 - i] = binary[len(binary) - i - 1]
		return("".join(out))
	else:
		binary = "{0:b}".format(find(SYMBOL, x[1:size]))
		out2 = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0",]
		for i in range(len(binary)):
			if 15 - i > 0:
				out2[15 - i] = binary[len(binary) - i - 1]
		return("".join(out2))

#find binary command in the lists
def find(lista, word):
	for iten in lista:
		if word == iten[0]:
			return(iten[1])
	return("not")

#class that takes expressions, finds the binat equivalent and print command
class converter:
	def __init__(self, alu, dest, jump):
		self.alu = alu
		self.dest = dest
		self.jump = jump
	def convert(self):
		#print("111", find(COMP, self.alu), find(DEST, self.dest), find(JUMP, self.jump), sep="")
		OUT.append("".join(["111", find(COMP, self.alu), find(DEST, self.dest), find(JUMP, self.jump)]))

#first pass, to load adress labels (LABELS)
with open(sys.argv[1], 'r') as reader:
	line = reader.readline()
	counter = 0
	for line in reader:
		if line.find('//') != 0 and line.find('\n') != 0:
				x = line.split()
				if line.split() != []:
					y = x[0].split(";")
					if y[0][0] == "(":
						if find(SYMBOL, y[0][1:len(y[0]) - 1]) == "not":
							SYMBOL.append([y[0][1:len(y[0]) - 1], counter])
							counter -= 1
					counter += 1
	
#second pass, generates output and create adresses for variables
with open(sys.argv[1], 'r') as reader:
	line = reader.readline()
	counter = 16
	for line in reader:
		if line.find('//') != 0 and line.find('\n') != 0:
				x = line.split()
				if line.split() != []:
					y = x[0].split(";")
					if y[0][0] != "(":
						if y[0][0] == "@":
							if find(SYMBOL, y[0][1:len(y[0])]) == "not" and not y[0][1:len(y[0])].isdigit():
								print(counter, y[0][1:len(y[0])])
								SYMBOL.append([y[0][1:len(y[0])], counter])
								counter += 1
							#print(convert_at(y[0]))	
							OUT.append(convert_at(y[0]))
						else:
							if len(y) == 2:
								jump = y[1]
							else:
								jump = "0";
							r = y[0].split("=")
							if len(r) == 2:
								dest = r[0]
								alu = r[1]
							else:
								dest = "0"
								alu = r[0]
							sets = converter(alu, dest, jump)
							sets.convert()
#writes to file
output = open(sys.argv[2], "w")							
for line in OUT:
	output.write(line)
	output.write("\n")
output.close()

