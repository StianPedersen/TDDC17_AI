from asyncore import ExitNow, socket_map
from distutils.log import ERROR
from agents import Direction
from lab1.liuvacuum import *

DEBUG_OPT_DENSEWORLDMAP = False

AGENT_STATE_UNKNOWN = 0
AGENT_STATE_WALL = 1
AGENT_STATE_CLEAR = 2
AGENT_STATE_DIRT = 3
AGENT_STATE_HOME = 4

AGENT_DIRECTION_NORTH = 0
AGENT_DIRECTION_EAST = 1
AGENT_DIRECTION_SOUTH = 2
AGENT_DIRECTION_WEST = 3


def direction_to_string(cdr):
    cdr %= 4
    return "NORTH" if cdr == AGENT_DIRECTION_NORTH else\
        "EAST" if cdr == AGENT_DIRECTION_EAST else\
        "SOUTH" if cdr == AGENT_DIRECTION_SOUTH else\
        "WEST"  # if dir == AGENT_DIRECTION_WEST


"""
Internal state of a vacuum agent
"""


class MyAgentState:

    def __init__(self, width, height):

        # Initialize perceived world state
        self.world = [[AGENT_STATE_UNKNOWN for _ in range(
            height)] for _ in range(width)]
        self.world[1][1] = AGENT_STATE_HOME

        # Agent internal state
        self.last_action = ACTION_NOP
        self.direction = AGENT_DIRECTION_EAST
        self.pos_x = 1
        self.pos_y = 1

        # Metadata
        self.world_width = width
        self.world_height = height

    """
    Update perceived agent location
    """

    def update_position(self, bump):
        if not bump and self.last_action == ACTION_FORWARD:
            if self.direction == AGENT_DIRECTION_EAST:
                self.pos_x += 1
            elif self.direction == AGENT_DIRECTION_SOUTH:
                self.pos_y += 1
            elif self.direction == AGENT_DIRECTION_WEST:
                self.pos_x -= 1
            elif self.direction == AGENT_DIRECTION_NORTH:
                self.pos_y -= 1

    """
    Update perceived or inferred information about a part of the world
    """

    def update_world(self, x, y, info):
        self.world[x][y] = info

    """
    Dumps a map of the world as the agent knows it
    """

    def print_world_debug(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.world[x][y] == AGENT_STATE_UNKNOWN:
                    print("?" if DEBUG_OPT_DENSEWORLDMAP else " ? ", end="")
                elif self.world[x][y] == AGENT_STATE_WALL:
                    print("#" if DEBUG_OPT_DENSEWORLDMAP else " # ", end="")
                elif self.world[x][y] == AGENT_STATE_CLEAR:
                    print("." if DEBUG_OPT_DENSEWORLDMAP else " . ", end="")
                elif self.world[x][y] == AGENT_STATE_DIRT:
                    print("D" if DEBUG_OPT_DENSEWORLDMAP else " D ", end="")
                elif self.world[x][y] == AGENT_STATE_HOME:
                    print("H" if DEBUG_OPT_DENSEWORLDMAP else " H ", end="")

            print()  # Newline
        print()  # Delimiter post-print


"""
Vacuum agent
"""


class MyVacuumAgent(Agent):

    def __init__(self, world_width, world_height, log):
        super().__init__(self.execute)
        self.initial_random_actions = 10
        self.iteration_counter = 15*15*2*2*2*2
        self.state = MyAgentState(world_width, world_height)
        self.log = log

        # My variables
        self.path_taken = []

    def move_to_random_start_position(self, bump):
        action = random()

        self.initial_random_actions -= 1
        self.state.update_position(bump)

        if action < 0.1666666:   # 1/6 chance
            self.state.direction = (self.state.direction + 3) % 4
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT
        elif action < 0.3333333:  # 1/6 chance
            self.state.direction = (self.state.direction + 1) % 4
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT
        else:                    # 4/6 chance
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD

    def execute(self, percept):

        ###########################
        # DO NOT MODIFY THIS CODE #
        ###########################

        bump = percept.attributes["bump"]
        dirt = percept.attributes["dirt"]
        home = percept.attributes["home"]

        # Move agent to a randomly chosen initial position
        if self.initial_random_actions > 0:
            self.log("Moving to random start position ({} steps left)".format(
                self.initial_random_actions))
            return self.move_to_random_start_position(bump)

        # Finalize randomization by properly updating position (without subsequently changing it)
        elif self.initial_random_actions == 0:
            self.initial_random_actions -= 1
            self.state.update_position(bump)
            self.state.last_action = ACTION_SUCK
            self.log("Processing percepts after position randomization")
            return ACTION_SUCK

        ########################
        # START MODIFYING HERE #
        ########################

        # Max iterations for the agent
        if self.iteration_counter < 1:
            if self.iteration_counter == 0:
                self.iteration_counter -= 1
                self.log("Iteration counter is now 0. Halting!")
                self.log("Performance: {}".format(self.performance))
            return ACTION_NOP

        self.log("Position: ({}, {})\t\tDirection: {}".format(self.state.pos_x, self.state.pos_y,
                                                              direction_to_string(self.state.direction)))

        self.iteration_counter -= 1

        # Track position of agent
        self.state.update_position(bump)

        if bump:
            # Get an xy-offset pair based on where the agent is facing
            offset = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.state.direction]

            # Mark the tile at the offset from the agent as a wall (since the agent bumped into it)
            self.state.update_world(
                self.state.pos_x + offset[0], self.state.pos_y + offset[1], AGENT_STATE_WALL)

        # Update perceived state of current tile
        if dirt:
            self.state.update_world(
                self.state.pos_x, self.state.pos_y, AGENT_STATE_DIRT)
        else:
            self.state.update_world(
                self.state.pos_x, self.state.pos_y, AGENT_STATE_CLEAR)

        # Debug
        self.state.print_world_debug()

        #Beginning of our code
        # Functions

        #Checks if square sq is AGENT_STATE_UNKNOWN or AGENT_STATE_HOME
        def check_square(sq):
            if sq == AGENT_STATE_UNKNOWN or sq == AGENT_STATE_HOME:                    
                return False
            else:
                return True

        # Determines the direction of the robot and check if the square in front is visited
        def front_visited():
            if self.state.direction == AGENT_DIRECTION_NORTH:   
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y - 1])

            elif self.state.direction == AGENT_DIRECTION_EAST:
                return check_square(self.state.world[self.state.pos_x+1][self.state.pos_y])

            elif self.state.direction == AGENT_DIRECTION_SOUTH:
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y+1])

            elif self.state.direction == AGENT_DIRECTION_WEST:
                return check_square(self.state.world[self.state.pos_x-1][self.state.pos_y])
            
        # Determines the direction of the robot and check if the square directly to the right is visited
        def right_visited():
            if self.state.direction == AGENT_DIRECTION_NORTH:
                return check_square(self.state.world[self.state.pos_x+1][self.state.pos_y])

            elif self.state.direction == AGENT_DIRECTION_EAST:
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y+1])

            elif self.state.direction == AGENT_DIRECTION_SOUTH:
                return check_square(self.state.world[self.state.pos_x-1][self.state.pos_y])

            elif self.state.direction == AGENT_DIRECTION_WEST:
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y-1])
            
        # Determines the direction of the robot and check if the square directly to the left is visited
        def left_visited():
            if self.state.direction == AGENT_DIRECTION_NORTH:
                return check_square(self.state.world[self.state.pos_x-1][self.state.pos_y])

            elif self.state.direction == AGENT_DIRECTION_EAST:
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y-1])

            elif self.state.direction == AGENT_DIRECTION_SOUTH:
                return check_square(self.state.world[self.state.pos_x+1][self.state.pos_y])

            elif self.state.direction == AGENT_DIRECTION_WEST:
                return check_square(self.state.world[self.state.pos_x][self.state.pos_y+1])
            
        # Sets last action to forward, appends the direction of forward move and returns forward action.
        def go_forward():
            self.state.last_action = ACTION_FORWARD
            self.path_taken.append(self.state.direction)


            return ACTION_FORWARD

        # Turns right and sets state direction depending on current direction.
        def go_right():
            self.state.last_action = ACTION_TURN_RIGHT
            if self.state.direction == AGENT_DIRECTION_NORTH:
                self.state.direction = AGENT_DIRECTION_EAST
            elif self.state.direction == AGENT_DIRECTION_EAST:
                self.state.direction = AGENT_DIRECTION_SOUTH
            elif self.state.direction == AGENT_DIRECTION_SOUTH:
                self.state.direction = AGENT_DIRECTION_WEST
            elif self.state.direction == AGENT_DIRECTION_WEST:
                self.state.direction = AGENT_DIRECTION_NORTH
            return ACTION_TURN_RIGHT

        # Turns left and sets state direction depending on current direction.
        def go_left():
            self.state.last_action = ACTION_TURN_LEFT
            if self.state.direction == AGENT_DIRECTION_NORTH:
                self.state.direction = AGENT_DIRECTION_WEST
            elif self.state.direction == AGENT_DIRECTION_WEST:
                self.state.direction = AGENT_DIRECTION_SOUTH
            elif self.state.direction == AGENT_DIRECTION_SOUTH:
                self.state.direction = AGENT_DIRECTION_EAST
            elif self.state.direction == AGENT_DIRECTION_EAST:
                self.state.direction = AGENT_DIRECTION_NORTH
            return ACTION_TURN_LEFT

        # Returns true if tmp dir is opposite of the state direction
        def obtain_opposite(tmp_dir):
            if tmp_dir == 0 and self.state.direction == 2:
                return True
            if tmp_dir == 1 and self.state.direction == 3:
                return True
            if tmp_dir == 2 and self.state.direction == 0:
                return True
            if tmp_dir == 3 and self.state.direction == 1:
                return True
            return False


        # Decide action
        if dirt:
            self.log("DIRT -> choosing SUCK action!")
            self.state.last_action = ACTION_SUCK
            return ACTION_SUCK
        else:
            # We do not want to path into walls or obstacles
            if bump:
                if len(self.path_taken) != 0:
                    self.path_taken.pop()

            # Check front, right and left
            if front_visited() is False:
                return go_forward()
            elif right_visited() is False:
                return go_right()
            elif left_visited() is False:
                return go_left()
            else:
                # If all adjecent tiles has been visited go back.
                if len(self.path_taken) != 0:
                    tmp_dir = self.path_taken[-1]                  
                    if not obtain_opposite(tmp_dir):
                        return go_right()
                    self.path_taken.pop()
                    self.state.last_action = ACTION_FORWARD
                    return ACTION_FORWARD

                ##### Manhattan distance ###############################    
                if self.state.pos_x != 1:
                    if self.state.direction != AGENT_DIRECTION_WEST:
                        return go_right()
                    if bump:
                        self.log(self.iteration_counter)
                        self.iteration_counter = 0
                        self.state.last_action = ACTION_NOP
                        return ACTION_NOP
                    self.state.last_action = ACTION_FORWARD
                    return ACTION_FORWARD
                if self.state.pos_y != 1 :
                    if self.state.direction != AGENT_DIRECTION_NORTH:
                        return go_right()
                    if bump:
                        self.log(self.iteration_counter)
                        self.iteration_counter = 0
                        self.state.last_action = ACTION_NOP
                        return ACTION_NOP    
                    self.state.last_action = ACTION_FORWARD
                    return ACTION_FORWARD
                ##########################################################
                self.log(self.iteration_counter)
                self.iteration_counter = 0
                self.state.last_action = ACTION_NOP
                return ACTION_NOP
