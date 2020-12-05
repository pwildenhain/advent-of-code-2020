from typing import List, Literal, Union


# puzzle_input = """FBFBBFFRLR
# BFFFBBFRRR
# FFFBBBFRRR
# BBFFBBFRLL"""

# boarding_passes = puzzle_input.split("\n")


with open("day5/input.txt") as input_file:
    boarding_passes = input_file.read().split("\n")


def split_list_in_half(
    x: List[int], orientation: Union[Literal["lower"], Literal["upper"]]
) -> List[int]:
    list_len = len(x)
    half_list_len = int(list_len / 2)
    return x[:half_list_len] if orientation == "lower" else x[half_list_len:list_len]


def find_row(boarding_pass: str) -> int:
    first_seven = boarding_pass[:7]
    boarding_rows = [num for num in range(128)]
    for orientation in first_seven:
        if orientation == "F":
            boarding_rows = split_list_in_half(boarding_rows, "lower")
        elif orientation == "B":
            boarding_rows = split_list_in_half(boarding_rows, "upper")
    return boarding_rows[0]


def find_column(boarding_pass: str) -> int:
    last_three = boarding_pass[7:10]
    boarding_columns = [num for num in range(8)]
    for orientation in last_three:
        if orientation == "L":
            boarding_columns = split_list_in_half(boarding_columns, "lower")
        elif orientation == "R":
            boarding_columns = split_list_in_half(boarding_columns, "upper")
    return boarding_columns[0]


# Part 1, what is the highest seat id out of all the boarding passes
highest_seat_id = 0
for boarding_pass in boarding_passes:
    seat_id = find_row(boarding_pass) * 8 + find_column(boarding_pass)
    if seat_id > highest_seat_id:
        highest_seat_id = seat_id

print("The highest seat id is:", highest_seat_id)

# Part 2, what is my seat id
seat_ids = sorted(
    [
        find_row(boarding_pass) * 8 + find_column(boarding_pass)
        for boarding_pass in boarding_passes
    ]
)

current_seat_id = seat_ids[0]
my_seat_id = 0
# skip first iteration, since we already have the current seat_id
for seat_id in seat_ids[1:]:
    expected_seat_id = current_seat_id + 1
    if seat_id == expected_seat_id:
        current_seat_id += 1
    else:
        my_seat_id = expected_seat_id
        break

print("My seat id is:", my_seat_id)
