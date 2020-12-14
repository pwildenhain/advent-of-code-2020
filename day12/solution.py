from collections import namedtuple

Instruction = namedtuple("Instruction", ["direction", "magnitude"])
# puzzle_input = """F10
# N3
# F7
# R90
# F11"""


# instructions = [
#     Instruction(direction=step[0], magnitude=int(step[1 : len(step)]))
#     for step in puzzle_input.splitlines()
# ]

# Part 1: Following the instructions, where do we end up?
with open("day12/input.txt") as puzzle_input:
    instructions = [
        Instruction(direction=step[0], magnitude=int(step[1 : len(step)]))
        for step in puzzle_input.read().splitlines()
    ]


class Ferry:
    def __init__(self, instructions: list) -> None:
        # Treat direction facing as an angle
        self._direction_facing = 0
        self._direction_facing_lookup = {0: "E", 1: "N", 2: "W", 3: "S"}
        self._direction_opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        self._direction_procedure_lookup = {
            "N": self.move_cardinal_position,
            "S": self.move_cardinal_position,
            "E": self.move_cardinal_position,
            "W": self.move_cardinal_position,
            "F": self.move_relative_position,
            "R": self.shift_direction_facing,
            "L": self.shift_direction_facing,
        }
        self.instructions = instructions
        self.location = {"N": 0, "S": 0, "E": 0, "W": 0}

    def _move_position(self, direction, magnitude) -> dict:
        new_position = {}
        opposite_direction = self._direction_opposites.get(direction)
        current_opposite_magnitude = self.location[opposite_direction]
        new_opposite_magnitude = current_opposite_magnitude - magnitude
        new_position[opposite_direction] = new_opposite_magnitude

        if new_opposite_magnitude < 0:
            new_direction_magnitude = self.location[direction] + abs(
                new_opposite_magnitude
            )
            new_position[opposite_direction] = 0
            new_position[direction] = new_direction_magnitude

        return new_position

    def _get_direction_facing(self) -> str:
        # Simply the angle to one of 4 mulitiple of 90, like a cartesian plane
        direction_facing = self._direction_facing / 90 % 4
        return self._direction_facing_lookup[direction_facing]

    def move_cardinal_position(self, instruction: Instruction) -> dict:
        return self._move_position(instruction.direction, instruction.magnitude)

    def move_relative_position(self, instruction: Instruction) -> dict:
        direction = self._get_direction_facing()
        return self._move_position(direction, instruction.magnitude)

    def shift_direction_facing(self, instruction: Instruction) -> None:
        # Left adds to the angle, R subtracts from it
        self._direction_facing = (
            self._direction_facing + instruction.magnitude
            if instruction.direction == "L"
            else self._direction_facing - instruction.magnitude
        )

    def follow_instructions(self) -> None:
        for instruction in self.instructions:
            # print(f"{self.location=}")
            # print(f"{instruction=}")
            direction_procedure = self._direction_procedure_lookup[
                instruction.direction
            ]
            # print(f"{direction_procedure.__name__}")
            procedure_result = direction_procedure(instruction)
            # print(f"{procedure_result=}")
            if procedure_result:
                # If we returned a new position, then update the ferry's position
                self.location = {**self.location, **procedure_result}

    def get_manhattan_distance(self) -> int:
        return sum(self.location.values())


ferry = Ferry(instructions)
ferry.follow_instructions()
print(ferry.location)
print(ferry.get_manhattan_distance())
# Part 2: Following the _actual_ instructions, where do we end up?
# (0)
#   -- nothing will happen (will fully rotate around)
# (1)

# (2)
#   -- east coordinate -> west coordinate
#   -- north coordinate -> south coordinate
#   -- west coordinate -> east coordinate
#   -- south coordinate -> north coordinate
# (3)
#   -- east coordinate -> south coordinate
#   -- north coordinate -> east coordinate
#   -- west coordinate -> north coordinate
#   -- south coordinate -> west coordinate


