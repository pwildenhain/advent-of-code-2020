# Graciously taken from the comments section of this video: https://www.youtube.com/watch?v=LVCa6MJ1XK8 
import re

lines = open("day18/input.txt").readlines()
# print(lines)
class num(int):
    def __sub__(self, b):
        return num(int(self) * int(b))

    def __add__(self, b):
        return num(int(self) + int(b))

    def __mul__(self, b):
        return num(int(self) + int(b))


def solve(lines, p1):
    res = 0
    for line in lines:
        line = line.strip()
        # print(f"{line=}")
        line = line.replace('*', '-')
        # print(f"line with replacements={line}")
        if not p1:
            line = line.replace('+', '*')
            # print(f"line with additional replacements={line}")
        line = re.sub('(\d+)', r'num(\1)', line)
        # print(f"line with sub={line}")
        x = eval(line)
        # print(x)
        res += x
    return res

# solve(lines[0:1], True)
# solve(lines[0:1], False)
print(solve(lines, True))
print(solve(lines, False))