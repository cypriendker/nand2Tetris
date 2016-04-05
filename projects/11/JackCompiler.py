import os
from collections import deque
os.chdir("C:/Users/cypriend/Documents/05. Perso/NandToTetris/nand2tetris/projects/11")

symboleDic = {}
symboleDic["{"] = "bracket"
symboleDic["}"] = "bracket"
symboleDic["("] = "bracket"
symboleDic[")"] = "bracket"
symboleDic["["] = "bracket"
symboleDic["]"] = "bracket"
symboleDic["."] = "separator"
symboleDic[","] = "separator"
symboleDic[";"] = "separator"
symboleDic["+"] = "op"
symboleDic["-"] = "unaryop"
symboleDic["*"] = "op"
symboleDic["/"] = "op"
symboleDic["&"] = "op"
symboleDic["|"] = "op"
symboleDic["<"] = "op"
symboleDic[">"] = "op"
symboleDic["="] = "op"
symboleDic["~"] = "unaryop"

keywordDic = {}
keywordDic["class"] = "class"
keywordDic["constructor"] = "subroutineDec"
keywordDic["function"] = "subroutineDec"
keywordDic["method"] = "subroutineDec"
keywordDic["field"] = "classVarDec"
keywordDic["static"] = "classVarDec"
keywordDic["var"] = "varDec"
keywordDic["int"] = "type"
keywordDic["char"] = "type"
keywordDic["boolean"] = "type"
keywordDic["void"] = "voidtype"
keywordDic["true"] = "KeywordConstant"
keywordDic["false"] = "KeywordConstant"
keywordDic["null"] = "KeywordConstant"
keywordDic["this"] = "KeywordConstant"
keywordDic["let"] = "statement"
keywordDic["do"] = "statement"
keywordDic["if"] = "statement"
keywordDic["else"] = "statement"
keywordDic["while"] = "statement"
keywordDic["return"] = "statement"

opDic = {}
opDic["+"] = "add"
opDic["-"] = "sub"
opDic["*"] = "call Math.multiply 2"
opDic["/"] = "call Math.divide 2"
opDic["&"] = "and"
opDic["|"] = "or"
opDic["<"] = "lt"
opDic[">"] = "gt"
opDic["="] = "eq"

unopDic = {}
unopDic["-"] = "neg"
unopDic["~"] = "not"

identifier = "identifier"
intconst = "integerConstant"
strconst = "stringConstant"
keyword = "keyword"
symbol = "symbol"

xmlDic = {}
xmlDic["<"] = "&lt;"
xmlDic[">"] = "&gt;"
xmlDic["\""] = "&quot;"
xmlDic["&"] = "&amp;"

static = "static"
field = "field"
arg = "argument"
var = "local"
pointer = "pointer"
that = "that"
this = "this"
constant = "constant"
temp = "temp"

class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def intVal(self):
        if self.type == intconst:
            return int(self.value)

    def stringVal(self):
        if self.type == strconst:
            return self.value[1:-1]

    def getVal( self):
        if self.type == strconst:
            return self.value[1:-1]
        return self.value

    def getXmlVal( self ):
        try:
            return xmlDic[self.value]
        except:
            return self.getVal()

    def getType( self ):
        return self.type

    def toString( self ):
        print self.value

    def getKeyType( self ):
        return keywordDic[self.value]

    def isType( self, withvoid):
        out = False
        try:
            out = (self.getKeyType() == "type" or (withvoid and self.getKeyType() == "voidtype" ) )
        except:
            out = ( self.type  == identifier )
        return out

    def isOp(self):
        if (self.value == "-" ):
            return True
        try:
            return symboleDic[self.value] == "op"
        except:
            return False

    def isUnaryOp(self):
        try:
            return symboleDic[self.value] == "unaryop"
        except:
            return False
            
        
class SymbolDef:
    def __init__( self, type, kind, i ):
        self.type = type
        self.kind = kind
        self.index = i

    def getType(self):
        return self.type

    def getKind( self ):
        return self.kind

    def getInd( self ):
        return self.index

