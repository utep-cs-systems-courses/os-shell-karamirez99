from os import read, write

sbuf = ""
    
def readLine(keepNewLine = False):
    global sbuf
    lineToReturn = ""
    
    while True:
        myChar = mygetchar()
        
        if myChar == "":
            return ""
        
        if myChar == '\n':
            if keepNewLine:
                lineToReturn += '\n'        
            return lineToReturn
        else:
            lineToReturn += myChar

def mygetchar():
    global sbuf

    #Read more characters when nothing is left in buffer
    if not len(sbuf):
        ibuf = read(0, 100)
        sbuf = ibuf.decode()

    if len(sbuf):
        charToReturn = sbuf[0]
        sbuf = sbuf[1:]
        return charToReturn
    else:
        return ""

def readLines():
    line = readLine(True)
    
    while line != "":
        writeLine(line)
        line = readLine(True)

    
def writeLine(line):
    write(1, line.encode())

if __name__ == "__main__":
    readLines()
