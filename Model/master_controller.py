from Model.macro_map import Macro_map
import logging


class Master_controller:
    """ A class that represents the master controller
    """
    # ToDo: Implement logging

    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        """__init__ creates a new master controller object

        Args:
            MACRO_X (int): The length of the macro map in the x direction
            MACRO_Y (int): The length of the macro map in the y direction
            MACRO_TO_MICRO_CONVERSION (int): The number of micro steps for every macro step 
        """
        self.found_objects = 0
        self.objects_identified = 0
        self.object_interacted = 0
        self.total_objects = 3  # ToDo: Make this dynamic in the future
        self.known_objects = []
        self.macro_map = Macro_map(MACRO_X, MACRO_Y, MACRO_TO_MICRO_CONVERSION)
        FORMAT = '%(asctime)s -- %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger('Master controller log')

    def add_detected_object(self, object):
        """add_detected_object adds a detected object to the list of objects the master controller knows about

        Args:
            object (world object): A world object in the simulation
        """
        self.known_objects.append(object)
        self.found_objects += 1

    def request_updated_task_list(self):
        """request_updated_task_list returns the current number of;
        Found objects -- How many objects is the master controller aware of
        Objects identified -- How many identified objects is the master controller aware of
        Objects interacted -- How many objects is the master controller aware of that have been interacted with
        Total objects --- How many objects is the master controller aware of in total
        """
        return(self.found_objects, self.objects_identified, self.object_interacted, self.total_objects)

    def request_macro_map(self):
        """request_macro_map returns the current macro map when requested
        """
        return(self.macro_map)