class SymbolTable:
    def __init__( self ):
        self.classTable = {}
        self.subroutineTable = {}
        self.indexes ={}
        self.indexes[static] = 0
        self.indexes[field] = 0
        self.indexes[var] = 0
        self.indexes[arg] = 0

    def startSubroutine( self):
        self.subroutineTable.clear()
        self.indexes[var] = 0
        self.indexes[arg] = 0

    def Define( self, name, type, kind ):
        if ( not self.indexes.has_key( name ) ):
            ind = self.VarCount( kind )
            self.indexes[ kind ] = ind + 1
            if ( kind == static or kind == field ):
                self.classTable[ name ] = SymbolDef( type, kind, ind )
            elif ( kind == var or kind == arg ):
                self.subroutineTable[ name ] = SymbolDef( type, kind, ind )
        else:
            raise Exception( name + " is already defined in the Symbole table " )

    def VarCount( self, kind ):
        try:
            return self.indexes[ kind ]
        except:
            raise Exception( "Unknown kind : " + kind )

    def TypeOf( self, name ):
        if self.subroutineTable.has_key( name ):
            return self.subroutineTable[name].getType()
        elif self.classTable.has_key( name ):
            return self.classTable[name].getType()
        else:
            return "None"

    def KindOf( self, name ):
        if self.subroutineTable.has_key( name ):
            return self.subroutineTable[name].getKind()
        elif self.classTable.has_key( name ):
            return self.classTable[name].getKind()
        else:
            return "None"
        
    def IndOf( self, name ):
        if self.subroutineTable.has_key( name ):
            return self.subroutineTable[name].getInd()
        elif self.classTable.has_key( name ):
            return self.classTable[name].getInd()
        else:
            return "None"

class VMWriter:
    def __init__(self ):
        self.output = []

    def writePush(self, segment, index ):
        self.output.append("push " + segment + " " + str(index) )

    def writePop(self, segment, index ):
        self.output.append("pop " + segment + " " + str(index) )

    def writeArithmetic(self, cmd ):
        self.output.append( cmd )

    def writeLabel(self, label ):
        self.output.append("label " + label )
        
    def writeGoto(self, label ):
        self.output.append("goto " + label)

    def writeIf(self, label ):
        self.output.append("if-goto " + label )

    def writeCall(self, name, nArgs ):
        self.output.append("call " + name + " " + str(nArgs) )

    def writeFunction(self, name, nLocals ):
        self.output.append("function " + name + " " + str(nLocals) )

    def writeReturn(self):
        self.output.append("return" )

    def writeToFile( self, file ):
        file.write( "\n".join(self.output) )

def passComment( inputfile, i_i, n):
    i = i_i
    if ( i < n-1 ):
        startComm = inputfile[i:i+2]
        if ( startComm == "/*" ):
            endComm = "*/"
            while ( i < n-1 ):
                if endComm == inputfile[i:i+2]:
                    return i+2
                else:
                    i = i+1
        elif ( startComm == "//"):
            endComm ="\n"
            i = i+1
            while ( i < n ):
                if endComm == inputfile[i]:
                    return i+1
                else:
                    i = i+1
    return i

def jackTokenizer( inputfile ):
    i = 0;
    n = len(inputfile)
    tokenlist = deque()

    currentToken = ""
    while( i < n):
        current_sym = inputfile[i]
        if current_sym == "/":
            i_new = passComment( inputfile, i, n )
            if ( i == i_new ):
                tokenlist.append( Token( "/", symbol ) )
                i = i+1
            else:
                i = i_new
        elif symboleDic.has_key( inputfile[i] ):
            tokenlist.append( Token( inputfile[i], symbol ) )
            i = i+1

        elif current_sym == "\n":
            i = i+1

        elif current_sym == " " or current_sym == "\t":
            i = i+1

        elif current_sym == "\"":
            currentToken = current_sym
            i = i+1
            while ( i < n ):
                sym = inputfile[i]
                if sym == "\n":
                    print ("Synthax Error : unexpected new line in StringIndentifier : " + currentToken )
                    raise
                elif sym == "\"":
                    currentToken = currentToken + sym
                    i = i+1
                    break
                else:
                    currentToken = currentToken + sym
                    i = i+1
            if sym != "\"":
                print ("Synthax Error : unexpected end of StringIndentifier : " + currentToken )
                raise
            tokenlist.append( Token(currentToken, strconst ) )
                
        else:
            currentToken = inputfile[i]
            i = i+1
            while( i<n ):
                sym = inputfile[i]
                if (sym == " " or symboleDic.has_key( sym )):
                    break
                else:
                    currentToken = currentToken + sym
                    i = i+1
            if ( keywordDic.has_key( currentToken ) ):
                type = keyword
            else:
                try:
                    int( currentToken )
                    type = intconst
                except ValueError:
                    type = identifier
                except:
                    print "unexpected error upon converting " + currentToken + "to int"

            tokenlist.append( Token( currentToken, type ) )
    return tokenlist


