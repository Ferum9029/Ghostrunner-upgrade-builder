def generate_field_id(field: list[list, ...]) -> int:
    result = []
    for row in field:
        id_ = bin(row[0])
        for i in row[1:]:
            id_ += bin(i)
        result.append(id_)
    return hash(tuple(result))


class Field:
    def __init__(self, field: list[list, ...]):
        self.field = field

    def is_placeable(self, figure, x: int, y: int) -> bool:
        if len(self)-1 < y + len(figure) - 1 or len(self[0])-1 < x + len(figure[0]) - 1:
            return False

        placeable = True
        for figure_y, figure_row in enumerate(figure):
            for figure_x, figure_value in enumerate(figure_row):
                if not bool(self[y + figure_y][x + figure_x]) <= figure_value:
                    placeable = False
        return placeable

    def place_figure(self, figure, x: int, y: int, multiplier: int = 1) -> None:
        for figure_y, figure_row in enumerate(figure):
            for figure_x, figure_value in enumerate(figure_row):
                field_value = self.field[y+figure_y][x + figure_x]
                mlt = -1 if field_value == -1 else multiplier if not field_value else field_value
                self[y+figure_y][x + figure_x] = (figure_value <= (bool(field_value)))*mlt

    def count_holes(self) -> int:
        c = 0
        for line in self.field:
            for value in line:
                if not value:
                    c += 1
        return c

    def copy(self):
        return Field([i.copy() for i in self.field])

    def __iter__(self):
        return iter(self.field)

    def __getitem__(self, item):
        return self.field[item]

    def __len__(self):
        return len(self.field)
