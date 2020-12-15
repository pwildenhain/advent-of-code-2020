# puzzle_input = """0,3,6"""
puzzle_input = """11,18,0,20,1,7,16"""
spoken_numbers = puzzle_input.split(",")
spoken_numbers_last_turn = {num: idx + 1 for idx, num in enumerate(spoken_numbers)}

# Part 1: What is the 2020th number spoken?
# Part 2: What is the 30000000th number spoken?

spoken_number_idx = len(spoken_numbers) - 1
turn = spoken_number_idx + 2
# total_turns = 2020
total_turns = 30000000
while turn <= total_turns:
    last_spoken_number = spoken_numbers[-1]
    try:
        # we have said the last number before, how long has it been since we said it
        last_spoken_number_turn = spoken_numbers_last_turn[last_spoken_number]
        last_turn = turn - 1
        turns_since_last_spoken_number = str(last_turn - last_spoken_number_turn)
        # now remember that we said it last turn
        spoken_numbers_last_turn[last_spoken_number] = last_turn
        # then say the number for this turn
        spoken_numbers.append(turns_since_last_spoken_number)
    except KeyError:
        # this is the first time we've seen this number
        # so we say 0 next
        spoken_numbers.append("0")
        spoken_numbers_last_turn[last_spoken_number] = turn - 1
    except KeyboardInterrupt:
        print(turn)

    spoken_number_idx += 1
    turn += 1

print(spoken_numbers[-1])