############### Check Synthax Error #######################
def checkType(expectedtype, token):
    type = token.getType()
    if (type != expectedtype ):
        print "Unexpected token receive : expected type " + expectedtype + "but get" + type
        raise

def checkValue(expectedvalue, token):
    value = token.getVal()
    if (value != expectedvalue ):
        print "Unexpected token receive : expected value " + expectedvalue + "but get" + value
        raise

def checkIsKeyType( token, withvoid ):
    if ( not token.isType( withvoid ) ):
        print "Unexpected token receive : expected a type but got " + token.getVal()
        raise

def checkIsKeyStat( token):
    if token.getType() == keyword:
        return token.getKeyType() == "statement"
    return False

def checkIsKeyConst( token):
    if ( token.getKeyType() != "KeywordConstant" ):
        print "Unexpected keyword : expected type KeywordConstant but got " + token.getKeyType() + " for token :" + token.getVal()
        raise

################## Write in xml methods ##################
def openLabel(xml, label, nbtab):
    newline = "\t"*nbtab + "<"+label+">"
    #print newline
    xml.append( newline )
    

def closeLabel(xml, label, nbtab):
    newline = "\t"*nbtab + "</"+label+">"
    #print newline
    xml.append( newline )

def writeTerminal(xml, token, nbtab):
    label = token.getType()
    newline = "\t"*nbtab + "<"+label+">"+token.getXmlVal()+"</"+label+">" 
    #print newline
    xml.append( newline )

################## Compile Class Method ###################

def CompileClass( tokenQueue, nbtab, xml ):
    global className
    
    token = tokenQueue.popleft()
    openLabel( xml, "class" , nbtab )
    writeTerminal( xml, token , nbtab+1 )
    
    t = tokenQueue.popleft()
    checkType( identifier, t )
    #Xml
    writeTerminal( xml,t, nbtab+1)
    #Compiler
    className = t.getVal()


    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1)

    t = tokenQueue[0]
    while( t.getVal() != "}" ):
        keytype = t.getKeyType()
        if ( keytype == "subroutineDec" ):
            CompileSubroutine( tokenQueue, nbtab+1, xml )
        elif (keytype == "classVarDec" ):
            CompileClassVarDec( tokenQueue, nbtab+1, xml )
        else :
            print "Unexpected token keyword type : expected classVarDec or subroutineDec but got " + keytype
            raise
        t = tokenQueue[0]

    t = tokenQueue.popleft()
    checkValue( "}", t )
    writeTerminal( xml, t, nbtab+1)
    closeLabel( xml, "class" , nbtab )

################## Compile ClassVarDec Method ###################

def CompileClassVarDec( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "classVarDec" , nbtab )

    t = tokenQueue.popleft()
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    kind = t.getVal()    

    t = tokenQueue.popleft()
    checkIsKeyType( t, False )
    #Xml
    writeTerminal( xml, t, nbtab + 1 )
    #Compiler
    type = t.getVal()

    t = tokenQueue.popleft()
    checkType( identifier, t )
    #Xml
    writeTerminal( xml, t, nbtab+1)
    #Compiler
    name = t.getVal()
    symTable.Define( name, type, kind )

    t = tokenQueue[0]
    while( t.getVal() == "," ):
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1)

        t = tokenQueue.popleft()
        checkType( identifier, t )
        #Xml
        writeTerminal( xml, t, nbtab+1)
        #Compiler
        name = t.getVal()
        symTable.Define( name, type, kind )

        t = tokenQueue[0]

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1)
    closeLabel( xml, "classVarDec" , nbtab )

