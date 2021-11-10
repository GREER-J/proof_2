from Model.world_object import World_Objects
from config import WORLD_SETTINGS, AGENTS
from controller import Controller
from Model.world_object import Marker
from Model.agent import USV, UAV
from Model.master_controller import Master_controller
import random


class Simulation:
    def __init__(self) -> None:
        self.MICRO_X_MAX = WORLD_SETTINGS['MACRO_X_MAX'] * \
            WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
        self.MICRO_Y_MAX = WORLD_SETTINGS['MACRO_Y_MAX'] * \
            WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION']
        self.objects = []
        self.agents = []
        self.create_markers()
        self.create_agents()
        self.master_controller = Master_controller(
            WORLD_SETTINGS['MACRO_X_MAX'], WORLD_SETTINGS['MACRO_Y_MAX'], WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])

    def create_markers(self):
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

    def create_agents(self):
        number_of_USV = AGENTS['NUMBER_OF_USV']
        # Create USV
        for i in range(number_of_USV):
            agent = USV(0, 0, self)  # ToDo: Make this relate to config file
            self.agents.append(agent)
        # Create UAV
        number_of_UAV = AGENTS['NUMBER_OF_UAV']
        for i in range(number_of_UAV):
            agent = UAV(0, 1, self)  # ToDo: Make this relate to config file
            self.agents.append(agent)

    def run_mainloop(self):
        for agent in self.agents:
            agent.mainloop()

    def handle_report_detection_to_master_controller(self, object):
        self.master_controller.add_detected_object(object)
