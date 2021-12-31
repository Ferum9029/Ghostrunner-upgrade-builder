from field import Field, generate_field_id
import json
from upgrades import upgrades, Upgrade


def find_another_combination(figures: tuple[Upgrade, ...], field, fields: set):
    for figure_index, figure in enumerate(figures):
        for _ in range(4):
            figure.rotate()
            for y, line in enumerate(field):
                for x, value in enumerate(field[y]):
                    if field.is_placeable(figure.shape, x, y):
                        new_field = field.copy()
                        new_field.place_figure(figure.shape, x, y, multiplier=figure.id)
                        new_field_id = generate_field_id(new_field.field)
                        if new_field_id in fields:
                            del new_field
                            continue
                        fields.add(new_field_id)
                        yield from find_another_combination(figures[:figure_index] + figures[figure_index+1:],
                                                            new_field,
                                                            fields)
    yield field


def write_into_file(f, field):
    for line in field:
        f.write(' '.join(str(value) if value // 10 != 0 or value == -1 else ' ' + str(value) for value in line))
        f.write("\n")
    f.write("\n")


def found_fields(start_field: Field, upgrades_to_place: tuple):
    fields = []
    for field in find_another_combination(upgrades_to_place, start_field, set()):
        fields.append(field)

    open("All Upgrades.txt", "w")
    f = open("All Upgrades.txt", "a")
    for field in sorted(fields, key=lambda x: x.count_holes()):
        write_into_file(f, field)
    f.close()


def best_fields(start_field: Field, upgrades_to_place: tuple):
    minimum_holes = len(start_field) * len(start_field[0])
    open("Best Upgrades.txt", "w")
    f = open("Best Upgrades.txt", "a")
    for field in find_another_combination(upgrades_to_place, start_field, set()):
        holes = field.count_holes()
        if minimum_holes >= holes:
            write_into_file(f, holes)
            minimum_holes = holes
    f.close()


def less_holes_than(start_field: Field, upgrades_to_place: tuple):
    maximum_holes = int(input("Less holes than(if <= 0 it will save nothing): "))
    fields = []
    for field in find_another_combination(upgrades_to_place, start_field, set()):
        holes = field.count_holes()
        if maximum_holes > holes:
            fields.append(field)
    open("Min Upgrades.txt", "w")
    f = open("Min Upgrades.txt", "a")
    for field in sorted(fields, key=lambda x: x.count_holes()):
        write_into_file(f, field)
    f.close()


if __name__ == "__main__":
    field_ = Field(json.loads(open('jsons/field.json', 'r').read())['field'])
    modes = (found_fields, best_fields, less_holes_than)
    explanatory_text = "There are 3 modes:\n1 - Saves all found ways to place upgrades. The less holes there is, the higher it will be in the output file\n" \
                       "2 - When script finds a way to place upgrades more efficient or equally to the previous best, it saves it\n" \
                       "3 - You enter a number, then the script finds all ways to set upgrades so the count of holes will be less than your number.\n The less holes there is, the higher it will be\n" \
                       "When the script's done working the window will close itself"
    print(explanatory_text)
    mode = int(input('Mode(number): '))
    upgs = tuple(upgrades[upg_id - 1] for upg_id in map(int, input("Ids of upgrades to place:\n").split()))
    modes[mode-1](field_, upgs)
