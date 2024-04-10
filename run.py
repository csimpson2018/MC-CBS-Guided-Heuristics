import os
import subprocess
import shutil
import shlex
import random
import logging

logging.basicConfig(filename="rollouts.log",
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('RolloutLog')

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

    rng = random.seed()

    proc_args = user_args

    seed_arg_loc = None

    if "-d" in proc_args:
        seed_arg_loc = proc_args.index("-d") + 1
    elif "--seed" in proc_args:
        seed_arg_loc = proc_args.index("--seed") + 1
    else:
        proc_args.append("-d")
        proc_args.append(str(random.randint(0, 2147483647)))

        seed_arg_loc = len(proc_args) - 1


    agent_file_loc = None
    agent_arg_index = None

    try:
        agent_arg_index = proc_args.index("-a") + 1
    except ValueError:
        agent_arg_index = proc_args.index("--agents") + 1

    agent_file_loc = proc_args[agent_arg_index]
    

    proc_args.insert(0, exec_filename)

    process_arg_string = " ".join(proc_args)

    logger.info("Starting process with args: %s" % process_arg_string)
    
    for iteration in range(num_iters):

        subprocess.run(proc_args, stdout=subprocess.DEVNULL)

        try:
            os.remove(agent_file_loc)
        except OSError:
            pass

        proc_args[seed_arg_loc] = str(random.randint(0, 2147483647))




if __name__ == '__main__':
    main()

    logger.info("Process completed")
    