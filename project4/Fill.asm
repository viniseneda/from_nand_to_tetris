// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP)
	@KBD
	D=M
	@BLACKSCREEN
	D;JGT
	
(WHITESCREEN)
	@SCREEN
	D=A
	@addr
	M=D
(PAINTW)
	//if whole screen is painted leave loop
	@addr
	D=M
	@24575
	D=D-A
	@LOOP
	D;JGT

	@addr
	A=M;
	M=0
	A=A+1
	D=A
	@addr
	M=D
	@PAINTW
	0;JMP

(BLACKSCREEN)
	@SCREEN
	D=A
	@addr
	M=D
(PAINTB)
	//if whole screen is painted leave loop
	@addr
	D=M
	@24575
	D=D-A
	@LOOP
	D;JGT

	@addr
	A=M;
	M=-1
	A=A+1
	D=A
	@addr
	M=D
	@PAINTB
	0;JMP
