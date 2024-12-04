import os
import subprocess
import random
import logging



def RunProcess(sample_program, map_file, timeout, num_agents, rectangle, seed, num_iters, worker_id):

    handler = logging.FileHandler("rollouts.log")   
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    handler.setFormatter(formatter)

    logger = logging.getLogger("RolloutLog")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    random.seed(seed)

    agent_file = ".".join( (str(worker_id), "agents") )

    sample_args = []

    sample_args.append(sample_program)

    sample_args.append("-m")
    sample_args.append(map_file)

    sample_args.append("-k")
    sample_args.append(str(num_agents))

    sample_args.append("-t")
    sample_args.append(str(timeout))

    sample_args.append("--rectangle")
    sample_args.append(str(rectangle))

    sample_args.append("-a")
    sample_args.append(agent_file)

    sample_args.append("-o")
    sample_args.append(".".join( ( ( str(worker_id) + "_sample"), "csv") ) )

    sample_args.append("-j")
    sample_args.append(".".join( ( ( str(worker_id) + "_sample"), "json") ) )

    sample_args.append("-d")

    agent_seed = random.randint(0, 2147483647)

    sample_args.append( str(agent_seed))
    
    for _ in range(num_iters):

        logger.info("Worker ID %d: Starting sample program with args: %s" % (worker_id, sample_args))

        logger.info("Agent seed for worker ID %d is %d" % (worker_id, agent_seed) )

        subprocess.run(sample_args, stdout=subprocess.DEVNULL)

        logger.info("Sample Worker ID %d: Iteration completed with args: %s" % (worker_id, sample_args))

        agent_seed = random.randint(0, 2147483647)

        sample_args[-1] = str(agent_seed)

        try:
            os.remove(agent_file)
        except OSError:
            pass

    
    