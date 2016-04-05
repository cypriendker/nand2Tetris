import glob, os
os.chdir("C:/Users/cypriend/Documents/05. Perso/NandToTetris/nand2tetris/projects/08/FunctionCalls")

C_PUSH = "push"
C_POP = "pop"
C_LABEL = "label"
C_IF = "if-goto"
C_GOTO = "goto"
C_CALL = "call"
C_FUNC = "function"
C_RETURN = "return"

memSeg = {}
memSeg["local"] = "LCL"
memSeg["argument"] = "ARG"
memSeg["this"] = "THIS"
memSeg["that"] = "THAT"

nbArg = {}
nbArg["add"] = 2
nbArg["sub"] = 2
nbArg["neg"] = 1
nbArg["eq"] = 2
nbArg["gt"] = 2
nbArg["lt"] = 2
nbArg["and"] = 2
nbArg["or"] = 2
nbArg["not"] = 1

countT = 0

filename = ""
currentfunction = "null"

def cleanline( str ): #Remove comment and space
	return (str.split("//")[0]).strip()


	
def sepDInst(inst):
        eq = inst.find("=")
        jmp = inst.find(";")
        
        if jmp == -1:
                jmp = len(inst)
        J = inst[jmp+1:]
	
        if eq == -1:
                D = ""
        else:
                D = inst[:eq]
        C = inst[eq+1:jmp]
	
        return D,C,J

def writePushPop( cmd, seg, ind ):
    output = []

    #Go to address
    if seg == "pointer":
        if ind == "0":
            output.append("@THIS")
        elif ind == "1":
            output.append("@THAT")
    elif seg != "constant":
        output.append("@"+ind)
        output.append("D=A")
        if seg == "temp":
            output.append("@5")
            output.append("A=A+D")
        elif seg == "static":
            output.append("@" + filename + "." + ind)
        else :
            output.append("@" + memSeg[seg] )
            output.append("A=M+D")

    #For the push
    if cmd == C_PUSH:
        if seg == "constant": #Store index in D
            output.append("@"+ind)
            output.append("D=A")
        else:#Store Value in D
            output.append("D=M")

        #Get top of the stack and push
        output.append("@SP")
        output.append("A=M")
        output.append("M=D")

        #Increment the stack
        output.append("@SP")
        output.append("M=M+1")

    elif cmd == C_POP:
        #No constant so directly store the address in R13
        output.append("D=A")
        output.append("@R13")
        output.append("M=D")

        #Get the top of the stack value
        output.append("@SP")
        output.append("A=M-1")
        output.append("D=M")

        #Push the value
        output.append("@R13")
        output.append("A=M")
        output.append("M=D")

        #Increment the stack
        output.append("@SP")
        output.append("M=M-1")    
           
    return output

def writeArithmetic( cmd ):
    global countT    
    output = []
    output.append("@SP")
    output.append("AM=M-1")

    if nbArg[cmd] == 1:
        if cmd == "neg":
            output.append("M=-M")
        elif cmd == "not":
            output.append("M=!M")

    elif nbArg[cmd] == 2:
        output.append("D=M")
        output.append("@SP")
        output.append("AM=M-1")

        if cmd == "add":
            output.append("M=M+D")
        elif cmd == "sub":
            output.append("M=M-D")
        elif cmd == "and":
            output.append("M=D&M")
        elif cmd == "or":
            output.append("M=D|M")
        else:
            countT+=1
            output.append("D=M-D")
            output.append("@TRUE"+str(countT) )
            if cmd == "eq":
                output.append("D;JEQ")
            elif cmd == "gt":
                output.append("D;JGT")
            elif cmd == "lt":
                output.append("D;JLT")

            output.append("@SP")
            output.append("A=M")
            output.append("M=0")
            output.append("@END"+str(countT) )
            output.append("0;JMP")
            output.append("(TRUE"+str(countT)+")")
            output.append("@SP")
            output.append("A=M")
            output.append("M=-1")
            output.append("(END"+str(countT)+")")

    output.append("@SP")
    output.append("M=M+1")        

    return output

def writeInit():
        output = []
        output.append("@256")
        output.append("D=A")
        output.append("@SP")
        output.append("M=D")
        output = output + writeCall("Sys.init", 0)
        output.append("(EOF)")
        output.append("@EOF")
        output.append("0;JMP")
        return output


def writeLabel( lbl ):
        output = []
        output.append("(" + currentfunction + "$" + lbl + ")")
        return output

def writeGoto( lbl ):
        output = []
        output.append("@" + currentfunction + "$" + lbl)
        output.append("0;JMP")
        return output

def writeIf ( lbl ):
        output = ["@SP"]
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@" + currentfunction + "$" + lbl)
        output.append("D;JNE")
        return output

