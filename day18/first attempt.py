from typing import List, Literal, Tuple


test_input1 = """1 + 2 * 3 + 4 * 5 + 6"""
expected_answer1 = 71
test_equation1 = test_input1.split()

test_input2 = """1 + (2 * 3) + (4 * (5 + 6))"""
expected_answer2 = 51
test_equation2 = [char for char in test_input2 if char != " "]

def solve_equation(equation: List[str], idx: int = 0, anchor: int = 0) -> Tuple[int, int, int]:
    try:
        total = int(equation[idx])
    except ValueError:
        # We hit a paretheses, we have to go deeper
        total, idx = solve_equation(equation, idx=idx + 1)
    print(f"New equation: {idx=}, {anchor=}, {total=}")
    idx +=1
    while idx < len(equation):
        print(f"Current equation: {idx=}, {anchor=}, {total=}")
        char = equation[idx]
        try:
            number = int(char)
        except ValueError:
            if char in ["+", "*"]:
                # Hit an operator, on to the next
                idx += 1
                print("Hit a", char, "incrementing")
                continue
            elif char == "(":
                # Hit a start paretheses, we have to go deeper
                print("Go deeper")
                number, idx, anchor = solve_equation(equation, idx=idx + 1, anchor = idx)
                print(f"Back from the deep. Got: {idx=}, {anchor=}, {number=}")
            elif char == ")":
                # Hit an end parentheses, time to surface
                print(f"Surface. Returning: {idx=}, {anchor=}, {total=}")
                return total, anchor, idx
        operator = equation[idx - 1]
        print(f"{idx=}, {anchor=}, {total=}, {number=}, {operator=}")
        if operator == "+":
            total += number
        elif operator == "*":
            total *= number
        # Got a result, on to the next
        idx = idx + 1

    return total, idx

# assert expected_answer1 == solve_equation(test_equation1)
# assert expected_answer2 == solve_equation(test_equation2)
print(test_equation2)
solve_equation(test_equation2)
