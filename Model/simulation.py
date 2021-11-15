from Model.world_object import World_Objects
from config import WORLD_SETTINGS, AGENTS
from controller import Controller
from Model.world_object import Marker
from Model.agent import USV, UAV
from Model.master_controller import Master_controller
import random


class Simulation:
    """ A class to handle the simulation and contain everything in it
    """

    def __init__(self) -> None:
        """__init__ creates a new simulation using values from the config file

        This means:
         - Create all markers in the world
         - Create all agents in the world
        - Create the master controller
        """
        # ToDo: Make the config file passed in my the main file
        self.MICRO_X_MAX = WORLD_SETTINGS['MACRO_X_MAX'] * \
            WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
        self.MICRO_Y_MAX = WORLD_SETTINGS['MACRO_Y_MAX'] * \
            WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
        self.objects = []
        self.agents = []
        self.create_markers()
        self.create_agents(
            WORLD_SETTINGS['MACRO_X_MAX'], WORLD_SETTINGS['MACRO_Y_MAX'], WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])
        self.master_controller = Master_controller(
            WORLD_SETTINGS['MACRO_X_MAX'], WORLD_SETTINGS['MACRO_Y_MAX'], WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])

    def create_markers(self):
        """create_markers creates all the markers required using data from the config file
        """
        number_of_markers = WORLD_SETTINGS['MARKERS_IN_WORLD']
        for i in range(number_of_markers):
            # Create marker object
            # Select macro grid
            macro_x_position = random.randrange(
                0, WORLD_SETTINGS['MACRO_X_MAX'])
            macro_y_position = random.randrange(
                0, WORLD_SETTINGS['MACRO_Y_MAX'])

            # Select where in that macro square
            micro_x_position = macro_x_position * \
                WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
            micro_x_position += random.randrange(
                0, WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])

            micro_y_position = macro_y_position * \
                WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
            micro_y_position += random.randrange(
                0, WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])
            marker_object = Marker(
                micro_x_position, micro_y_position, macro_x_position, macro_y_position)
            # Add marker to objects
            self.objects.append(marker_object)

    def create_agents(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int):
        """create_agents creates all agents in the simulation

        Args:
            MACRO_X (int): The x position of the macro square
            MACRO_Y (int): The y position of the macro square
            MACRO_TO_MICRO_CONVERSION (int): The number of micro steps for every macro step
        """
        number_of_USV = AGENTS['NUMBER_OF_USV']
        # Create USV
        for i in range(number_of_USV):
            # ToDo: Make this relate to config file
            agent = USV(0, 0, self, MACRO_X, MACRO_Y,
                        MACRO_TO_MICRO_CONVERSION)
            self.agents.append(agent)
        # Create UAV
        number_of_UAV = AGENTS['NUMBER_OF_UAV']
        for i in range(number_of_UAV):
            # ToDo: Make this relate to config file
            agent = UAV(0, 1, self, MACRO_X, MACRO_Y,
                        MACRO_TO_MICRO_CONVERSION)
            self.agents.append(agent)

    def run_mainloop(self):
        """run_mainloop loops through each agents and calls their mainloop for this timestep
        """
        for agent in self.agents:
            agent.mainloop()

    def handle_report_detection_to_master_controller(self, world_object):
        """handle_report_detection_to_master_controller calls the relevant function on the master controller

        Args:
            world_object (world_object): The world object to be reported to the master controller
        """
        self.master_controller.add_detected_object(world_object)

    def handle_request_for_updated_tasks(self):
        """handle_request_for_updated_tasks simulates calls to the master controller for updated tasks
        We:
         - Get the required data from the master controller
         - Determine whether in this simulation the master controller is communicating or not
         - Pass all this information onto the agent calling
        """
        master_controller_communicating = True
        found_objects, identified_objects, interacted_objects, total_objects = self.master_controller.request_updated_task_list()
        return(master_controller_communicating, found_objects, identified_objects, interacted_objects, total_objects)

    def handle_request_for_updated_macro_map(self):
        """handle_request_for_updated_macro_map handles requests for updated macro maps
         - Get the required data from the master controller
         - Determine whether in this simulation the master controller is communicating or not
         - Pass all this information onto the agent calling
        """
        master_controller_communicating = True
        macro_map = self.master_controller.request_macro_map()
        return(master_controller_communicating, macro_map)