################## Compile Subroutine Method ###################

def CompileSubroutine(tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "subroutineDec" , nbtab )

    #Compiler
    symTable.startSubroutine()

    t = tokenQueue.popleft()
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    subroutinetype = t.getVal()
    if subroutinetype == "method":
        symTable.Define( "this", className, arg )

    
    t = tokenQueue.popleft()
    checkIsKeyType( t, True )
    writeTerminal( xml, t, nbtab + 1 )

    t = tokenQueue.popleft()
    checkType( identifier, t )
    #Xml    
    writeTerminal( xml, t, nbtab+1)
    #Compiler
    routName = t.getVal()

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileParameterList( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileSubroutineBody( tokenQueue, nbtab+1, xml, routName, subroutinetype )
    
    closeLabel( xml, "subroutineDec" , nbtab )

################## Compile ParemetersList Method ###################

def CompileParameterList( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "parameterList" , nbtab )
    t = tokenQueue[0]
    if t.isType( False ):
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1)
        #Compiler
        type = t.getVal()

        t = tokenQueue.popleft()
        checkType( identifier, t )
        #Xml
        writeTerminal( xml, t, nbtab+1)
        #Compiler
        name = t.getVal()
        symTable.Define( name, type, arg )

        while ( tokenQueue[0].getVal() == "," ):
            t = tokenQueue.popleft()
            #Xml
            writeTerminal( xml, t, nbtab+1)

            t = tokenQueue.popleft()
            checkIsKeyType( t, False )
            #Xml
            writeTerminal( xml, t, nbtab+1)
            #Compiler
            type = t.getVal()

            t = tokenQueue.popleft()
            checkType( identifier, t )
            #Xml
            writeTerminal( xml, t, nbtab+1)
            #Compiler
            name = t.getVal()
            symTable.Define( name, type, arg )
            
    closeLabel( xml, "parameterList" , nbtab )


################## Compile SubRoutineBody Method ###################

def CompileSubroutineBody( tokenQueue, nbtab, xml, routineName, routineType ): #Compiler OK
    openLabel( xml, "subroutineBody" , nbtab )

    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1 )

    while ( tokenQueue[0].getVal() == "var" ):
        CompileVarDec( tokenQueue, nbtab +1 , xml)

    #Compiler
    nbVars = symTable.VarCount( var )
    vmWriter.writeFunction( className + "." + routineName, nbVars )
    if routineType == "constructor":
        vmWriter.writePush( constant, symTable.VarCount( field ) )
        vmWriter.writeCall( "Memory.alloc", 1 )
        vmWriter.writePop( pointer, 0 )
    elif routineType == "method":
        vmWriter.writePush( arg, 0 )
        vmWriter.writePop( pointer, 0 )

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "subroutineBody" , nbtab )

################## Compile VarDec Method ###################

def CompileVarDec( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "varDec" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )
    
    t = tokenQueue.popleft()
    checkIsKeyType( t, False )
    #Xml
    writeTerminal( xml, t, nbtab+1)
    #Compiler
    type = t.getVal()
    
    t = tokenQueue.popleft()
    checkType( identifier, t )
    #Xml
    writeTerminal( xml, t, nbtab+1)
    #Compiler
    symTable.Define( t.getVal(), type, var )

    while ( tokenQueue[0].getVal() == "," ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1)
            
        t = tokenQueue.popleft()
        checkType( identifier, t )
        #Xml
        writeTerminal( xml, t, nbtab+1)
        #Compiler
        symTable.Define( t.getVal(), type, var )

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )

    #Xml
    closeLabel( xml, "varDec" , nbtab )


################## Compile Statements Method ###################