def writeCall( func, nArg ):
        global countT
        output = []
        #Get returnAddress
        output.append("@RETURN"+func+str( countT ))
        output.append("D=A")
        #Push to stack
        output.append("@SP")
        output.append("A=M")
        output.append("M=D")
        #Get LCL address
        output.append("@LCL")
        output.append("D=M")
        #Push to stack
        output.append("@SP")
        output.append("AM=M+1")
        output.append("M=D")
        #Get Arg address
        output.append("@ARG")
        output.append("D=M")
        #Push to stack
        output.append("@SP")
        output.append("AM=M+1")
        output.append("M=D")
        #Get This address
        output.append("@THIS")
        output.append("D=M")
        #Push to stack
        output.append("@SP")
        output.append("AM=M+1")
        output.append("M=D")
        #Get That adress
        output.append("@THAT")
        output.append("M=D")
        #Push to stack
        output.append("@SP")
        output.append("AM=M+1")
        output.append("M=D")
        output.append("@SP")
        output.append("M=M+1")

        #Calc ARG
        output.append("D=M")
        output.append("@"+str(nArg) )
        output.append("D=D-A")
        output.append("@5")
        output.append("D=D-A")
        output.append("@ARG")
        output.append("M=D")

        #Calc LCL
        output.append("@SP")
        output.append("D=M")
        output.append("@LCL")
        output.append("M=D")

        #Goto g
        output.append("@"+func)
        output.append("0;JMP")

        #Return address
        output.append("(RETURN"+func+str(countT)+")")
        countT += 1
        return output

def writeFunction( func, nVars ):
        global currentfunction
        currentfonction = func
        output = []
        output.append("("+func+")")
        output.append("@SP")
        output.append("A=M")
        for i in range(nVars):
                output.append("M=0")
                output.append("A=A+1")
        output.append("D=A")
        output.append("@SP")
        output.append("M=D")

        return output

def writeReturn():
        output = []

        # R14= Return address
        output.append("@5")
        output.append("D=A")
        output.append("@LCL")
        output.append("A=M-D")
        output.append("D=M")
        output.append("@R14")
        output.append("M=D")

        # *ARg = pop()
        output.append("@SP")
        output.append("A=M-1")
        output.append("D=M")
        output.append("@ARG")
        output.append("A=M")
        output.append("M=D")

        #SP = Arg+1
        output.append("D=A+1")
        output.append("@SP")
        output.append("M=D")

        #Store (LCL-1) in R13
        output.append("@LCL")
        output.append("D=M")
        output.append("@R13")
        output.append("AM=D-1")

        #THAT = R13 = LCL-1
        output.append("D=M")
        output.append("@THAT")
        output.append("M=D")

        #THIS = R13 = LCL-2
        output.append("@R13")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@THIS")
        output.append("M=D")
        
        #ARG = R13 = LCL-3
        output.append("@R13")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@ARG")
        output.append("M=D")

        #LCL = R13 = LCL-4
        output.append("@R13")
        output.append("AM=M-1")
        output.append("D=M")
        output.append("@LCL")
        output.append("M=D")
        
        #Goto R14 = LCL-5
        output.append("@R14")
        output.append("A=M")
        output.append("0;JMP")

        return output
        


def readCleanFile( file ):
        inputList = file.read().split("\n")

        i = 0
        while( i < len(inputList) ):
                str = inputList[i]
                if ( str == "" or str.startswith("//") ):
                        inputList.pop(i)
                else:
                        inputList[i] = cleanline(str)
                        i += 1
        return inputList

def vmToAsm( input, outputcmd ):
        for line in input:
                cmdlist = line.split(" ")
                cmd = cmdlist[0]
                if cmd == C_PUSH or cmd == C_POP:
                        outputcmd = outputcmd + writePushPop(cmd, cmdlist[1], cmdlist[2])
                elif cmd == C_LABEL:
                        outputcmd = outputcmd + writeLabel(cmdlist[1])
                elif cmd == C_GOTO:
                        outputcmd = outputcmd + writeGoto( cmdlist[1])
                elif cmd == C_IF:
                        outputcmd = outputcmd + writeIf(cmdlist[1])
                elif cmd == C_CALL:
                        outputcmd = outputcmd + writeCall(cmdlist[1], int(cmdlist[2]))
                elif cmd == C_FUNC:
                        outputcmd = outputcmd + writeFunction(cmdlist[1], int(cmdlist[2]))
                elif cmd == C_RETURN:
                        outputcmd = outputcmd + writeReturn()
                else :
                        outputcmd = outputcmd + writeArithmetic(cmd)
        return outputcmd
                        

def translate():
        global filename
        filesdir = raw_input("Enter your path: ")
        fileasm = open( filesdir + "/" + filesdir + ".asm", 'w' )

        outputcmd = []
        outputcmd = outputcmd + writeInit()
        
        for file in os.listdir("./"+filesdir):
                if file.endswith(".vm"):
                      filevm = open( filesdir + "/" + file )
                      filename = file[:-3]
                      print "translating " + file
                      inputList = readCleanFile( filevm )
                      outputcmd = vmToAsm( inputList, outputcmd )
                      filevm.close()

        
        fileasm.write( "\n".join(outputcmd) )
        fileasm.close()


	        
