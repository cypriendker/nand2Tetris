// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.

@8191
D = A
@SCREEN
D = A + D
@n
M = D //n = 8191 + SCREEN

(LOOP)
@KBD
D = M
@WHITE
D;JEQ //IF KEY = 0 GOTO WHITE

(BLACK)
@SCREEN
D = A
@i
M = D // i = SCREEN

(BLACKLOOP)
@n
D=M
@i
D=M-D
@LOOP
D;JGT //If i>n GOTO LOOP

@i
A = M
M = -1
@i
M=M+1
@BLACKLOOP
0;JMP

(WHITE)
@SCREEN
D = A
@i
M = D // i = SCREEN

(WHITELOOP)
@n
D=M
@i
D=M-D
@LOOP
D;JGT //If i>n GOTO LOOP

@i
A = M
M = 0
@i
M=M+1
@WHITELOOP
0;JMP
