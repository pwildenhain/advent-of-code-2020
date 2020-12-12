from copy import deepcopy
from pprint import pprint
from typing import List, Tuple

# puzzle_input = """L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL"""

# puzzle_input = """#.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##"""

# seat_map = [[char for char in row] for row in puzzle_input.splitlines()]
# Part 1: Given the seating rules, what is the stable number of occupied seats?
with open("day11/input.txt") as input_file:
    seat_map = [[char for char in row] for row in input_file.read().splitlines()]


def seat_is_filled(map_dict: dict, location: Tuple[int, int]) -> bool:
    row_idx, col_idx = location
    seat_filled = False
    if row_idx < 0 or col_idx < 0:
        # not on the map
        return False
    try:
        if map_dict[row_idx][col_idx] == "#":
            seat_filled = True
    except IndexError:
        # Not on the map
        pass
    return seat_filled


def find_number_occupied_adjacent_seats(
    map_dict: dict, location: Tuple[int, int]
) -> int:
    row_idx, col_idx = location

    row_above = row_idx - 1
    row_below = row_idx + 1
    right_col = col_idx + 1
    left_col = col_idx - 1
    # breakpoint()
    return sum(
        [
            # top
            seat_is_filled(map_dict, location=(row_above, col_idx)),
            # top right
            seat_is_filled(map_dict, location=(row_above, right_col)),
            # right
            seat_is_filled(map_dict, location=(row_idx, right_col)),
            # bottom right
            seat_is_filled(map_dict, location=(row_below, right_col)),
            # bottom
            seat_is_filled(map_dict, location=(row_below, col_idx)),
            # bottom left
            seat_is_filled(map_dict, location=(row_below, left_col)),
            # left
            seat_is_filled(map_dict, location=(row_idx, left_col)),
            # top left
            seat_is_filled(map_dict, location=(row_above, left_col)),
        ]
    )


def simulate_round_part_one(map_dict: dict) -> Tuple[list, list]:
    seats_to_be_filled: List[Tuple[int, int]] = []
    seats_to_be_emptied: List[Tuple[int, int]] = []

    for row_num, row in enumerate(map_dict):
        for col_num, col in enumerate(row):
            if col == ".":
                # it's the floor, no one can sit here
                continue

            current_seat = (row_num, col_num)
            num_occupied_adjacent_seats = find_number_occupied_adjacent_seats(
                map_dict, current_seat
            )
            current_seat_is_empty = not seat_is_filled(map_dict, current_seat)
            if current_seat_is_empty and num_occupied_adjacent_seats == 0:
                seats_to_be_filled += [current_seat]
            elif not current_seat_is_empty and num_occupied_adjacent_seats >= 4:
                seats_to_be_emptied += [current_seat]

    return (seats_to_be_filled, seats_to_be_emptied)


seat_map_part_1 = deepcopy(seat_map)
filled_seats, empty_seats = (True, True)
while filled_seats or empty_seats:
    filled_seats, empty_seats = simulate_round_part_one(seat_map_part_1)
    # Update the map
    for row_idx, col_idx in filled_seats:
        seat_map_part_1[row_idx][col_idx] = "#"
    for row_idx, col_idx in empty_seats:
        seat_map_part_1[row_idx][col_idx] = "L"

    # print(f"{filled_seats=}")
else:
    stable_num_occupied_seats_part_1 = [
        char for row in seat_map_part_1 for char in row
    ].count("#")

print("The stable number of occupied seats is:", stable_num_occupied_seats_part_1)
# Part 2: Given the _new_ seating rules, what is the stable number of occupied seats?
def location_is_floor(map_dict: dict, location: Tuple[int, int]) -> bool:
    row_idx, col_idx = location
    is_floor = False
    if row_idx < 0 or col_idx < 0:
        # not on the map
        return False
    try:
        if map_dict[row_idx][col_idx] == ".":
            is_floor = True
    except IndexError:
        # Not on the map
        pass

    return is_floor


