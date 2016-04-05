import os
from collections import deque
os.chdir("C:/Users/cypriend/Documents/05. Perso/NandToTetris/nand2tetris/projects/10")

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
keywordDic["field"] = "classVarDec"
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
    token = tokenQueue.popleft()
    openLabel( xml, "class" , nbtab )
    writeTerminal( xml, token , nbtab+1 )
    
    t = tokenQueue.popleft()
    checkType( identifier, t )
    writeTerminal( xml,t, nbtab+1)

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

def CompileClassVarDec( tokenQueue, nbtab, xml ):
    openLabel( xml, "classVarDec" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkIsKeyType( t, False )
    writeTerminal( xml, t, nbtab + 1 )

    t = tokenQueue.popleft()
    checkType( identifier, t )
    writeTerminal( xml, t, nbtab+1)

    t = tokenQueue[0]
    while( t.getVal() == "," ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1)

        t = tokenQueue.popleft()
        checkType( identifier, t )
        writeTerminal( xml, t, nbtab+1)

        t = tokenQueue[0]

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1)
    closeLabel( xml, "classVarDec" , nbtab )

################## Compile Subroutine Method ###################

def CompileSubroutine(tokenQueue, nbtab, xml ):
    openLabel( xml, "subroutineDec" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkIsKeyType( t, True )
    writeTerminal( xml, t, nbtab + 1 )

    t = tokenQueue.popleft()
    checkType( identifier, t )
    writeTerminal( xml, t, nbtab+1)

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileParameterList( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileSubroutineBody( tokenQueue, nbtab+1, xml )
    
    closeLabel( xml, "subroutineDec" , nbtab )

################## Compile ParemetersList Method ###################

def CompileParameterList( tokenQueue, nbtab, xml ):
    openLabel( xml, "parameterList" , nbtab )
    t = tokenQueue[0]
    if t.isType( False ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1)

        t = tokenQueue.popleft()
        checkType( identifier, t )
        writeTerminal( xml, t, nbtab+1)

        while ( tokenQueue[0].getVal() == "," ):
            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1)

            t = tokenQueue.popleft()
            checkIsKeyType( t, False )
            writeTerminal( xml, t, nbtab+1)

            t = tokenQueue.popleft()
            checkType( identifier, t )
            writeTerminal( xml, t, nbtab+1)
            
    closeLabel( xml, "parameterList" , nbtab )


################## Compile SubRoutineBody Method ###################

def CompileSubroutineBody( tokenQueue, nbtab, xml ):
    openLabel( xml, "subroutineBody" , nbtab )

    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1 )

    while ( tokenQueue[0].getVal() == "var" ):
        CompileVarDec( tokenQueue, nbtab +1 , xml)

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "subroutineBody" , nbtab )

################## Compile VarDec Method ###################

def CompileVarDec( tokenQueue, nbtab, xml ):
    openLabel( xml, "varDec" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )
    
    t = tokenQueue.popleft()
    checkIsKeyType( t, False )
    writeTerminal( xml, t, nbtab+1)
        
    t = tokenQueue.popleft()
    checkType( identifier, t )
    writeTerminal( xml, t, nbtab+1)

    while ( tokenQueue[0].getVal() == "," ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1)
            
        t = tokenQueue.popleft()
        checkType( identifier, t )
        writeTerminal( xml, t, nbtab+1)

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )
    
    closeLabel( xml, "varDec" , nbtab )

################## Compile Statements Method ###################

def CompileStatements( tokenQueue, nbtab, xml ):
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

def CompileLetStatement( tokenQueue, nbtab, xml ):
    openLabel( xml, "letStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )
    
    t = tokenQueue.popleft()
    checkType( identifier, t )
    writeTerminal( xml, t, nbtab+1)

    if( tokenQueue[0].getVal() == "[" ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1 )

        CompileExpression( tokenQueue, nbtab+1, xml )

        t = tokenQueue.popleft()
        checkValue( "]", t )
        writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "=", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )    
    
    closeLabel( xml, "letStatement" , nbtab )

################## Compile IfStatement Method ###################

def CompileIfStatement( tokenQueue, nbtab, xml ):
    openLabel( xml, "ifStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    writeTerminal( xml, t, nbtab+1 )

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

    closeLabel( xml, "ifStatement" , nbtab )

################## Compile WhileStatement Method ###################

def CompileWhileStatement( tokenQueue, nbtab, xml ):
    openLabel( xml, "whileStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileExpression( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( ")", t )
    writeTerminal( xml, t, nbtab+1 )

    t = tokenQueue.popleft()
    checkValue( "{", t )
    writeTerminal( xml, t, nbtab+1 )

    CompileStatements( tokenQueue, nbtab+1, xml )

    t = tokenQueue.popleft()
    checkValue( "}", t )
    writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "whileStatement" , nbtab )

