import os
import subprocess
import random
import logging



def RunProcess(sample_program, optimal_program, map_file, timeout, num_agents, rectangle, seed, num_iters):

    handler = logging.FileHandler("rollouts.log")   
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    handler.setFormatter(formatter)

    logger = logging.getLogger("RolloutLog")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    random.seed(seed)

    agent_file = ".".join((str(os.getpid()), "agents"))

    sample_args = []

    sample_args.append(sample_program)

    sample_args.append("-m")
    sample_args.append(map_file)

    sample_args.append("-k")
    sample_args.append(str(num_agents))

    sample_args.append("-t")
    sample_args.append(str(timeout))

    sample_args.append("-r")
    sample_args.append(str(rectangle))

    sample_args.append("-a")
    sample_args.append(agent_file)

    sample_args.append("-o")
    sample_args.append(".".join( ( ( str(os.getpid()) + "_sample"), "csv") ) )

    sample_args.append("-j")
    sample_args.append(".".join( ( ( str(os.getpid()) + "_sample"), "json") ) )

    sample_args.append("-d")
    sample_args.append( str(random.randint(0, 2147483647)) )

    optimal_args = []

    optimal_args.append(optimal_program)

    optimal_args.append("-m")
    optimal_args.append(map_file)

    optimal_args.append("-k")
    optimal_args.append(str(num_agents))

    optimal_args.append("-t")
    optimal_args.append(str(timeout))

    optimal_args.append("-r")
    optimal_args.append(str(rectangle))

    optimal_args.append("-a")
    optimal_args.append(agent_file)

    optimal_args.append("-o")
    optimal_args.append(".".join( ( ( str(os.getpid()) + "_optimal"), "csv") ) )
    
    for iteration in range(num_iters):

        logger.info("PID %d: Starting sample program with args: %s" % (os.getpid(), sample_args))

        subprocess.run(sample_args, stdout=subprocess.DEVNULL)

        logger.info("Sample PID %d: Iteration completed with args: %s" % (os.getpid(), sample_args))

        logger.info("Optimal PID %d: Starting optimal program with args: %s" % (os.getpid(), optimal_args))

        subprocess.run(optimal_args, stdout=subprocess.DEVNULL)

        logger.info("Optimal PID %d: Iteration completed with args: %s" % (os.getpid(), optimal_args))

        try:
            os.remove(agent_file)
        except OSError:
            pass

    
    