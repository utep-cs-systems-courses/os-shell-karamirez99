import os
import sys
from myIO import readLine, writeLine

Testing = False

def main():
    PS1 = os.environ["PS1"] if "PS1" in os.environ else "$: "
    
    while True and not Testing:
        wait = True
        writeLine(PS1)
            
        inputline = readLine()

        if (inputline == 'exit'):
            break

        #ignore basic invalid input
        if len(inputline) == 0 or inputline[0] == ' ':
            continue

        args = inputline.split(" ")

        #directly handle change directory
        if args[0] == 'cd':
            os.chdir(args[1])
            continue

        rc = None

        if "&" in args:
            wait = False
            args = args[0:args.index("&")] + args[args.index("&") + 1:]
            
        #handle pipes
        if "|" in args:
            rc, args = handlePipes(args)
        else:
            rc = os.fork()
            
        if rc < 0:
            writeLine("Fork Failed")
        elif rc == 0:
            if "<" in args or ">" in args:
               args = redirect(args)
            attemptCommands(args)
            sys.exit(1)
        else:
            if not wait:
                continue
            #Wait for all child process to end
            while True:
                try:
                    os.wait() #Parent waits for child process to end
                except ChildProcessError:
                    break
            
    print("Exiting my shell")
        
def attemptCommands(args):
    dirs = os.environ["PATH"]

    #Try to find given program for each dir in PATH
    for dir in dirs.split(":"):
        program = "{}/{}".format(dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except OSError:
            pass
    writeLine("Unrecognized Command\n")

def redirect(args):
    if ">" in args:
        os.close(1)
        os.open(args[args.index(">") + 1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)
        args = args[0:args.index(">")] + args[args.index(">") + 2:]

    if "<" in args:
        os.close(0)
        os.open(args[args.index("<") + 1], os.O_RDONLY)
        os.set_inheritable(0, True)
        args = args[0:args.index("<")] + args[args.index("<") + 2:]
        
    return args

def handlePipes(args):
    args = separatePipes(args)
    fds = [os.pipe() for i in range(len(args) - 1)] # call pipe for each pipe
    rc = None
    
    for fdPair in fds:
        for fd in fdPair:
            os.set_inheritable(fd, True)
                    
    for i in range(len(args)):
        rc = os.fork()
        if rc < 0:
            sys.exit(1)
        elif rc == 0:
            if i == 0:
                directPipes(fds[0], "w")
            elif i == len(args) - 1:
                directPipes(fds[-1], "r")
            else:
                fd = (fds[i-1][0], fds[i][1])
                directPipes(fd, "rw")
            args = args[i]
            break;
    closePipes(fds)    

    return (rc, args)
    
def separatePipes(args):
    numPipes = args.count("|")
    newArgs = [[] for i in range(numPipes + 1)]

    for i in range(numPipes):
        newArgs[i] = args[0: args.index("|")]
        args = args[args.index("|") + 1:]

    newArgs[-1] = args
    return newArgs
        
def directPipes(fd, flag):
    set0 = False
    set1 = False

    #Given to the argument after last pipe
    if flag == "r":
        set0 = updateFD(fd, 0)

    #Given to the argument before first pipe
    elif flag == "w":
        set1 = updateFD(fd, 1)
        
    else:
        set0 = updateFD(fd, 0)
        set1 = updateFD(fd, 1)
      
    if set0:
        os.set_inheritable(0, True)
    if set1:
        os.set_inheritable(1, True)

def updateFD(fd, fdNum):
    os.close(fdNum)
    os.dup(fd[fdNum])
    return True
        
def closePipes(fds):
    for fdPair in fds:
        for fd in fdPair:
            os.close(fd)
        
if __name__ == "__main__":
    main()
