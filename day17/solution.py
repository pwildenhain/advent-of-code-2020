from typing import Dict, List, Set, Tuple
from itertools import product

from pprint import pprint
# puzzle_input = """.#.
# ..#
# ###"""

puzzle_input = open("day17/input.txt").read()


# cubes start on the 0 plane (z)
activated_cubes = {
    (x, y, 0)
    for y, col in enumerate(puzzle_input.splitlines())
    for x, row in enumerate(col)
    if row == "#"
}

deactivated_cubes = {
    (x, y, 0)
    for y, col in enumerate(puzzle_input.splitlines())
    for x, row in enumerate(col)
    if row == "."
}

def find_3d_neighbors(cube: Tuple[int, int, int]) -> Set[Tuple[int, int, int]]:
    x, y, z = cube
    neighbor_distances = [-1, 0, 1]
    x_neighbors = [x + distance for distance in neighbor_distances]
    y_neighbors = [y + distance for distance in neighbor_distances]
    z_neighbors = [z + distance for distance in neighbor_distances]
    cube_neighbors = product(x_neighbors, y_neighbors, z_neighbors)
    # Filter out the original cube from the return value
    return {cube_neighbor for cube_neighbor in cube_neighbors if cube_neighbor != cube}

# Also should include the deactivated neighbors of all the currently activated cubes
addl_deactivated_cubes = {
    cube_neighbor
    for activated_cube in activated_cubes
    for cube_neighbor in find_3d_neighbors(activated_cube)
    if cube_neighbor not in activated_cubes
}
# pprint(addl_deactivated_cubes)
deactivated_cubes.update(addl_deactivated_cubes)


def simulate_3d_cycle(
    cubes: Dict[str, Set[Tuple[int, int, int]]]
) -> Dict[str, Set[Tuple[int, int, int]]]:
    activated_cubes = set()
    deactivated_cubes = set()
    all_cubes = [cube for all_cubes in cubes.values() for cube in all_cubes]
    # print(all_cubes)
    for cube in all_cubes:
        # print(cube)
        cube_is_activated = cube in cubes["activated cubes"]
        cube_neighbors = find_3d_neighbors(cube)
        activated_neighbors = set()
        for cube_neigbor in cube_neighbors:
            if cube_neigbor in cubes["activated cubes"]:
                activated_neighbors.add(cube_neigbor)
        # print(f"{'Activated' if cube_is_activated else 'Deactivated'} cube", cube, "has the following activated neighbors", activated_neighbors)
        if len(activated_neighbors) in [2, 3] and cube_is_activated:
            # print("Cube", cube, "is activated")
            activated_cubes.add(cube)
        elif len(activated_neighbors) == 3 and not cube_is_activated:
            # print("Cube", cube, "is activated")
            activated_cubes.add(cube)
        else:
            # print("Cube", cube, "is deactivated")
            deactivated_cubes.add(cube)
  
    return {"activated cubes": activated_cubes, "deactivated cubes": deactivated_cubes}

cubes_dict = {"activated cubes": activated_cubes, "deactivated cubes": deactivated_cubes}
cycle_num = 0

while cycle_num < 6:
    cubes_dict = simulate_3d_cycle(cubes_dict)
    # Expand our boundaries to all the neighbors of the currently activated cubes
    addl_deactivated_cubes = {
        cube_neighbor
        for activated_cube in cubes_dict["activated cubes"]
        for cube_neighbor in find_3d_neighbors(activated_cube)
        if cube_neighbor not in cubes_dict["activated cubes"]
    }
    cubes_dict["deactivated cubes"].update(addl_deactivated_cubes)
    cycle_num += 1

print(len(cubes_dict["activated cubes"]))
# Part 2: We're working in 4 dimensions, not 3
def find_4d_neighbors(cube: Tuple[int, int, int, int]) -> Set[Tuple[int, int, int, int]]:
    x, y, z, w = cube
    neighbor_distances = [-1, 0, 1]
    x_neighbors = [x + distance for distance in neighbor_distances]
    y_neighbors = [y + distance for distance in neighbor_distances]
    z_neighbors = [z + distance for distance in neighbor_distances]
    w_neighbors = [w + distance for distance in neighbor_distances]
    cube_neighbors = product(x_neighbors, y_neighbors, z_neighbors, w_neighbors)
    # Filter out the original cube from the return value
    return {cube_neighbor for cube_neighbor in cube_neighbors if cube_neighbor != cube}

# print(len(find_4d_neighbors((0, 0, 0, 0))))
# works, got 80
# cubes start on the 0 plane (z)
activated_cubes = {
    (x, y, 0, 0)
    for y, col in enumerate(puzzle_input.splitlines())
    for x, row in enumerate(col)
    if row == "#"
}

deactivated_cubes = {
    (x, y, 0, 0)
    for y, col in enumerate(puzzle_input.splitlines())
    for x, row in enumerate(col)
    if row == "."
}

# Also should include the deactivated neighbors of all the currently activated cubes
addl_deactivated_cubes = {
    cube_neighbor
    for activated_cube in activated_cubes
    for cube_neighbor in find_4d_neighbors(activated_cube)
    if cube_neighbor not in activated_cubes
}
# pprint(addl_deactivated_cubes)
deactivated_cubes.update(addl_deactivated_cubes)


def simulate_4d_cycle(
    cubes: Dict[str, Set[Tuple[int, int, int]]]
) -> Dict[str, Set[Tuple[int, int, int]]]:
    activated_cubes = set()
    deactivated_cubes = set()
    all_cubes = [cube for all_cubes in cubes.values() for cube in all_cubes]
    # print(all_cubes)
    for cube in all_cubes:
        # print(cube)
        cube_is_activated = cube in cubes["activated cubes"]
        cube_neighbors = find_4d_neighbors(cube)
        activated_neighbors = set()
        for cube_neigbor in cube_neighbors:
            if cube_neigbor in cubes["activated cubes"]:
                activated_neighbors.add(cube_neigbor)
        # print(f"{'Activated' if cube_is_activated else 'Deactivated'} cube", cube, "has the following activated neighbors", activated_neighbors)
        if len(activated_neighbors) in [2, 3] and cube_is_activated:
            # print("Cube", cube, "is activated")
            activated_cubes.add(cube)
        elif len(activated_neighbors) == 3 and not cube_is_activated:
            # print("Cube", cube, "is activated")
            activated_cubes.add(cube)
        else:
            # print("Cube", cube, "is deactivated")
            deactivated_cubes.add(cube)
  
    return {"activated cubes": activated_cubes, "deactivated cubes": deactivated_cubes}

cubes_dict = {"activated cubes": activated_cubes, "deactivated cubes": deactivated_cubes}
cycle_num = 0

while cycle_num < 6:
    cubes_dict = simulate_4d_cycle(cubes_dict)
    # Expand our boundaries to all the neighbors of the currently activated cubes
    addl_deactivated_cubes = {
        cube_neighbor
        for activated_cube in cubes_dict["activated cubes"]
        for cube_neighbor in find_4d_neighbors(activated_cube)
        if cube_neighbor not in cubes_dict["activated cubes"]
    }
    cubes_dict["deactivated cubes"].update(addl_deactivated_cubes)
    cycle_num += 1

print(len(cubes_dict["activated cubes"]))