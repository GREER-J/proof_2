import random
from config import WORLD_SETTINGS
import math


class Agent:
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation) -> None:
        self.simulation = simulation
        self.micro_x_position = start_micro_x_position
        self.micro_y_position = start_micro_y_position
        self.home_micro_x_position = start_micro_x_position
        self.home_micro_y_position = start_micro_y_position
        self.mission = 'idle'
        self.moving = False

    def move(self, target_micro_x_position: int, target_micro_y_position: int):
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
        random_micro_x_position = random.randrange(
            0, self.simulation.MICRO_X_MAX)
        random_micro_y_position = random.randrange(
            0, self.simulation.MICRO_Y_MAX)
        return(random_micro_x_position, random_micro_y_position)

    def see(self):
        """see checks through each world object in the simulation and checks if it is within detection range
        """
        for world_object in self.simulation.objects:
            delta_x = world_object.micro_x_position - self.micro_x_position
            delta_y = world_object.micro_y_position - self.micro_y_position
            distance = math.sqrt(delta_x**2 + delta_y**2)
            if(distance < self.detection_range):
                if(world_object.detected == False):
                    # Object detected
                    world_object.set_detected()
                    # Report detection
                    self.simulation.handle_report_detection_to_master_controller(
                        world_object)

    def move_mission(self):
        if(self.mission == 'idle'):
            self.target_x, self.target_y = self.select_random_target()
            self.mission = 'Moving'
        self.move(self.target_x, self.target_y)
        self.see()
        if(self.moving == False):
            # We've stopped moving, mission complete
            self.mission = 'idle'

    def enact_mission(self, mission_choice: str):
        if(mission_choice == 'move'):
            self.move_mission()

    def run_policy(self) -> str:
        # ToDo: Make this individual to UAV, USV!
        mission_choice = 'move'
        return(mission_choice)

    def mainloop(self):
        # Choose what to do
        mission_choice = self.run_policy()

        # Enact mission
        self.enact_mission(mission_choice)


class USV(Agent):
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position, simulation)
        self.detection_range = 1  # ToDo: Make this relate to config file


class UAV(Agent):
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position, simulation)
        self.detection_range = 3  # ToDo: Make this relate to config file
