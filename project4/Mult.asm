// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

	@0
	D=A
	@R2
	M=D

(LOOP)
	@R1
	D=M
	@END
	D;JLE
	@R1
	M=D-1
	@R0
	D=M
	@R2
	M=D+M
	@LOOP
	0;JMP

(END)
	@END
	0;JMP