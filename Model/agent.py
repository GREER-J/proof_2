import random
from config import WORLD_SETTINGS
from Model.macro_map import Macro_map
import math


class Agent:
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        """__init__ creates a generic world agent

        Args:
            start_micro_x_position (int): Starting x position in the micro world
            start_micro_y_position (int): Starting y position in the micro world
            simulation (Simulation object): An instance of the simulation class containing the simulation
            MACRO_X (int): Current x position in the macro world
            MACRO_Y (int): Current y position in the macro world
            MACRO_TO_MICRO_CONVERSION (int): The number of micro grid steps to one macro grid step
        """
        self.simulation = simulation
        self.MACRO_TO_MICRO_CONVERSION = MACRO_TO_MICRO_CONVERSION
        self.micro_x_position = start_micro_x_position
        self.micro_y_position = start_micro_y_position
        self.home_micro_x_position = start_micro_x_position
        self.home_micro_y_position = start_micro_y_position
        self.macro_map = Macro_map(MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        self.mission = 'idle'
        self.moving = False

    @property
    def macro_x_position(self):
        """macro_x_position is the current x position of the agent in the macro grid
        """
        return(int(self.micro_x_position / self.MACRO_TO_MICRO_CONVERSION))

    @property
    def macro_y_position(self):
        """macro_y_position is the current y position of the agent in the macro grid
        """
        return(int(self.micro_y_position / self.MACRO_TO_MICRO_CONVERSION))

    def move(self, target_micro_x_position: int, target_micro_y_position: int):
        """
        move moves the agent closer to a target x,y position.
        Sets a variable self.moving to true when moving and false is the agent arrives

        Args:
            target_micro_x_position (int): Target x position in the micro grid
            target_micro_y_position (int): Target y position in the micro grid
        """
        # ToDo: Add a for loop so UAV can move further than USV per turn
        self.moving = True
        delta_x = target_micro_x_position - self.micro_x_position
        delta_y = target_micro_y_position - self.micro_y_position
        if(delta_x > 0):
            # Move in +'ve x direction
            self.micro_x_position += 1
        if(delta_x < 0):
            # Move in -'ve x direction
            self.micro_x_position -= 1
        if(delta_y > 0):
            # Move in +'ve y direction
            self.micro_y_position += 1
        if(delta_y < 0):
            # Move in -'ve y direction
            self.micro_y_position -= 1
        if(delta_x == 0):
            if(delta_y == 0):
                # We've arrived
                self.moving = False

    def select_random_target(self) -> int:
        """select_random_target selects a random x,y position in the micro grid.
        This is no longer used but remains here in case it becomes useful

        Returns:
            int: two coordinates in the micro grid as a target x,y position
        """
        random_micro_x_position = random.randrange(
            0, self.simulation.MICRO_X_MAX)
        random_micro_y_position = random.randrange(
            0, self.simulation.MICRO_Y_MAX)
        return(random_micro_x_position, random_micro_y_position)

    def select_macro_square_to_search(self):
        """select_macro_square_to_search returns a macro square object if and only if it has not been searched previously and is not currently assigned to any other agent.

        Returns:
            (obj): Macro square object
        """
        for row in self.simulation.master_controller.macro_map.macro_map:
            for square in row:
                if(square.searched == False):  # The square hasn't been searched
                    if(square.assigned == False):  # The square isn't currently assigned for search
                        return (square)
        return(False)  # If no square meets requirements

    def release_macro_from_marked_as_assigned(self):
        """release_macro_from_marked_as_assigned marks the target square as no longer assigned to this agents
        """
        self.target_square.release_from_marked_as_assigned()

    def search_macro_grid(self):
        """search_macro_grid searches through each object in the simulation to see if it's our current macro square.
        This could be done by checking whether self.target_square has any objects in it but I wanted to keep this separate
        to enable us to muck around with simulating the macro controller not responding later
        """
        square = self.simulation.master_controller.macro_map.get_cell_obj_from_macro(
            self.macro_x_position, self.macro_y_position)
        square.mark_as_searched()
        for obj in self.simulation.objects:
            if(obj.detected == False):
                if(obj.macro_x_position == self.macro_x_position):
                    if(obj.macro_y_position == self.macro_y_position):
                        # We're in the same grid, mark as found
                        obj.set_detected()
                        self.simulation.handle_report_detection_to_master_controller(
                            obj)

    def see(self):
        # ToDo: Something is up with this function, it returns False when it clearly should't
        """see checks through each world object in the simulation and checks if it is within detection range.
        If an object is in range we return the object. Else we return False.
        """
        for world_object in self.simulation.objects:
            delta_x = world_object.micro_x_position - self.micro_x_position
            delta_y = world_object.micro_y_position - self.micro_y_position
            distance = math.sqrt(delta_x**2 + delta_y**2)
            if(distance < self.detection_range):
                if(world_object.detected == False):
                    return(world_object)
        return(False)

    def move_mission(self):
        """move_mission implements a move mission.
        We:
         - Set a random target x,y position if we haven't got one
         - Move to that position
         - Check to see if we can see anything

        If we arrive at out target position we set ourselves available for another mission.
        """
        if(self.mission == 'idle'):
            self.target_x, self.target_y = self.select_random_target()
            self.mission = 'Moving'
        self.move(self.target_x, self.target_y)
        self.see()
        if(self.moving == False):
            # We've stopped moving, mission complete
            self.mission = 'idle'

    def go_home(self):
        """go_home implements a go home mission
        We:
            - Set out target x,y position as home if we haven't already
            - Move towards home
            - See if we can see anything

        When we arrive home we go into a 'standby home' mode, which just stops movement.
        """
        # Select home cords
        if(self.mission == 'idle'):
            self.mission = 'go home'
        self.move(self.home_micro_x_position, self.home_micro_y_position)
        self.see()
        if(self.moving == False):
            # We're home
            self.mission = 'standby home'

    def scout(self):
        """scout implements a scout mission
        We:
            - Select a macro grid square to search by calling the relevant function
                - If a macro grid square can't be found we mark ourselves idle
                - If a macro grid square is found we set our target xy position to the center of that square

            - We move towards that square
            - Once we've arrived we search the square, report any finding and mark ourselves idle
        """
        # Select macro square
        if(self.mission == 'idle'):
            # Set target to center point
            self.mission = 'scout'
            self.target_square = self.select_macro_square_to_search()

            if(self.target_square == False):
                self.mission = 'idle'  # Mark available for more missions
                return
            else:
                # If we've found a square that matches requirements
                # Mark it out to us
                self.target_square.mark_as_assigned()
                # Set target x, y to center position of square
                self.target_x = self.target_square.micro_x_pos_center
                self.target_y = self.target_square.micro_y_pos_center

        # Move to target
        self.move(self.target_x, self.target_y)
        # Exit conditions
        if(self.moving == False):
            self.search_macro_grid()
            self.release_macro_from_marked_as_assigned()
            self.mission = 'idle'

    def interacting(self):
        if(self.mission == 'idle'):
            # Select object to identify
            for world_object in self.simulation.master_controller.known_objects:
                if(world_object.identified == False):  # If it hasn't been identified
                    # Set target to near object micro coords
                    self.target_x = world_object.micro_x_position - 1  # Just to the left of object
                    self.target_y = world_object.micro_y_position - 1  # Just underneath the object
        # Move towards object
        self.move(self.target_x, self.target_y)
        # If close enough to object identify it
        world_object = self.see()
        if(world_object):
            if(world_object.interacted == False):
                # Object detected
                world_object.set_interacted()
                # Report detection
                self.simulation.handle_report_interacted_to_master_controller()
                self.mission = 'idle'

    def enact_mission(self, mission_choice: str):
        """enact_mission takes a mission choice and calls the relevant function

        Args:
            mission_choice (str): the name of the mission type to be called
        """
        if(mission_choice == 'move'):
            self.move_mission()
        elif(mission_choice == 'go home'):
            self.go_home()
        elif(mission_choice == 'scout'):
            self.scout()
        elif(mission_choice == 'identify'):
            self.interacting()

    def mainloop(self):
        """mainloop runs through each of the decisions and actions of agents on each turn
        We:
         - Request the latest info of what tasks need doing from the macro controller
            - If we get a reply we replace our internal tasks with those from the macro controller
            - If we do not get a reply we just crack on using our internal ones (i.e no information from other agents) 
         - Request the latest macro map from the macro controller
            - If we get a reply we replace our internal map  with those from the macro controller
            - If we do not get a reply we just crack on using our internal map (i.e no information from other agents) 
         - Enact our policy specific to the agent type to generate a mission choice
         - Enact that choice
        """
        # Update task list
        rv = self.simulation.handle_request_for_updated_tasks()
        if(rv[0]):
            self.found_object = rv[1]
            self.identified_objects = rv[2]
            self.interacted_objects = rv[3]
            self.total_objects = rv[4]

        # Update map
        rv = self.simulation.handle_request_for_updated_macro_map()
        if(rv[0]):
            self.macro_map = rv[1]

        # Choose what to do
        mission_choice = self.run_policy()

        # Enact mission
        self.enact_mission(mission_choice)


class USV(Agent):
    """USV A class to handle the specifics of the UAV agent type.
    These agents can fly and so move faster than the USV type.
    They can't see as far, and cannot perform interaction mission but can still find and identify objects.

    Args:
        Agent (obj): The master class for all agents in the simulation
    """

    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position,
                         simulation, MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        self.detection_range = 1  # ToDo: Make this relate to config file

    def run_policy(self) -> str:
        """run_policy runs USV policy:

        USV will:
            - Interact with an object if available
            - Then identify objects if available
            - Then scout objects if available
            - Then go home

        Returns:
            str: The name of the mission type to be selected
        """
        mission_choice = 'go home'
        if(self.found_object < self.total_objects):
            mission_choice = 'scout'
        if(self.identified_objects < self.found_object):
            mission_choice = 'identify'
        return(mission_choice)


class UAV(Agent):
    """UAV a class to handle the specifics of the USV agent type.
    USV agents are a boat and so can't move very fast.
    They can perform all mission types, being the only ones who can do interaction missions.

    Args:
        Agent (obj): The master class for all agents in the simulation
    """

    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position,
                         simulation, MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        self.detection_range = 3  # ToDo: Make this relate to config file

    def run_policy(self) -> str:
        """run_policy UAV policy:

        UAV will:
            - Scout all objects first
            - Then identify objects
            - Then go home

        Returns:
            str: The name of the mission type to be selected
        """
        mission_choice = 'go home'
        if(self.found_object < self.total_objects):
            mission_choice = 'scout'
        return(mission_choice)