def find_number_occupied_straight_visible_seats(
    map_dict: dict, straight_path: List[int], anchor: str, anchor_idx: int
) -> bool:
    for idx in straight_path:
        location = (anchor_idx, idx) if anchor == "row" else (idx, anchor_idx)
        if not location_is_floor(map_dict, location):
            # can only see the _first_ available seat
            return seat_is_filled(map_dict, location)

    return 0


def find_number_occupied_diagonal_visible_seats(
    map_dict: dict, diagonal_path: List[int]
) -> bool:
    for row_idx, col_idx in diagonal_path:
        location = (row_idx, col_idx)
        if not location_is_floor(map_dict, location):
            # can only see the _first_ available seat
            return seat_is_filled(map_dict, location)

    return 0


def find_number_occupied_visible_seats(
    map_dict: dict, location: Tuple[int, int]
) -> int:
    row_idx, col_idx = location
    top_row = 0
    bottom_row = len(map_dict)
    leftmost_col = 0
    rightmost_col = len(map_dict[0])
    rows_above = list(reversed(range(top_row, row_idx)))
    rows_below = list(range(row_idx + 1, bottom_row))
    right_cols = list(range(col_idx + 1, rightmost_col))
    left_cols = list(reversed(range(leftmost_col, col_idx)))
    top_left_diagonals = list(zip(rows_above, left_cols))
    bottom_left_diagonals = list(zip(rows_below, left_cols))
    bottom_right_diagonals = list(zip(rows_below, right_cols))
    top_right_diagonals = list(zip(rows_above, right_cols))
    return sum(
        [
            find_number_occupied_straight_visible_seats(
                map_dict, rows_above, anchor="col", anchor_idx=col_idx
            ),
            find_number_occupied_straight_visible_seats(
                map_dict, rows_below, anchor="col", anchor_idx=col_idx
            ),
            find_number_occupied_straight_visible_seats(
                map_dict, right_cols, anchor="row", anchor_idx=row_idx
            ),
            find_number_occupied_straight_visible_seats(
                map_dict, left_cols, anchor="row", anchor_idx=row_idx
            ),
            find_number_occupied_diagonal_visible_seats(map_dict, top_left_diagonals),
            find_number_occupied_diagonal_visible_seats(
                map_dict, bottom_left_diagonals
            ),
            find_number_occupied_diagonal_visible_seats(
                map_dict, bottom_right_diagonals
            ),
            find_number_occupied_diagonal_visible_seats(map_dict, top_right_diagonals),
        ]
    )


def simulate_round_part_two(map_dict: dict) -> Tuple[list, list]:
    seats_to_be_filled: List[Tuple[int, int]] = []
    seats_to_be_emptied: List[Tuple[int, int]] = []

    for row_num, row in enumerate(map_dict):
        for col_num, col in enumerate(row):
            if col == ".":
                # it's the floor, no one can sit here
                continue

            current_seat = (row_num, col_num)
            num_occupied_adjacent_seats = find_number_occupied_visible_seats(
                map_dict, current_seat
            )
            current_seat_is_empty = not seat_is_filled(map_dict, current_seat)
            if current_seat_is_empty and num_occupied_adjacent_seats == 0:
                seats_to_be_filled += [current_seat]
            # it now takes 5 or more rather than 4 or more
            elif not current_seat_is_empty and num_occupied_adjacent_seats >= 5:
                seats_to_be_emptied += [current_seat]

    return (seats_to_be_filled, seats_to_be_emptied)


seat_map_part_2 = deepcopy(seat_map)
filled_seats, empty_seats = (True, True)
while filled_seats or empty_seats:
    filled_seats, empty_seats = simulate_round_part_two(seat_map_part_2)
    # Update the map
    for row_idx, col_idx in filled_seats:
        seat_map_part_2[row_idx][col_idx] = "#"
    for row_idx, col_idx in empty_seats:
        seat_map_part_2[row_idx][col_idx] = "L"
else:
    stable_num_occupied_seats_part_2 = [
        char for row in seat_map_part_2 for char in row
    ].count("#")
# Right now the number is too high. Debug later (today)
print("The stable number of occupied seats is:", stable_num_occupied_seats_part_2)
