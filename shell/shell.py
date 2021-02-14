import os
import sys
from myIO import readLine, writeLine

def main():
    while True:
        writeLine("$: ")
        inputline = readLine()

        if (inputline == 'exit'):
            break
    
        if len(inputline) == 0 or inputline[0] == ' ':
            continue

        args = inputline.split(" ")
        rc = os.fork()

        if rc < 0:
            writeLine("Fork Failed")
        elif rc == 0:
            attemptCommands(args)
            sys.exit(1)
        else:
            os.wait()
        
        
def attemptCommands(args):
    dirs = os.environ["PATH"]
    
    for dir in dirs.split(":"):
        program = "{}/{}".format(dir, args[0])
        try:
            os.execve(program, args, os.environ)
        except OSError:
            pass
    writeLine("Unrecognized Command\n")

    
if __name__ == "__main__":
    main()
