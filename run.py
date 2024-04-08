import os
import subprocess
import shutil
import shlex
import time

def main():
    exec_filename = getExecutable()
    print()

    user_args = getExecArgs(exec_filename)
    print()


    num_iters = getNumIters()
    print()

    runProcessIters(exec_filename, user_args, num_iters)


def getExecutable():
    print("Getting executable...")

    directory = os.getcwd() 

    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)
    
        if os.path.isfile(f):


            if shutil.which(f) != None:

                print("Executable found, is this the correct executable?")
                print(f)
                user_answer = input("(Y/N)\n")

                if user_answer.upper() == 'Y':
                    print("Selecting executable %s" % f)
                    return f
                
                print("Searching for another executable...")
                print()

    print("No executable found! Aborting")
    exit(-1)


def getExecArgs(exec_file):


    arg_proc = subprocess.run([exec_file, "--help"], capture_output=True, text=True)

    print(arg_proc.stdout)
    print()

    user_confirm = False

    while user_confirm != True:


        print("Input arguments for executable below. Type how you would normally input shell arguments.\n")
        user_args = input("Args here: ")

        print()
        print("Command will look like this:")
        print(exec_file, user_args)

        print("Is this correct? (Y/N)")
        user_input = input()

        if user_input.upper() == "Y":
            user_confirm = True

    user_args = shlex.split(user_args)

    return user_args

def getNumIters():

    print("How many iterations should this script run?")
    num_iters = input("Iterations here: ")

    print("Going to do %d iterations" % int(num_iters))

    return int(num_iters)

def runProcessIters(exec_filename, user_args, num_iters):

    proc_args = user_args

    proc_args.insert(0, exec_filename)
    
    for iteration in range(num_iters):

        subprocess.run(proc_args, stdout=subprocess.DEVNULL)




if __name__ == '__main__':
    main()