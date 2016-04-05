// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R0
D = M
@R1
D = D-M
@JUMP1
D; JGT //If R0>R1 GOTO JUMP1

@R0
D=M
@term1
M=D //term1 = R0

@R1
D=M
@term2
M=D //term2 = R1

@JUMP2
D;JMP // GOTO JUMP2

(JUMP1)
@R1
D=M
@term1
M=D //term1 = R1

@R0
D=M
@term2
M=D //term2 = R0

(JUMP2)
@0
D = A 
@R2
M = D //R2 = 0
@i
M = D //i = 0

@term1
D = M
@END
D; JEQ //if term1 = 0 Goto end


(LOOP)
@term2
D = M
@R2
M = M+D //R2 = R2 + term2

@i
M=M+1 //i++

D=M
@term1
D=M-D
@LOOP
D;JGT //If i<n GOTO Loop

(END)
@END
0;JMP //Infinite  loop
