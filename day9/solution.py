# puzzle_input = """35
# 20
# 15
# 25
# 47
# 40
# 62
# 55
# 65
# 95
# 102
# 117
# 150
# 182
# 127
# 219
# 299
# 277
# 309
# 576"""

# numbers_list = [int(num) for num in puzzle_input.splitlines()]
# previous_numbers_lookback = 5
# Part 1: Which of the numbers is not the sum of the previous 25 numbers?

with open("day9/input.txt") as input_file:
    numbers_list = [int(num) for num in input_file.read().splitlines()]
previous_numbers_lookback = 25
invalid_number = None
for idx, current_number in enumerate(numbers_list):
    if idx < previous_numbers_lookback:
        continue
    #print(f"{current_number=}")
    lookback_start, lookback_stop = (idx - previous_numbers_lookback, idx)

    lookback_numbers_list = numbers_list[lookback_start:lookback_stop]
    #print(f"{lookback_numbers_list=}")
    lookback_number_idx = 0
    sum_pair_not_found = True
    while sum_pair_not_found and lookback_number_idx < previous_numbers_lookback:
        #print(f"{lookback_number_idx=}")
        current_lookback_number = lookback_numbers_list[lookback_number_idx]
        difference_number = current_number - current_lookback_number
        try:
            difference_number_idx = lookback_numbers_list.index(difference_number)
            if difference_number_idx != lookback_number_idx:
                sum_pair_not_found = False
                sum_pair = [current_lookback_number, difference_number]
                #print(f"{sum_pair=}")
            else:
                lookback_number_idx += 1
        except ValueError:
            # difference_number wasn't in lookback_numbers_list
            lookback_number_idx += 1
    
    if sum_pair_not_found:
        invalid_number = current_number
        break

print("The invalid number is: ", invalid_number)

# Part 2: Given that invalid number, find a set of contigous numbers that
# add up to that number. What is the sum of the smallest and largest number in that list?

start_idx = 0
contigous_numbers_not_found = True
while contigous_numbers_not_found:
    idx = 0
    contigous_numbers = []
    while sum(contigous_numbers) < invalid_number:
        contigous_numbers += [numbers_list[start_idx + idx]]
        if len(contigous_numbers) == 1:
            idx += 1
            continue
        if sum(contigous_numbers) == invalid_number:
            contigous_numbers_not_found = False
            break
        else:
            idx += 1
    else:
        start_idx += 1

print("The encryption weakness is:", min(contigous_numbers) + max(contigous_numbers))
