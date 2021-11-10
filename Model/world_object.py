class World_Objects:
    """ A class to handle any world object in the simulation. This does not include agents who will have their own class.
    """

    def __init__(self, micro_x_position: int, micro_y_position: int, macro_x_position: int, macro_y_position: int) -> None:
        """__init__ initializes the object

        Args:
            micro_x_position (int): x position in the micro map
            micro_y_position (int): y position in the micro map
            macro_x_position (int): x position in the macro map
            macro_y_position (int): y position in the macro map
        """
        self.micro_x_position = micro_x_position
        self.micro_y_position = micro_y_position
        self.macro_x_position = macro_x_position
        self.macro_y_position = macro_y_position
        # Bool representing if the object is known to the agents / master controller or not
        self.detected = False

    def set_detected(self):
        self.detected = True


class Marker(World_Objects):
    """Marker a class to representing markers in the simulation

    Args:
        World_Objects (obj): the superclass representing object (except the agents) in the simulation
    """

    def __init__(self, micro_x_position: int, micro_y_position: int, macro_x_position: int, macro_y_position: int) -> None:
        super().__init__(micro_x_position, micro_y_position,
                         macro_x_position, macro_y_position)
        self.interacted = False
        self.identified = False
