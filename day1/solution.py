# Part 1 Find two numbers that sum up to one number
#puzzle_input = {1721: "", 979: "", 366: "", 299: "", 675: "", 1456: ""}
sum_number = 2020
with open("day1/input.txt") as input_file:
    puzzle_input = {int(line.rstrip("\n")): "" for line in input_file.readlines()}

for first_num in puzzle_input:
    second_num = sum_number - first_num
    try:
        puzzle_input[second_num]
        print(first_num, "and", second_num, "add up to", sum_number)
        print("Their product is", first_num * second_num)
        break
    except KeyError:
        continue
# Part 2 Find three numbers that sum up to one number
answer = 0
for first_num in puzzle_input:
    if answer:
        break
    remaining_sum = sum_number - first_num
    for second_num in puzzle_input:
        if second_num == first_num:
            continue
        else:
            third_num = remaining_sum - second_num
            try:
                puzzle_input[third_num]
                print(first_num, ", ", second_num, " and ", third_num, " add up to ", sum_number, sep="")
                answer = first_num * second_num * third_num
                print("Their product is", answer)
                break
            except KeyError:
                continue