def CompileStatements( tokenQueue, nbtab, xml ): #No COmpiler code
    openLabel( xml, "statements" , nbtab )

    t = tokenQueue[0]
    while( checkIsKeyStat( t ) ):
        val = t.getVal()
        if ( val == "let" ):
            CompileLetStatement( tokenQueue, nbtab+1, xml)
        elif ( val == "if" ):
            CompileIfStatement( tokenQueue, nbtab+1, xml)
        elif ( val == "while" ):
            CompileWhileStatement( tokenQueue, nbtab+1, xml)
        elif ( val == "do" ):
            CompileDoStatement( tokenQueue, nbtab+1, xml)
        elif ( val == "return" ):
            CompileReturnStatement( tokenQueue, nbtab+1, xml)
        t = tokenQueue[0]
            
    closeLabel( xml, "statements" , nbtab )

################## Compile LetStatement Method ###################

def CompileLetStatement( tokenQueue, nbtab, xml ): #COMPILER OK
    openLabel( xml, "letStatement" , nbtab )

    t = tokenQueue.popleft() #LET
    writeTerminal( xml, t, nbtab+1 )
    
    t = tokenQueue.popleft() #Destination
    checkType( identifier, t )
    #Xml
    writeTerminal( xml, t, nbtab+1)
    #Compiler
    varName = t.getVal()

    if( tokenQueue[0].getVal() == "[" ):#Array
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1 )
        #Compiler
        kind = symTable.KindOf( varName )
        ind = symTable.IndOf( varName )
                
        CompileExpression( tokenQueue, nbtab+1, xml )
        vmWriter.writePush( kind, ind )
        
        t = tokenQueue.popleft()
        checkValue( "]", t )
        #Xml
        writeTerminal( xml, t, nbtab+1 )
        #Compiler
        vmWriter.writeArithmetic( "add" )
        #vmWriter.writePop( pointer, 1 )
        destKind = that
        destInd = 0
        
    #Compiler
    else:
        destKind = symTable.KindOf( varName )
        destInd = symTable.IndOf( varName )

    if destKind == field: #Object attribute
        destKind = this

    t = tokenQueue.popleft()
    checkValue( "=", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )
    #Compiler
    if destKind == that:
        vmWriter.writePop( temp, 0 )
        vmWriter.writePop( pointer, 1 )
        vmWriter.writePush( temp, 0 )

    vmWriter.writePop( destKind, destInd )

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )    
    
    closeLabel( xml, "letStatement" , nbtab )

################## Compile IfStatement Method ###################

