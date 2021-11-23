dict = {"push" : {"constant": [
["@", 0],
"D=A",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"temp": [
"@5",
"D=A",
["@", 0],		#@i
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"pointer": [
"@3",
"D=A",
["@", 0],		#@i
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"static": [
["@static.", 0],	#@static.i
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"local": [
"@LCL",
"D=M",
["@", 0],
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"argument": [
"@ARG",
"D=M",
["@", 0],
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"this": [
"@THIS",
"D=M",
["@", 0],
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"that": [
"@THAT",
"D=M",
["@", 0],
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"]},

"pop": {"temp": [
"@SP",
"M=M-1",
"A=M",
"D=M",
["@", 5],
"M=D"],

"pointer": [
"@SP",
"M=M-1",
"A=M",
"D=M",
["@", 3],
"M=D"],

"static": [
"@SP",
"M=M-1",
"A=M",
"D=M",
["@static.", 0],
"M=D"],

"local": [
"@SP",
"M=M-1",
"@LCL",		#segment
"D=M",
["@", 0],	#i
"D=A+D",
"@13",
"M=D",
"@SP",
"A=M",
"D=M",
"@13",
"A=M",
"M=D"],

"argument": [
"@SP",
"M=M-1",
"@ARG",		#segment
"D=M",
["@", 0],	#i
"D=A+D",
"@13",
"M=D",
"@SP",
"A=M",
"D=M",
"@13",
"A=M",
"M=D"],

"that": [
"@SP",
"M=M-1",
"@THAT",		#segment
"D=M",
["@", 0],	#i
"D=A+D",
"@13",
"M=D",
"@SP",
"A=M",
"D=M",
"@13",
"A=M",
"M=D"],

"this": [
"@SP",
"M=M-1",
"@THIS",	#segment
"D=M",
["@", 0],	#i
"D=A+D",
"@13",
"M=D",
"@SP",
"A=M",
"D=M",
"@13",
"A=M",
"M=D"]},

"add": [ # Add two numbers in the stack
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"M=D+M"],

"sub": [ # subtract two numbers in the stack
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"M=M-D"],

"neg" : [
"@SP",
"D=M-1",
"A=D",
"M=-M"],

"eq" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"D=M-D",
"M=-1",
["@END", 1],
"D;JEQ",
"@SP",
"A=M-1",
"M=0",
["(END", 2]],

"gt" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"D=M-D",
"M=-1",
["@END", 1],
"D;JGT",
"@SP",
"A=M-1",
"M=0",
["(END", 2]],

"lt" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"D=M-D",
"M=-1",
["@END", 1],
"D;JLT",
"@SP",
"A=M-1",
"M=0",
["(END", 2]],

"and" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"M=D&M"],

"or" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"M=D|M"],

"not" : [
"@SP",
"D=M-1",
"A=D",
"M=!M"]}
