class Macro_map:
    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int):
        self.macro_map = []
        self.MACRO_TO_MICRO_CONVERSION = MACRO_TO_MICRO_CONVERSION
        for x in range(MACRO_X):
            row = []
            for y in range(MACRO_Y):
                row.append(macro_map_square(x, y, MACRO_TO_MICRO_CONVERSION))
            self.macro_map.append(row)

    def get_cell_obj_from_macro(self, MACRO_X: int, MACRO_Y: int):
        return(self.macro_map[MACRO_X][MACRO_Y])


class macro_map_square:
    def __init__(self, MACRO_X: int, MACRO_Y: int, MACRO_TO_MICRO_CONVERSION: int):
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
        self.contains_objects = True
        self.objects_in_square.append(object_to_add)

    def mark_as_assigned(self):
        self.assigned = True

    def release_from_marked_as_assigned(self):
        self.assigned = False

    def mark_as_searched(self):
        self.searched = True
