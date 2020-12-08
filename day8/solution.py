# puzzle_input = """nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6"""

import copy
with open("day8/input.txt") as input_file:
    puzzle_input = input_file.read()

game_instructions = []

for step in puzzle_input.split("\n"):
    command, value = step.split(" ")
    game_instructions += [[command, int(value)]]
# Part 1, what is the value of the "accumulator" immediately before the program
# would run an instruction for the second time (i.e proceed to an infinte loop)?
def run_program(instructions):
    end_of_instructions = len(instructions)
    accumulator_value = 0
    steps_executed = []
    step = 0
    # print(instructions)
    while step not in steps_executed:
        if step == end_of_instructions:
            return accumulator_value
        steps_executed += [step]
        command, value = instructions[step]
        if command == "acc":
            accumulator_value += value
            step += 1
        elif command == "jmp":
            step += value
        elif command == "nop":
            step += 1
    
    raise ValueError(f"Infinite loop detected. {accumulator_value=}")

try:
    run_program(game_instructions)
except ValueError as e:
    print(e)

# Part 2, which jmp/nop has to be swapped in order to correctly run this program
# escaping the infinite loop?

# Brute force it...by swapping one instruction at a time until the program runs.
# Not elegant at all, and I'm sure I'm missing some pattern that would help me
# narrow down which instructions to modify but hey it's 12:30 am, cut me some slack
jmp_idxs = []
nop_idxs = []
for idx, _ in enumerate(game_instructions):
    command, value = game_instructions[idx]
    if command == "jmp":
        jmp_idxs += [idx]
    elif command == "nop":
        nop_idxs += [idx]

# Try swapping jmps first:
for jmp_idx in jmp_idxs:
    new_game_instructions = copy.deepcopy(game_instructions)
    # Swap jmp for nop
    new_game_instructions[jmp_idx][0] = "nop"
    try:
        accumulator_value = run_program(new_game_instructions)
    except ValueError as e:
        continue
try:
    print(f"{accumulator_value=}")
    quit()
except NameError:
    # Looks like it didn't work with the jmps, time to try the nops
    pass

for nop_idx in nop_idxs:
    new_game_instructions = copy.deepcopy(game_instructions)
    # Swap jmp for nop
    new_game_instructions[nop_idx][0] = "nop"
    try:
        accumulator_value = run_program(new_game_instructions)
    except ValueError as e:
        continue

print(f"{accumulator_value=}")
