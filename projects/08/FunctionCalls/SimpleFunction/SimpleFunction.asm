@256
D=A
@SP
M=D
(SimpleFunction.test)
@SP
A=M
M=0
A=A+1
M=0
A=A+1
D=A
@SP
M=D
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
@SP
AM=M-1
M=!M
@SP
M=M+1
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
@SP
A=M-1
D=M
@ARG
A=M
M=D
D=A+1
@SP
M=D
@LCL
D=M
@R13
AM=D-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R13
A=M-1
0;JMP
(EOF)
@EOF
0;JMP