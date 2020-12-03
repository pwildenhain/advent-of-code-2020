# puzzle_input = """..##.......
# #...#...#..
# .#....#..#.
# ..#.#...#.#
# .#...##..#.
# ..#.##.....
# .#.#.#....#
# .#........#
# #.##...#...
# #...##....#
# .#..#...#.#"""

# Part 1, how many trees do we encounter?
tree_map = []
with open("day3/input.txt") as input_file:    
    for row in input_file.readlines():
        tree_map += [[char for char in row if char != "\n"]]
# How the toboggan moves
down_inc = 1
right_inc = 3
# Expand the map
map_height = len(tree_map)
map_width = len(tree_map[0])
map_multipler = int((map_height * right_inc // map_width) / down_inc) + 1
print(map_multipler)
for row_num, row in enumerate(tree_map):
    tree_map[row_num] = row * map_multipler
# Where the toboggan starts
down_idx = 0
right_idx = 0

num_trees_encountered = 0
for row in tree_map:
    if tree_map[down_idx][right_idx] == "#":
        num_trees_encountered += 1
    down_idx += down_inc
    right_idx += right_inc

print("Encountered", num_trees_encountered, "trees")

# Part 2, how many trees do we encounter with different slopes?
tree_map = []
with open("day3/input.txt") as input_file:    
    for row in input_file.readlines():
        tree_map += [[char for char in row if char != "\n"]]
slopes = [(1, 1), (1, 3), (1, 5), (1, 7), (2, 1)]
slope_product = 1
map_height = len(tree_map)
map_width = len(tree_map[0])
for down_inc, right_inc in slopes:
    map_multipler = int((map_height * right_inc // map_width) / down_inc) + 1
    new_map = []
    for row_num, row in enumerate(tree_map):
        new_map += [row * map_multipler]
    # Where the toboggan starts
    down_idx = 0
    right_idx = 0

    num_trees_encountered = 0
    for row_num, row in enumerate(new_map):
        # check to see if we can skip this row
        if row_num % down_inc != 0:
            continue

        if new_map[down_idx][right_idx] == "#":
            num_trees_encountered += 1

        down_idx += down_inc
        right_idx += right_inc
    
    slope_product *= num_trees_encountered

print("The slopes product is:", slope_product)