class Waypoint:
    def __init__(self) -> None:
        self._direction_opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        self.rotation_procedure_lookup = {
            0: self._rotate_0,
            1: self._rotate_90,
            2: self._rotate_180,
            3: self._rotate_270,
        }
        self.location = {"N": 1, "S": 0, "E": 10, "W": 0}

    def _move_position(self, direction, magnitude) -> dict:
        new_position = {}
        opposite_direction = self._direction_opposites[direction]
        current_opposite_magnitude = self.location[opposite_direction]
        new_opposite_magnitude = current_opposite_magnitude - magnitude
        new_position[opposite_direction] = new_opposite_magnitude

        if new_opposite_magnitude < 0:
            new_direction_magnitude = self.location[direction] + abs(
                new_opposite_magnitude
            )
            new_position[opposite_direction] = 0
            new_position[direction] = new_direction_magnitude

        return new_position

    def _rotate_0(self) -> dict:
        return self.location

    def _rotate_90(self) -> dict:
        new_location = {}
        # east coordinate becomes north coordinate
        new_location["N"] = self.location["E"]
        # north coordinate becomes west coordinate
        new_location["W"] = self.location["N"]
        # west coordinate becomes south coordinate
        new_location["S"] = self.location["W"]
        # south coordinate becomes east coordinate
        new_location["E"] = self.location["S"]
        return new_location

    def _rotate_180(self) -> dict:
        new_location = {}
        # east coordinate becomes west coordinate
        new_location["W"] = self.location["E"]
        # north coordinate becomes south coordinate
        new_location["S"] = self.location["N"]
        # west coordinate becomes east coordinate
        new_location["E"] = self.location["W"]
        # south coordinate becomes north coordinate
        new_location["N"] = self.location["S"]
        return new_location

    def _rotate_270(self) -> dict:
        new_location = {}
        # east coordinate becomes south coordinate
        new_location["S"] = self.location["E"]
        # north coordinate becomes east coordinate
        new_location["E"] = self.location["N"]
        # west coordinate becomes north coordinate
        new_location["N"] = self.location["W"]
        # south coordinate becomes west coordinate
        new_location["W"] = self.location["S"]
        return new_location

    def rotate(self, instruction: Instruction) -> dict:
        # Simply the angle to one of 4 mulitiple of 90, like a cartesian plane
        sign = 1 if instruction.direction == "L" else -1
        relative_magnitude = instruction.magnitude * sign
        rotate_angle = relative_magnitude / 90 % 4
        rotation_angle_procedure = self.rotation_procedure_lookup[rotate_angle]
        return rotation_angle_procedure()

    def move_cardinal_position(self, instruction: Instruction) -> dict:
        return self._move_position(instruction.direction, instruction.magnitude)

    def move_relative_position(self, instruction: Instruction) -> dict:
        direction = self._get_direction_facing()
        return self._move_position(direction, instruction.magnitude)

    def shift_direction_facing(self, instruction: Instruction) -> None:
        # Left adds to the angle, R subtracts from it
        self._direction_facing = (
            self._direction_facing + instruction.magnitude
            if instruction.direction == "L"
            else self._direction_facing - instruction.magnitude
        )


class Ferry:
    def __init__(self, instructions: list) -> None:
        # Treat direction facing as an angle
        self._waypoint = Waypoint()
        self._direction_procedure_lookup = {
            "N": self._waypoint.move_cardinal_position,
            "S": self._waypoint.move_cardinal_position,
            "E": self._waypoint.move_cardinal_position,
            "W": self._waypoint.move_cardinal_position,
            "R": self._waypoint.rotate,
            "L": self._waypoint.rotate,
            "F": self.move_relative_to_waypoint,
        }
        self.instructions = instructions
        self.location = {"N": 0, "S": 0, "E": 0, "W": 0}

    def _move_position(self, direction, magnitude) -> dict:
        new_position = {}
        opposite_direction = self._waypoint._direction_opposites[direction]
        current_opposite_magnitude = self.location[opposite_direction]
        new_opposite_magnitude = current_opposite_magnitude - magnitude
        new_position[opposite_direction] = new_opposite_magnitude

        if new_opposite_magnitude < 0:
            new_direction_magnitude = self.location[direction] + abs(
                new_opposite_magnitude
            )
            new_position[opposite_direction] = 0
            new_position[direction] = new_direction_magnitude

        return new_position

    def move_relative_to_waypoint(self, instruction: Instruction) -> list:
        toward_waypoint_magnitude = {
            direction: relative_magnitude * instruction.magnitude
            for direction, relative_magnitude in self._waypoint.location.items()
            if relative_magnitude > 0
        }

        return [
            self._move_position(direction, magnitude)
            for direction, magnitude in toward_waypoint_magnitude.items()
        ]

    def follow_instructions(self) -> None:
        for instruction in self.instructions:
            # print(f"{self.location=}")
            # print(f"{instruction=}")
            direction_procedure = self._direction_procedure_lookup[
                instruction.direction
            ]
            # print(f"{direction_procedure.__name__}")
            procedure_result = direction_procedure(instruction)
            # print(f"{procedure_result=}")
            if instruction.direction == "F":
                # Update the ferry's position only on "Forward" commands
                # Need to account for getting multiple commands, like
                # "North 10" _and_ "East 3"
                for result in procedure_result:
                    self.location = {**self.location, **result}
            else:
                # Otherwise, update the waypoint's position
                self._waypoint.location = {
                    **self._waypoint.location,
                    **procedure_result,
                }

    def get_manhattan_distance(self) -> int:
        return sum(self.location.values())


ferry = Ferry(instructions)
ferry.follow_instructions()
print(ferry.location)
print(ferry.get_manhattan_distance())