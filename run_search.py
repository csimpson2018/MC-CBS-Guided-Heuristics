import os
import multiprocessing as mp
import random
import logging

import search

from argparse import ArgumentParser

logging.basicConfig(filename="proc_spawner.log",
                    filemode='a',
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('SpawnerLog')

# Add arguments to arg parser
parser = ArgumentParser()

parser.add_argument("-s", "--sample", help="Program that will sample a goal node.", required=True, type=str)
parser.add_argument("-v", "--verify", help="Program that will verify the optimal solution.", required=True, type=str)
parser.add_argument("-m", "--map", help="REQUIRED. Domain to run the MAPF problems on.", required=True, type=str)
parser.add_argument("-t", "--timeout", help="How long the program should wait for the optimal solution, in seconds.", type=int)
parser.add_argument("-k", "--numAgents", help="REQUIRED. Number of agents to use in the MAPF problem.", required=True, type=int)
parser.add_argument("-r", "--rectangle", help="Whether to use rectangle reasoning or not.", type=int)
parser.add_argument("-d", "--seed", help="A seed to generate the random agent locations.", type=int)
parser.add_argument("-p", "--processes", help="REQUIRED. How many processes to use in parallel.", required=True, type=int)
parser.add_argument("-i", "--iterations", help="REQUIRED. How many iterations each subprocess should attempt.", required=True, type=int)

def main():

    passed_args = GetExecArgs()

    SpawnProcesses(passed_args)

def GetExecArgs():

    args = parser.parse_args()

    logger.info("Starting spawner with args: %s", args)

    return args
    
def SpawnProcesses(process_args):

    sample_program = process_args.sample

    optimal_program = process_args.verify

    map_file = process_args.map

    timeout = 7200

    if process_args.timeout != None:

        timeout = process_args.timeout

    num_agents = process_args.numAgents

    rectangle = 0

    if process_args.rectangle != None:

        rectangle = process_args.rectangle

    seed = 0

    if process_args.seed != None:

        seed = process_args.seed

    num_processes = process_args.processes

    num_iters = process_args.iterations


    if seed == 0:
        random.seed()
    else:
        random.seed(seed)

    if num_processes > mp.cpu_count():

        logger.warning("Number of requested processes is too large for system to execute simultaneously."
                      "Restricting number of processes to %d to ensure simultaneous execution of all processes.", (mp.cpu_count() - 1))
        
        num_processes = mp.cpu_count() - 1

    p = [mp.Process(target=search.RunProcess, args=(sample_program, optimal_program, map_file, timeout, num_agents, rectangle, random.randint(0, 2147483647), num_iters,)) for p in range(num_processes)]

    for proc in p:
        proc.start()

    for proc in p:
        proc.join()

        







if __name__ == '__main__':
    main()

    logger.info("Process completed")
    