################## Compile doStatement Method ###################

def CompileDoStatement( tokenQueue, nbtab, xml ):
    openLabel( xml, "doStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    CompileSubroutineCall( tokenQueue, nbtab+1, xml)

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "doStatement" , nbtab )

################## Compile returnStatement Method ###################

def CompileReturnStatement( tokenQueue, nbtab, xml ):
    openLabel( xml, "returnStatement" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab+1 )

    if( tokenQueue[0].getVal() != ";" ):
        CompileExpression( tokenQueue, nbtab+1, xml)

    t = tokenQueue.popleft()
    checkValue( ";", t )
    writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "returnStatement" , nbtab )

################## Compile Expression Method ###################

def CompileExpression( tokenQueue, nbtab, xml ):
    openLabel( xml, "expression" , nbtab )

    CompileTerm( tokenQueue, nbtab +1, xml)

    while( tokenQueue[0].isOp() ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1 )

        CompileTerm( tokenQueue, nbtab +1, xml)

    closeLabel( xml, "expression" , nbtab )


################## Compile Term Method ###################

def CompileTerm( tokenQueue, nbtab, xml ):
    openLabel( xml, "term" , nbtab )

    type = tokenQueue[0].getType()
    if ( type == intconst or type == strconst ):
        t = tokenQueue.popleft()
        writeTerminal( xml, t, nbtab+1 )
    elif ( type == keyword ):
        t = tokenQueue.popleft()
        checkIsKeyConst( t )
        writeTerminal( xml, t, nbtab+1)
    elif ( type == symbol ):
        t = tokenQueue.popleft()
        if ( t.isUnaryOp() ):
            writeTerminal( xml, t, nbtab+1)
            CompileTerm( tokenQueue, nbtab +1 , xml )
        else:
            checkValue( "(", t )
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab +1, xml )

            t = tokenQueue.popleft()
            checkValue( ")", t )
            writeTerminal( xml, t, nbtab+1 )
    else :
        nextTokenVal = tokenQueue[1].getVal()
        if nextTokenVal == "(" or nextTokenVal == ".":
            CompileSubroutineCall( tokenQueue, nbtab +1, xml)
        elif nextTokenVal == "[":
            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1 )

            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab +1, xml)

            t = tokenQueue.popleft()
            checkValue( "]", t )
            writeTerminal( xml, t, nbtab+1 )            
        else:
            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1 )

    closeLabel( xml, "term" , nbtab )

################## Compile subroutinCall Method ###################

def CompileSubroutineCall( tokenQueue, nbtab, xml ):
    #openLabel( xml, "subroutineCall" , nbtab )

    t = tokenQueue.popleft()
    writeTerminal( xml, t, nbtab )

    t = tokenQueue.popleft()
    if t.getVal() == ".":
        writeTerminal( xml, t, nbtab )

        t = tokenQueue.popleft()
        checkType( identifier, t )
        writeTerminal( xml, t, nbtab)

        t = tokenQueue.popleft()
        
    checkValue( "(", t )
    writeTerminal( xml, t, nbtab )

    CompileExpressionList( tokenQueue, nbtab, xml)

    t = tokenQueue.popleft()
    checkValue( ")", t )
    writeTerminal( xml, t, nbtab )
    
    #closeLabel( xml, "subroutineCall" , nbtab )

################## Compile ExpressionList Method ###################

def CompileExpressionList( tokenQueue, nbtab, xml ):
    openLabel( xml, "expressionList" , nbtab )

    if tokenQueue[0].getVal() != ")":
        CompileExpression( tokenQueue, nbtab+1, xml)

        while tokenQueue[0].getVal() == ",":
            t = tokenQueue.popleft()
            writeTerminal( xml, t, nbtab+1 )

            CompileExpression( tokenQueue, nbtab+1, xml)
    
    closeLabel( xml, "expressionList" , nbtab )

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
        filexml = open(filesdir + "/"+filename + "O.xml", "w")
        print "Compiling " + file
        inputfile = fileJack.read()
        tokenizedlist = jackTokenizer( inputfile )
        xml = CompilationEngine( tokenizedlist )
        filexml.write("\n".join(xml))
        filexml.close()       
        fileJack.close()
