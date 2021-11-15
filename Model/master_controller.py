from Model.macro_map import Macro_map
import logging


class Master_controller:
    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
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
        self.known_objects.append(object)
        self.found_objects += 1

    def request_updated_task_list(self):
        return(self.found_objects, self.objects_identified, self.object_interacted, self.total_objects)

    def request_macro_map(self):
        return(self.macro_map)
