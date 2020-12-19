from pprint import pprint

# puzzle_input = """class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50

# your ticket:
# 7,1,14

# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12"""

# puzzle_input = """class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19

# your ticket:
# 11,12,13

# nearby tickets:
# 9,3,18
# 1,15,5
# 14,5,9"""

# rules, my_ticket, nearby_tickets = puzzle_input.split("\n\n")
# Part 1: Find all the invalid values on the nearby tickets. What is their sum?

from typing import List


with open("day16/input.txt") as puzzle_input:
    rules, my_ticket, nearby_tickets = puzzle_input.read().split("\n\n")

rules_dict = {}
for rule in rules.splitlines():
    field, ranges = rule.split(": ")
    lower_range, upper_range = ranges.split(" or ")
    lower_range_min, lower_range_max = [int(num) for num in lower_range.split("-")]
    upper_range_min, upper_range_max = [int(num) for num in upper_range.split("-")]
    rules_dict[field] = (
        range(lower_range_min, lower_range_max + 1),
        range(upper_range_min, upper_range_max + 1),
    )

my_ticket = [int(num) for num in my_ticket.lstrip("your ticket:\n").split(",")]
nearby_tickets = [
    [int(num) for num in nearby_ticket.split(",")]
    for nearby_ticket in nearby_tickets.lstrip("nearby tickets:\n").splitlines()
]


def convert_ticket_to_str(ticket: List[int]) -> str:
    return ",".join([str(num) for num in ticket])


invalid_tickets_dict = {}

for nearby_ticket in nearby_tickets:
    for num in nearby_ticket:
        for ranges in rules_dict.values():
            lower_range, upper_range = ranges
            if num in lower_range or num in upper_range:
                # valid number
                break
        else:
            # went through all the ranges, and didn't find a match
            # print(f"{nearby_ticket=}")
            # print(f"{num=}")
            # print(f"{lower_range=}")
            # print(f"{upper_range=}")
            invalid_tickets_dict[convert_ticket_to_str(nearby_ticket)] = num


print("The sum of the invalid values is:", sum(invalid_tickets_dict.values()))
# Part 2: Figure out the "departure" fields on my ticket and then multiple those
# values together

# Discard invalid tickets:

valid_nearby_tickets = [
    ticket
    for ticket in nearby_tickets
    if convert_ticket_to_str(ticket) not in invalid_tickets_dict
]

possible_field_idxs = {idx: None for idx, _ in enumerate(my_ticket)}
for idx, _ in enumerate(my_ticket):
    # print(f"{field_positions=}")
    idx_qualifying_fields = []
    # # These are all the fields we yet to associate with a position
    # possible_fields = [
    #     field for field, position in field_positions.items() if position is None
    # ]
    # print("possible fields for index", idx, ":", possible_fields)
    # print(idx)
    for nearby_ticket in valid_nearby_tickets:
        num = nearby_ticket[idx]
        # Iterate through our rules to see which fields are appropriate for this
        # specific number
        num_qualifying_fields = set()
        for field, ranges in rules_dict.items():
            # if field in possible_fields:
            lower_range, upper_range = ranges
            # print("Testing if", num, "qualifies for", field, lower_range, upper_range)
            if num in lower_range or num in upper_range:
                # print(num, "qualifies for", field, lower_range, upper_range)
                num_qualifying_fields.add(field)
        # print(num, "qualifies for:", num_qualifying_fields)
        # Add the qualifying fields for this number of this ticket to the
        # overall list for this idx
        # if len(num_qualifying_fields) == 0:
        # print(f"{idx=}")
        # print(f"{nearby_ticket=}")
        # print(f"{num=}")
        idx_qualifying_fields.append(num_qualifying_fields)
    # print(idx_qualifying_fields)
    qualifying_fields = set.intersection(*idx_qualifying_fields)
    # print(idx, "qualifies for", qualifying_fields)
    # Need to figure out what to do at this point...the idx qualifies for multiple
    # fields...🤔 so maybe we should just save all the possbilities for each index
    # and then see if we get any bright ideas from there 💡
    # possibly a main `while` loop that keeps going until we have eliminated
    # all possibilites
    possible_field_idxs[idx] = qualifying_fields

# pprint(possible_field_idxs)
field_positions = {field: None for field in rules_dict}
# Keep iteration through the list, process of elimination style, until all
# the fields have been assigned
while any([value for value in possible_field_idxs.values()]):
    assigned_field_idxs = [
        idx for idx, fields in possible_field_idxs.items() if len(fields) == 1
    ]
    print(f"{assigned_field_idxs=}")
    for idx in assigned_field_idxs:
        # Kick the single value out of the set, leaving it empty for the next iteration
        assigned_field = possible_field_idxs[idx].pop()
        print(f"{assigned_field=}, {idx=}")
        # Also kick that value out all other idx possible values
        for values in possible_field_idxs.values():
            if assigned_field in values:
                values.remove(assigned_field)
        # Lastly, record that we now know the position of this field
        print("Recording", assigned_field, "as position", idx)
        field_positions[assigned_field] = idx
# pprint(possible_field_idxs)
print(field_positions)
depature_field_idxs = [
    value for field, value in field_positions.items() if field.startswith("departure")
]
my_ticket_departure_values = [
    field for idx, field in enumerate(my_ticket) if idx in depature_field_idxs
]
from functools import reduce

print(reduce(lambda x, y: x * y, my_ticket_departure_values))
#
# for nearby_ticket in valid_nearby_tickets:
#     if all(field_positions.values()):
#         # We have a position for every value, we're done here!
#         break
#     print(f"{nearby_ticket=}")
#     for position, num in enumerate(nearby_ticket):
#         if position in field_positions.values():
#             # We already know which field this position is associated with
#             continue
#         # These are all the fields we yet to associate with a position
#         possible_fields = [
#             field for field, position in field_positions.items() if not position
#         ]
#         qualifying_fields = []
#         print("The remaining fields to find are", possible_fields)
#         for field, ranges in rules_dict.items():
#             if len(qualifying_fields) > 1:
#                 # This number qualifies for more than one field
#                 # so we can't know which field it should be associated with
#                 break
#             lower_range, upper_range = ranges
#             if field in possible_fields:
#                 if num in lower_range or num in upper_range:
#                     print(num, "qualifies for", field, lower_range, upper_range)
#                     qualifying_fields.append(field)
#         else:
#             # This number qualifies for exactly one field.
#             # We know that because the loop didn't "break"
#             # and logically _every_ number has to qualify
#             # for at least one of the possible fields.
#             # We can be certain of the position this field
#             # is associated with.
#             field_positions[qualifying_fields[0]] = position
