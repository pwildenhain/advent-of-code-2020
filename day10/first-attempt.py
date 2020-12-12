import math
from pprint import pprint

from itertools import combinations

# puzzle_input = """16
# 10
# 15
# 5
# 1
# 11
# 7
# 19
# 6
# 12
# 4"""

puzzle_input = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

adapters: list = [int(adapter) for adapter in puzzle_input.splitlines()]
# Part 1: Connecting all the adapters in order, what is the product of the number
# of 1 volt and 3 volt differences?
# with open("day10/input.txt") as input_file:
#     adapters: list = [int(adapter) for adapter in input_file.read().splitlines()]
charging_outlet: int = 0
device_adapter: int = max(adapters) + 3
adapters += [charging_outlet, device_adapter]
# Put the adapters in the proper order
adapters_in_order: list = sorted(adapters)
print(adapters_in_order)
adapter_next_diffs: dict = {1: [], 2: [], 3: []}
mandatory_adapters = []
optional_adapters = []
highest_current_adapter = 0
for adapter_idx, adapter in enumerate(adapters_in_order):
    next_adapter = adapters_in_order[adapter_idx + 1]

    if next_adapter == device_adapter:
        # end of list, break out so we don't get an IndexError when
        # try to look ahead
        adapter_next_diffs[3] += [device_adapter]
        mandatory_adapters += [device_adapter]
        break

    adapter_diff = next_adapter - adapter
    adapter_next_diffs[adapter_diff] += [next_adapter]
    highest_adapter_diff = adapter - highest_current_adapter
    if adapter_diff == 3:
        # Both the current _and_ next adapter are a needed pair
        mandatory_adapters += [adapter, next_adapter]
        highest_current_adapter = next_adapter
    if highest_adapter_diff == 3:
        mandatory_adapters += [highest_current_adapter, adapter]
        highest_current_adapter = adapter

print(
    "The number of 1-jolt difference multiplied by the number of 3-jolt differences is:",
    len(adapter_next_diffs[1]) * len(adapter_next_diffs[3]),
)

# Part 2: What are all the valid ways that the adapters can be connected?
# remove duplicate values
mandatory_adapters = set(mandatory_adapters)
optional_adapters = mandatory_adapters.symmetric_difference(adapters_in_order)
# optional_adapters.remove(0)
# convert back to lists for easy indexing
mandatory_adapters = sorted(mandatory_adapters)
optional_adapters = list(optional_adapters)
# remove the charging outlet
# optional_adapters.remove(charging_outlet)
############ testing
# optional_adapters.add(48)
############
print(f"{mandatory_adapters=}")
print(f"{optional_adapters=}")
fully_optional_adapters = []
mandatory_adapter_idx = 0
next_mandatory_adapter_idx = 1

while next_mandatory_adapter_idx < len(mandatory_adapters):
    mandatory_adapter = mandatory_adapters[mandatory_adapter_idx]
    next_mandatory_adapter = mandatory_adapters[next_mandatory_adapter_idx]

    potential_fully_optional_adapters = []
    for optional_adapter in optional_adapters:
        # print(f"{mandatory_adapter=}, {next_mandatory_adapter=}, {optional_adapter=}")
        if len(potential_fully_optional_adapters) == 2:
            fully_optional_adapters += potential_fully_optional_adapters
            break
        if optional_adapter in range(mandatory_adapter, next_mandatory_adapter):
            potential_fully_optional_adapters += [optional_adapter]

    mandatory_adapter_idx += 1
    next_mandatory_adapter_idx += 1
# I think I'm on to something with the non-fully optional adapters. Just need to keep
# plugging away.
#
# Still need to figure out how to get 48 into the optional_adapters list
# and then compare that to the fully_optional_adapters list when creating combinations?
# The answer might be to just brute force it and let my computer run for
# 10 hours :-)
print(f"{fully_optional_adapters=}")
all_possible_combos = []
all_possible_num_optional_adapters = range(1, len(optional_adapters))
for num_optional_adapters in all_possible_num_optional_adapters:
    all_possible_combos += list(combinations(optional_adapters, num_optional_adapters))

# Add two to the total to account for include no optional adapters or all optional adapters
# pprint(all_possible_combos[:100])
print(len(all_possible_combos) + 2)
