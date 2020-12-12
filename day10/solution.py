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

# puzzle_input = """28
# 33
# 18
# 42
# 31
# 14
# 46
# 20
# 48
# 47
# 24
# 23
# 49
# 45
# 19
# 38
# 39
# 11
# 1
# 32
# 25
# 35
# 8
# 17
# 7
# 9
# 4
# 2
# 34
# 10
# 3"""

# adapters: list = [int(adapter) for adapter in puzzle_input.splitlines()]
# Part 1: Connecting all the adapters in order, what is the product of the number
# of 1 volt and 3 volt differences?
with open("day10/input.txt") as input_file:
    adapters: list = [int(adapter) for adapter in input_file.read().splitlines()]
charging_outlet: int = 0
device_adapter: int = max(adapters) + 3
adapters += [charging_outlet, device_adapter]
# Put the adapters in the proper order
ADAPTERS_IN_ORDER: list = sorted(adapters)
print(ADAPTERS_IN_ORDER)
adapter_jump_nums: dict = {1: [], 2: [], 3: []}
for adapter_idx, adapter in enumerate(ADAPTERS_IN_ORDER):
    next_adapter = ADAPTERS_IN_ORDER[adapter_idx + 1]

    if next_adapter == device_adapter:
        # end of list, break out so we don't get an IndexError when
        # try to look ahead
        adapter_jump_nums[3] += [device_adapter]
        break

    adapter_diff = next_adapter - adapter
    adapter_jump_nums[adapter_diff] += [next_adapter]

print(
    "The number of 1-jolt difference multiplied by the number of 3-jolt differences is:",
    len(adapter_jump_nums[1]) * len(adapter_jump_nums[3])
)

# Part 2: The first part is all me 🙌 but the next part comes
# courtesy of: https://www.youtube.com/watch?v=cE88K2kFZn0 🙇‍♀️

POSSIBLE_PATHS = {}
print(f"{ADAPTERS_IN_ORDER=}")
def find_number_of_paths_to_end(adapter_idx):
    if adapter_idx == len(ADAPTERS_IN_ORDER) - 1:
        # made it to the end of the list 🎉 only one way to go from here
        print("End of the list")
        return 1
    
    if adapter_idx in POSSIBLE_PATHS.keys():
        # We've seen this index before 👀 and already calculated how many possible paths
        # we can take the reach the end
        print("We've already calculated possible paths from", adapter_idx, "it's", POSSIBLE_PATHS[adapter_idx])
        return POSSIBLE_PATHS[adapter_idx]
    # Otherwise, we need to calculate 🤖 how many possible paths we can take to get to the
    # end from our current position
    num_paths = 0
    for next_adapter_idx in range(adapter_idx + 1, len(ADAPTERS_IN_ORDER)):
        if ADAPTERS_IN_ORDER[next_adapter_idx] - ADAPTERS_IN_ORDER[adapter_idx] <= 3:
            print("Finding possible paths for", next_adapter_idx)
            num_paths += find_number_of_paths_to_end(next_adapter_idx)
        else:
            # we're more than 3 steps away, no more possible paths 🙅‍♂️
            print("We're more than 3 steps away, no more possible paths")
            break
    # Once we have calculated the number of paths, let's remember the answer from this
    # index, so if we end up here again, we don't have to recalculate
    print("Remembering number of possible paths for", adapter_idx)
    POSSIBLE_PATHS[adapter_idx] = num_paths
    print("There are", num_paths, "possible paths for", adapter_idx)
    return num_paths

print(find_number_of_paths_to_end(0))