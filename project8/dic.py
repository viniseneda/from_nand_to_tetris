dict = {"push" : {"constant": [
["a"],
"D=A",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"temp": [
"@5",
"D=A",
["a"],		#@i
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
["a"],		#@i
"A=A+D",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"static": [
["b"],	#@static.i
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"local": [
"@LCL",
"D=M",
["a"],	#@i
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
["a"],	#@i
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
["a"],	#@i
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
["a"],	#@i
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
["c", 5],	#@parserb + line[1]
"M=D"],

"pointer": [
"@SP",
"M=M-1",
"A=M",
"D=M",
["c", 3], 	#@parserb + line[1]
"M=D"],

"static": [
"@SP",
"M=M-1",
"A=M",
"D=M",
["b"], #@static.parserb
"M=D"],

"local": [
"@SP",
"M=M-1",
"@LCL",		#segment
"D=M",
["a"],	#@i
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
["a"],	#@i
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
["a"],	#@i
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
["a"],	#@i
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
["d"], #@END + counter
"D;JEQ",
"@SP",
"A=M-1",
"M=0",
["e"]], #(END + counter)

"gt" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"D=M-D",
"M=-1",
["d"],
"D;JGT",
"@SP",
"A=M-1",
"M=0",
["e"]],

"lt" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
"A=A-1",
"D=M-D",
"M=-1",
["d"],
"D;JLT",
"@SP",
"A=M-1",
"M=0",
["e"]],

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
"M=!M"],

"label" : [
["f"]], #(parser.a)

"goto" : [
["g"], #@parser.a
"0;JMP"],

"if-goto" : [
"@SP",
"M=M-1",
"A=M",
"D=M",
["g"], #@parser.a
"D;JNE"],

"call" : [
["i"], #return (generate a return adress label)
"D=A",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1",
#push LCL, ARG, THIS and THAT
"@LCL",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1",
"@ARG",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1",
"@THIS",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1",
"@THAT",
"D=M",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1",
#set new ARG
"@SP",
"D=M",
["j", 5], #parser.b + 5
"D=D-A",
"@ARG",
"M=D",
#set LCL
"@SP",
"D=M",
"@LCL",
"M=D",
#transfer control
["g"], #function name (parser.a)
"0;JMP",
#set return adress
["h"]], #return label


#set temp variable to LCL (FRAME)
"return":[
"@LCL",
"D=M",
"@R13",
"M=D",
#set temp to return adress
"@R13",
"D=M",
"@5",
"A=D-A",
"D=M",
"@R14",
"M=D",
#pop return value to caller 
"@SP",
"M=M-1",
"A=M",
"D=M",
"@ARG",
"A=M",
"M=D",
#restore SP
"@ARG",
"D=M+1",
"@SP",
"M=D",
#restore THAT, THIS, ARG and LCL
"@R13",
"A=M-1",
"D=M",
"@THAT",
"M=D",
"@R13",
"D=M",
"@2",
"D=D-A",
"A=D",
"D=M",
"@THIS",
"M=D",
"@R13",
"D=M",
"@3",
"D=D-A",
"A=D",
"D=M",
"@ARG",
"M=D",
"@R13",
"D=M",
"@4",
"D=D-A",
"A=D",
"D=M",
"@LCL",
"M=D",
#go to return adress
"@R14",
"A=M",
"0;JMP"],

"function" : [
#["f"],
"@0",
"D=A",
"@SP",
"A=M",
"M=D",
"@SP",
"M=M+1"],

"boot" : [
"@256",
"D=A",
"@SP",
"M=D"]
}
