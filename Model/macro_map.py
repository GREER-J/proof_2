class Macro_map:
    """ A class to handle the macro map representation for both agents and the macro controller
    """

    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int) -> None:
        """__init__ creates a new macro map

        Args:
            MACRO_X (int): The length of the macro map in the x direction
            MACRO_Y (int): The length of the macro map in the y direction
            MACRO_TO_MICRO_CONVERSION (int): The number of micro steps for every macro step
        """
        self.macro_map = []
        self.MACRO_TO_MICRO_CONVERSION = MACRO_TO_MICRO_CONVERSION
        for x in range(MACRO_X):
            row = []
            for y in range(MACRO_Y):
                row.append(macro_map_square(x, y, MACRO_TO_MICRO_CONVERSION))
            self.macro_map.append(row)

    def get_cell_obj_from_macro(self, MACRO_X: int, MACRO_Y: int):
        """get_cell_obj_from_macro returns an the macro square object in a given x,y position

        Args:
            MACRO_X (int): The x position of the desired macro square
            MACRO_Y (int): The y position of the desired macro square
        """
        return(self.macro_map[MACRO_X][MACRO_Y])


class macro_map_square:
    """ A class to handle the macro squares contained within the macro map
    """

    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int):
        """__init__ creates a new macro square

        Args:
            MACRO_X (int): The x position of the macro square
            MACRO_Y (int): The y position of the macro square
            MACRO_TO_MICRO_CONVERSION (int): The number of micro steps for every macro step
        """
        self.MACRO_X = MACRO_X
        self.MACRO_Y = MACRO_Y
        self.micro_x_pos_center = int(
            (MACRO_X + 0.5) * MACRO_TO_MICRO_CONVERSION)
        self.micro_y_pos_center = int(
            (MACRO_Y + 0.5) * MACRO_TO_MICRO_CONVERSION)
        self.objects_in_square = []
        self.searched = False
        self.contains_objects = False
        self.assigned = False

    def add_object_to_macro_square(self, object_to_add):
        """add_object_to_macro_square adds a new object to the list of objects in the macro square

        Args:
            object_to_add (world object): A world object in the simulation
        """
        self.contains_objects = True
        self.objects_in_square.append(object_to_add)

    def mark_as_assigned(self):
        """mark_as_assigned marks this square as assigned to an agent
        """
        self.assigned = True

    def release_from_marked_as_assigned(self):
        """release_from_marked_as_assigned marks this square as no longer assigned to an agent
        """
        self.assigned = False

    def mark_as_searched(self):
        """mark_as_searched marks this square as searched
        """
        self.searched = True
