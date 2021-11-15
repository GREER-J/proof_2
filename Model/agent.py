import random
from config import WORLD_SETTINGS
from Model.macro_map import Macro_map
import math


class Agent:
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
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
        return(int(self.micro_x_position / self.MACRO_TO_MICRO_CONVERSION))

    @property
    def macro_y_position(self):
        return(int(self.micro_y_position / self.MACRO_TO_MICRO_CONVERSION))

    def move(self, target_micro_x_position: int, target_micro_y_position: int):
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
        square = self.simulation.master_controller.macro_map.get_cell_obj_from_macro(
            self.macro_x_position, self.macro_y_position)
        square.release_from_marked_as_assigned()

    def search_macro_grid(self):
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

    def go_home(self):
        # Select home cords
        if(self.mission == 'idle'):
            self.mission = 'go home'
        self.move(self.home_micro_x_position, self.home_micro_y_position)
        self.see()
        if(self.moving == False):
            # We're home
            self.mission = 'standby home'

    def scout(self):
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

    def enact_mission(self, mission_choice: str):
        if(mission_choice == 'move'):
            self.move_mission()
        elif(mission_choice == 'go home'):
            self.go_home()
        elif(mission_choice == 'scout'):
            self.scout()

    def run_policy(self) -> str:
        # ToDo: Make this individual to UAV, USV!
        mission_choice = 'go home'
        if(self.found_object < self.total_objects):
            mission_choice = 'scout'
        return(mission_choice)

    def mainloop(self):
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
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position,
                         simulation, MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        self.detection_range = 1  # ToDo: Make this relate to config file


class UAV(Agent):
    def __init__(self, start_micro_x_position: int, start_micro_y_position: int, simulation, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        super().__init__(start_micro_x_position, start_micro_y_position,
                         simulation, MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        self.detection_range = 3  # ToDo: Make this relate to config file
