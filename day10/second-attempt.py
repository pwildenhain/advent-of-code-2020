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
adapter_jump_nums: dict = {1: [], 2: [], 3: []}
for adapter_idx, adapter in enumerate(adapters_in_order):
    next_adapter = adapters_in_order[adapter_idx + 1]

    if next_adapter == device_adapter:
        # end of list, break out so we don't get an IndexError when
        # try to look ahead
        adapter_jump_nums[3] += [device_adapter]
        break

    adapter_diff = next_adapter - adapter
    adapter_jump_nums[adapter_diff] += [next_adapter]

print(
    "The number of 1-jolt difference multiplied by the number of 3-jolt differences is:",
    len(adapter_jump_nums[1]) * len(adapter_jump_nums[3]),
)
# Part 2:

single_jump_runs = []
single_jump_run = []
for adapter_idx, adapter in enumerate(adapters_in_order):
    # # Don't bother with end
    if adapter == device_adapter:
        continue

    next_adapter = adapters_in_order[adapter_idx + 1]

    if next_adapter - adapter == 1:
        single_jump_run += [adapter]
    else:
        # have to skip the first value of the single jump run, it's required
        if len(single_jump_run) > 1:
            single_jump_runs += [single_jump_run[1 : len(single_jump_run)]]
        # reset the run
        single_jump_run = []

print(f"{single_jump_runs=}")
# create combos for each single jump run
# filter our empty combos
# the minimumn length of the combo is len(combo) - 2, minimum of one
#   so a run of three could go down to one
#   a run of four could go down to 2
#   a run of five could go down to three
distinct_arrangements = []
for single_jump_run in single_jump_runs:
    min_num_adapters = len(single_jump_run) - 2 if len(single_jump_runs) > 2 else 1
    all_possible_num_optional_adapters = (
        range(min_num_adapters, len(single_jump_run))
        if len(single_jump_run) > 2
        else range(1, 2)
    )
    # print(f"{single_jump_run=}")
    # print(f"{min_num_adapters=}")
    # print(f"{all_possible_num_optional_adapters=}")
    for num_optional_adapters in all_possible_num_optional_adapters:
        # print(f"    {num_optional_adapters}")
        # print(f"    {list(combinations(single_jump_run, num_optional_adapters))}")
        distinct_arrangements += list(combinations(single_jump_run, num_optional_adapters))

print(distinct_arrangements)
