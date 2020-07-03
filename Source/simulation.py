import logging
import constant
import time
import random

from threading import Thread
from tkinter import *
from enum import Enum

class State(Enum):
    '''Simulation states'''
    NOT_INITIALIZED = 1
    INITIALIZED = 2
    STARTED = 3

class Simulation:
    '''Simulation of a diffusion limited aggregation.'''

    def __init__(self, size):
        '''Constructor'''
        self.state = State.NOT_INITIALIZED
        self.size = size
        self.color = 0x773333
        self.color_negate = False
        self.points = {}

    def initialize_simulation(self):
        '''Initializes the simulation'''
        self.assert_state(State.NOT_INITIALIZED)
        logging.debug("Initializing simulation.")

        self.initialize_gui()

        self.state = State.INITIALIZED

    def start_simulation(self):
        '''Start simulation'''
        self.assert_state(State.INITIALIZED)
        logging.debug("Starting simulation.")
        self.state = State.STARTED
        self.thread = Thread(group=None, target=self.run, name=constant.SHORT_NAME)
        self.thread.start()
        mainloop()

    def stop_simulation(self):
        '''Stop simulation'''
        self.assert_state(State.STARTED)
        logging.debug("Stopping simulation.")
        self.state = State.NOT_INITIALIZED


    def initialize_gui(self):
        logging.debug("Initializing window.")
        window = Tk()
        window.title(constant.NAME)
        canvas = Canvas(window, width=self.size, height=self.size, bg="#000000")
        canvas.pack()
        self.img = PhotoImage(width=self.size, height=self.size)
        canvas.create_image((self.size // 2, self.size // 2), image = self.img, state="normal")

    def run(self):
        '''Runs the simulation'''
        logging.debug("Running simulation.")
        self.assert_state(State.STARTED)
        self.initialize_points()
        self.create_anchor_line()

        while self.state == State.STARTED:
            #create random x and y from which the random walk starts
            x = int(self.size * random.random())
            y = self.size - 10

            self.random_walk(x, y)

    def initialize_points(self):
        '''Initializes the points map'''
        for x in range(self.size):
            for y in range(self.size):
                self.points[x, y] = False

    def create_anchor_line(self):
        '''Creates an anchor of points to which the particles can dock to'''
        for x in range(self.size):
            self.points[x, 0] = True
            self.draw_point(x, 0)

    def random_walk(self, x, y):
        '''Random walk algorithm to move a particle until it touches another particle'''
        while self.is_in_bounds(x, y):
            x, y = self.apply_random_step(x, y)
            if self.is_touching(x, y):
                self.on_touching(x, y)
                return  # random walk is over because a touching particle exists

    def apply_random_step(self, x, y):
        '''Randomly increases or decreases x and/or y'''
        direction = random.random()

        if direction < 0.25:
            x -= 1
        elif direction < 0.5:
            x += 1
        elif direction < 0.65:
            y += 1
        else:
            y -= 1

        return (x, y)

    def is_in_bounds(self, x, y):
        '''Whether the given coordinates are in bounds'''
        return x < self.size - 2 and x > 1 and y < self.size - 2 and y > 1

    def is_touching(self, x, y):
        '''Checks whether the given coordinates are touching an existing particle'''
        #r = right, l = left, u = up, d = down
        r = self.points[x + 1, y]
        l = self.points[x - 1, y]
        u = self.points[x, y + 1]
        d = self.points[x, y - 1]
        ru = self.points[x + 1, y + 1]
        ld = self.points[x - 1, y - 1]
        rd = self.points[x + 1, y - 1]
        lu = self.points[x - 1, y + 1]
        return r or l or u or d or ru or ld or rd or lu

    def on_touching(self, x, y):
        '''Touching event handler'''
        logging.debug(f"Touch detected at {x}:{y}")
        self.points[x, y] = True
        self.draw_point(x, y)
        if y > self.size - 10:
            self.state = State.NOT_INITIALIZED

    def draw_point(self, x, y):
        '''Draws a point at the specified coordinates'''
        self.img.put("#{0:06X}".format(self.color), (x, y))
        self.update_color()

    def update_color(self):
        '''Updates the color'''
        if (self.color_negate):
            self.color -= 1
            if (self.color < 0x773333):
                self.color_negate = False
        else:
            self.color += 1
            if (self.color > 0xFFFFFF - 1):
                self.color_negate = True

    def assert_state(self, state):
        '''Asserts if the state if this instance is equal to the provided state.'''
        if not isinstance(state, State):
            logging.error("Illegal instance type of state")
            raise TypeError("Passed state is not an enumeration of type State")

        assert self.state == state