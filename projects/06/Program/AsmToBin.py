import os
os.chdir("C:/Users/cypriend/Documents/05. Perso/NandToTetris/nand2tetris/projects/06")

def cleanline( str ): #Remove comment and space
	return (str.split("//")[0]).strip()

def createSymbolDict( addr ):
        dic = {}
        for i in range(addr):
                dic["R"+str(i)] = i
        dic["SCREEN"] = 16384
        dic["KBD"] = 24576
        dic["SP"] = 0
        dic["LCL"] = 1
        dic["ARG"] = 2
        dic["THIS"] = 3
        dic["THAT"] = 4
        return dic
        


def createJMPDict():
        dic = {}
        dic[""] = "000"
        dic["JGT"] = "001"
        dic["JEQ"] = "010"
        dic["JGE"] = "011"
        dic["JLT"] = "100"
        dic["JNE"] = "101"
        dic["JLE"] = "110"
        dic["JMP"] = "111"
        return dic
	
def createDestDict():
        dic = {}
        dic[""] = "000"
        dic["M"] = "001"
        dic["D"] = "010"
        dic["MD"] = "011"
        dic["A"] = "100"
        dic["AM"] = "101"
        dic["AD"] = "110"
        dic["AMD"] = "111"
        return dic

def createCOMPDict():
        dic = {}
        dic["0"] = "101010"
        dic["1"] = "111111"
        dic["-1"] = "111010"
        dic["D"] = "001100"
        dic["A"] = "110000"
        dic["!D"] = "001101"
        dic["!A"] = "110001"
        dic["-D"] = "001111"
        dic["-A"] = "110011"
        dic["D+1"] = "011111"
        dic["A+1"] = "110111"
        dic["D-1"] = "001110"
        dic["A-1"] = "110010"
        dic["D+A"] = "000010"
        dic["D-A"] = "010011"
        dic["A-D"] = "000111"
        dic["D&A"] = "000000"
        dic["D|A"] = "010101"
        return dic
	
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

def translate():
        filename = raw_input("Enter your path: ")
        fileasm = open( filename + "/" + filename + ".asm")
        filebin = open( filename + "/" + filename + ".hack", 'w' )
        inputList = map( cleanline, fileasm.read().split("\n") )
        nextFreeAddress = 16
        symb = createSymbolDict(nextFreeAddress)
        
        i = 0
        while( i < len(inputList) ):
                str = inputList[i]
                if ( str == "" ):
                        inputList.pop(i)
                elif ( str.startswith("(")):
                        symb[ str[1:len(str)-1] ] = i
                        inputList.pop(i)
                else:
                        i += 1
			
        dictD = createDestDict()
        dictC = createCOMPDict()
        dictJ = createJMPDict()

        outputbin = []
        for inst in inputList:
                if inst.startswith("@"):
                        A = inst[1:]
                        try:
                                addr = int(A)
                        except ValueError:
                                if( symb.has_key(A) ):
                                        addr = symb[A]
                                else:
                                        symb[A] = nextFreeAddress
                                        addr = nextFreeAddress
                                        nextFreeAddress += 1
                        binaddr = bin(addr)[2:]
                        binInstruction = "0" + "0"*(15 - len(binaddr)) + binaddr
			
                else:
                        dest, comp, jmp = sepDInst(inst)
                        a = "0"
                        i = comp.find("M")
                        if ( i != -1 ):
                                a = "1"
                                comp = comp.replace("M","A")
                        binInstruction = "111" + a + dictC[comp] + dictD[dest] + dictJ[jmp]
			
                outputbin.append(binInstruction)

        filebin.write( "\n".join(outputbin) )
        fileasm.close()
        filebin.close()
	
