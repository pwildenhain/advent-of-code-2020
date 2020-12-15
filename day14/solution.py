from typing import List
import parse
from itertools import product

# puzzle_input = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0"""
# puzzle_input = """mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1"""

# steps = puzzle_input.splitlines()
with open("day14/input.txt") as puzzle_input:
    steps = puzzle_input.read().splitlines()

MASK = ""
MEM = {}
# Part 1: What is the sum of all the values left in memory after running the program?
for step in steps:
    if step.startswith("mask"):
        MASK = step[7:]
    else:
        mem_dict = parse.search("mem[{address:d}] = {value:d}", step).named
        address = mem_dict["address"]
        value = format(mem_dict["value"], "b")
        # fill in remaining 0 values
        value = value.zfill(36)
        # apply the mask, by iterating backwards
        masked_value = ""
        for idx, bit in enumerate(value):
            if MASK[idx] != "X":
                masked_value += MASK[idx]
            else:
                # Use the value idx
                masked_value += value[idx]

        MEM[address] = masked_value

masked_values_total = sum([int("0b" + mask_value, 2) for mask_value in MEM.values()])

print(masked_values_total)
# Part 2: Using version 2, what is the sum of all the values left
# in memory after running the program?.
def find_floating_addresses(masked_address: str) -> List[str]:
    num_floating_bits = masked_address.count("X")
    all_possible_floating_bits = product(["0", "1"], repeat=num_floating_bits)
    floating_addresses = []
    for floating_bits in all_possible_floating_bits:
        bits_list = list(floating_bits)
        floating_address = [
            bit if bit != "X" else bits_list.pop() for bit in masked_address
        ]
        floating_addresses.append("".join(floating_address))

    return floating_addresses


MASK = ""
MEM = {}

for step in steps:
    if step.startswith("mask"):
        MASK = step[7:]
    else:
        mem_dict = parse.search("mem[{address:d}] = {value:d}", step).named
        address = format(mem_dict["address"], "b")
        value = mem_dict["value"]
        # fill in remaining 0 values
        address = address.zfill(36)
        # apply the mask, by iterating backwards
        masked_address = ""
        for idx, bit in enumerate(address):
            if MASK[idx] != "0":
                masked_address += MASK[idx]
            else:
                # Use the address idx
                masked_address += address[idx]

        floating_addresses = find_floating_addresses(masked_address)

        for floating_address in floating_addresses:
            MEM[floating_address] = value

masked_values_total = sum([value for value in MEM.values()])

print(masked_values_total)
