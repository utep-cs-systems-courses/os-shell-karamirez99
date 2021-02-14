from os import read, write

ibuf = None
sbuf = ""
    
def readLine():
    global sbuf

    while True:
        myChar = mygetchar()
        if myChar == "":
            return ""
        if myChar == '\n':
            lineToReturn = sbuf
            sbuf = ""
            return lineToReturn
        else:
            sbuf += myChar

def mygetchar():
    global ibuf
    global sbuf

    if not ibuf or not len(sbuf):
        ibuf = read(0, 100)
        sbuf = ibuf.decode()

    if len(sbuf):
        charToReturn = sbuf[0]
        sbuf = sbuf[1:]
        return charToReturn
    else:
        return ""

    
def writeLine(line):
    write(1, line.encode())