def CompileIfStatement( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "ifStatement" , nbtab )
    global nbLabelIf
    labelTrue = "IF_TRUE" + str(nbLabelIf)
    labelFalse = "IF_FALSE" + str(nbLabelIf)
    labelEnd = "IF_END" + str(nbLabelIf)
    nbLabelIf += 1

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeIf( labelTrue )
    vmWriter.writeGoto( labelFalse )
    

    t = tokenQueue.popleft()
    checkValue( "{", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeLabel( labelTrue )

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeGoto( labelEnd )
    vmWriter.writeLabel( labelFalse )
    

    if (tokenQueue[0].getVal() == "else" ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1 )

        t = tokenQueue.popleft()
        checkValue( "{", t )
        writeTerminal( xml, t, nbtab+1 )

        CompileStatements( tokenQueue, nbtab+1, xml )

        t = tokenQueue.popleft()
        checkValue( "}", t )
        writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeLabel( labelEnd )

    closeLabel( xml, "ifStatement" , nbtab )

################## Compile WhileStatement Method ###################

def CompileWhileStatement( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "whileStatement" , nbtab )
    global nbLabelWhile
    labelExp = "WHILE_EXP"+ str(nbLabelWhile)
    labelEnd = "WHILE_END" + str(nbLabelWhile)
    nbLabelWhile +=1

    t = tokenQueue.popleft()
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeLabel( labelExp )

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeArithmetic( "not" )
    vmWriter.writeIf( labelEnd )

    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeGoto( labelExp )
    vmWriter.writeLabel( labelEnd )

    closeLabel( xml, "whileStatement" , nbtab )

################## Compile doStatement Method ###################

def CompileDoStatement( tokenQueue, nbtab, xml ): #COMPILER OK
    openLabel( xml, "doStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    CompileSubroutineCall( tokenQueue, nbtab+1, xml)

    t = tokenQueue.popleft()
    checkValue( ";", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writePop( temp, 0 )

    closeLabel( xml, "doStatement" , nbtab )

################## Compile returnStatement Method ###################

def CompileReturnStatement( tokenQueue, nbtab, xml ): #COMPILER OK
    openLabel( xml, "returnStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    if( tokenQueue[0].getVal() != ";" ):
        CompileExpression( tokenQueue, nbtab+1, xml)
    else: #Compile
        vmWriter.writePush( constant, 0 )

    t = tokenQueue.popleft()
    checkValue( ";", t )
    #Xml
    writeTerminal( xml, t, nbtab+1 )
    #Compiler
    vmWriter.writeReturn()

    closeLabel( xml, "returnStatement" , nbtab )

################## Compile Expression Method ###################

def CompileExpression( tokenQueue, nbtab, xml ): #COMPILER OK
    openLabel( xml, "expression" , nbtab )

    CompileTerm( tokenQueue, nbtab +1, xml)

    while( tokenQueue[0].isOp() ):
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1 )
        #Compiler
        op = t.getVal()

        CompileTerm( tokenQueue, nbtab +1, xml)

        #Compiler
        vmWriter.writeArithmetic( opDic[op] )

    closeLabel( xml, "expression" , nbtab )


################## Compile Term Method ###################

def CompileTerm( tokenQueue, nbtab, xml ): #Compiler OK
    openLabel( xml, "term" , nbtab )

    type = tokenQueue[0].getType()
    if ( type == intconst): #Int OK
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1 )
        #Compiler
        vmWriter.writePush(constant, int( t.getVal() ) )
    elif (type == strconst ): #String
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab+1 )
        #Compiler
        string = t.getVal()
        length = len(string)
        vmWriter.writePush( constant, length )
        vmWriter.writeCall( "String.new", 1 )
        for c in string:
            vmWriter.writePush( constant, ord(c) )
            vmWriter.writeCall( "String.appendChar", 2 )
    elif ( type == keyword ): #Keyword OK
        t = tokenQueue.popleft()
        checkIsKeyConst( t )
        #Xml
        writeTerminal( xml, t, nbtab+1)
        #Compiler
        key = t.getVal()
        if key == "true":
            vmWriter.writePush( constant, 1)
            vmWriter.writeArithmetic( "neg" )
        elif key == "this":
            vmWriter.writePush( pointer, 0 )
        else:
            vmWriter.writePush( constant, 0)
    elif ( type == symbol ): 
        t = tokenQueue.popleft()
        if ( t.isUnaryOp() ): #unaryop OK
            #Xml
            writeTerminal( xml, t, nbtab+1)
            #Compiler
            cmd = unopDic[t.getVal()]
            
            CompileTerm( tokenQueue, nbtab +1 , xml )
            #Compiler
            vmWriter.writeArithmetic( cmd )
        else: # expression OK
            checkValue( "(", t )
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab +1, xml )

            t = tokenQueue.popleft()
            checkValue( ")", t )
            writeTerminal( xml, t, nbtab+1 )
    else :
        nextTokenVal = tokenQueue[1].getVal()
        if nextTokenVal == "(" or nextTokenVal == ".": #subroutine OK
            CompileSubroutineCall( tokenQueue, nbtab +1, xml)
        elif nextTokenVal == "[": #Array OK
            t = tokenQueue.popleft()
            #Xml
            writeTerminal( xml, t, nbtab+1 )
            #Compiler
            name = t.getVal()
            ind = symTable.IndOf(name)
            kind = symTable.KindOf( name )
            
            t = tokenQueue.popleft()
            #Xml
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab +1, xml)
            #Compiler
            if kind != field:
                vmWriter.writePush( kind, ind )
            else:
                vmWriter.writePush( constant, ind )
                vmWriter.writePush( pointer, 0 )
                vmWriter.writeArithmetic( "add" )
                vmWriter.writePop( pointer, 1 )
                vmWriter.writePush( that, 0 )
            vmWriter.writeArithmetic("add")
            vmWriter.writePop( pointer, 1 )
            vmWriter.writePush( that, 0 )

            t = tokenQueue.popleft()
            checkValue( "]", t )
            writeTerminal( xml, t, nbtab+1 )            
        else:#varName OK
            t = tokenQueue.popleft()
            #Xml
            writeTerminal( xml, t, nbtab+1 )
            #Compiler
            name = t.getVal()
            ind = symTable.IndOf(name)
            kind = symTable.KindOf( name )
            if kind != field:
                vmWriter.writePush( kind, ind )
            else:
                vmWriter.writePush( this, ind )

    closeLabel( xml, "term" , nbtab )

