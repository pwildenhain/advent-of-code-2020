# puzzle_input = [
#     ["1-3 a", "abcde"],
#     ["1-3 b", "cdefg"],
#     ["2-9 c", "ccccccccc"],
#]
#Part 1, how many passwords are valid
with open("day2/input.txt") as input_file:
    puzzle_input = []
    for line in input_file.readlines():
        rule, password = line.split(":")
        puzzle_input += [[rule, password.rstrip("\n").lstrip(" ")]]

num_old_valid_passwords = 0

for rule, password in puzzle_input:
    letter_range, letter = rule.split()
    min_times, max_times = letter_range.split("-")
    if int(min_times) <= password.count(letter) <= int(max_times):
        num_old_valid_passwords += 1

print("The number of old valid passwords is:", num_old_valid_passwords)

# Part 2, different password policy
num_current_valid_passwords = 0

for rule, password in puzzle_input:
    letter_position, letter = rule.split()
    index_1, index_2 = letter_position.split("-")
    # Subtract 1 for zero indexing
    index_1 = int(index_1) - 1
    index_2 = int(index_2) - 1
    letter_appears_exactly_once = (password[index_1] + password[index_2]).count(letter) == 1
    if letter_appears_exactly_once:
        num_current_valid_passwords += 1

print("The number of current valid passwords is:", num_current_valid_passwords)
