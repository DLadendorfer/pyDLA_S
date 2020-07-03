from simulation import Simulation
import constant
import logging

def main():
    '''Entry point.'''
    logging.basicConfig(level=logging.DEBUG)
    logging.info(constant.VERSION_STRING)
    logging.debug("__main__")

    start()

def start():
    sim = Simulation(400)
    sim.initialize_simulation()
    sim.start_simulation()
    sim.stop_simulation()


if __name__ == "__main__":
    main()