################## Compile subroutinCall Method ###################

def CompileSubroutineCall( tokenQueue, nbtab, xml ): #Compiler OK
    #openLabel( xml, "subroutineCall" , nbtab )
    #Compiler
    nbArgs = 0

    t = tokenQueue.popleft()
    #Xml
    writeTerminal( xml, t, nbtab )
    #Compiler
    caller = t.getVal()

    if tokenQueue[0].getVal() == ".":
        t = tokenQueue.popleft()
        #Xml
        writeTerminal( xml, t, nbtab )
        #Compiler
        if symTable.KindOf( caller ) != "None":
            funcName = symTable.TypeOf( caller )
            kind = symTable.KindOf( caller )
            ind = symTable.IndOf( caller )
            if kind != field:
                vmWriter.writePush( kind, ind )
            else:
                vmWriter.writePush( this, ind )
            nbArgs += 1
        else:
            funcName = caller
        
        t = tokenQueue.popleft()
        checkType( identifier, t )
        #Xml
        writeTerminal( xml, t, nbtab)
        #Compiler
        funcName = funcName + "." + t.getVal()
    else: #Compiler
        funcName = className + "." + caller
        vmWriter.writePush( pointer, 0 )
        nbArgs += 1
        
    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab )

    nbArgs += CompileExpressionList( tokenQueue, nbtab, xml)

    t = tokenQueue.popleft()
    checkValue( ")", t )
    #Xml
    writeTerminal( xml, t, nbtab )
    #Compiler
    vmWriter.writeCall( funcName, nbArgs )
    
    #closeLabel( xml, "subroutineCall" , nbtab )

################## Compile ExpressionList Method ###################

def CompileExpressionList( tokenQueue, nbtab, xml ): #No Compiler Needed
    openLabel( xml, "expressionList" , nbtab )
    nbExpr = 0

    if tokenQueue[0].getVal() != ")":
        CompileExpression( tokenQueue, nbtab+1, xml)
        nbExpr += 1
        while tokenQueue[0].getVal() == ",":
            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab+1, xml)
            nbExpr += 1
    
    closeLabel( xml, "expressionList" , nbtab )
    return nbExpr

def CompilationEngine( tokenQueue ):
    xml = []
    CompileClass( tokenQueue, 0, xml )
    return xml
    
######################## Main function #############################

filesdir = raw_input("Enter your path: ")
#fileJack = open( filesdir + "/Main.jack")
#filexml = open(filesdir + "/MainO.xml", "w")
#inputfile = fileJack.read()
#tokenizedlist = jackTokenizer( inputfile )
#xml = CompilationEngine( tokenizedlist )
#filexml.write("\n".join(xml))
#filexml.close()

    
for file in os.listdir("./"+filesdir):
    if file.endswith(".jack"):
        fileJack = open( filesdir + "/" + file )
        filename = file[:-5]
        filexml = open(filesdir + "/"+filename + "Out.xml", "w")
        filevm = open(filesdir + "/" + filename + ".vm","w")
        print "Compiling " + file
        inputfile = fileJack.read()
        tokenizedlist = jackTokenizer( inputfile )

        symTable = SymbolTable()
        className = ""
        nbLabelIf = 0
        nbLabelWhile = 0
        vmWriter = VMWriter()
        
        xml = CompilationEngine( tokenizedlist )
        filexml.write("\n".join(xml))
        vmWriter.writeToFile( filevm )
        filevm.close()
        filexml.close()       
        fileJack.close()
