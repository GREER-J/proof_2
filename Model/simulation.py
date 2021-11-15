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
        self.create_agents(
            WORLD_SETTINGS['MACRO_X_MAX'], WORLD_SETTINGS['MACRO_Y_MAX'], WORLD_SETTINGS['MACRO_TO_MICRO_CONVERSION'])
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

    def create_agents(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int):
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
        for agent in self.agents:
            agent.mainloop()

    def handle_report_detection_to_master_controller(self, object):
        self.master_controller.add_detected_object(object)

    def handle_request_for_updated_tasks(self):
        master_controller_communicating = True
        found_objects, identified_objects, interacted_objects, total_objects = self.master_controller.request_updated_task_list()
        return(master_controller_communicating, found_objects, identified_objects, interacted_objects, total_objects)

    def handle_request_for_updated_macro_map(self):
        master_controller_communicating = True
        macro_map = self.master_controller.request_macro_map()
        return(master_controller_communicating, macro_map)
