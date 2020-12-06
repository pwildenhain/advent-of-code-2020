# puzzle_input = """abc

# a
# b
# c

# ab
# ac

# a
# a
# a
# a

# b"""

import string

# group_answers = [group.split("\n") for group in puzzle_input.split("\n\n")]

with open("day6/input.txt") as input_file:
    group_answers = [group.split("\n") for group in input_file.read().split("\n\n")]


# Part 1: For each group, how many people answered "yes" to a customs form question?

group_yes_answers = [
    {letter: 0 for letter in string.ascii_lowercase} for _ in group_answers
]

for group_num, group in enumerate(group_answers):
    for person_answer in group:
        for yes_letter in person_answer:
            yes_letter_count = group_yes_answers[group_num][yes_letter]
            if yes_letter_count > 0:
                # Already recorded this "yes_letter" for this group
                continue
            group_yes_answers[group_num][yes_letter] += 1

total_any_yes_answers_from_all_groups = sum(
    [
        num_yes_answers
        for group_answer_dict in group_yes_answers
        for num_yes_answers in group_answer_dict.values()
    ]
)

print(
    "The total amount of any yes answers from all groups is:",
    total_any_yes_answers_from_all_groups,
)

# Part 2: For each group, how many people in a group *all* answered yes to a customs form question?
 
group_yes_answers = [
    {letter: 0 for letter in string.ascii_lowercase} for _ in group_answers
]

for group_num, group in enumerate(group_answers):
    num_people_in_group = len(group)

    for person_answer in group:
        for yes_letter in person_answer:
            # Just record _all_ yes letters here, we'll fix it later
            group_yes_answers[group_num][yes_letter] += 1
    
    # Check the yes answers for that group, against the group size
    for yes_letter, yes_answer_count in group_yes_answers[group_num].items():
        # Everyone answered this question "yes"
        if yes_answer_count == num_people_in_group:
            group_yes_answers[group_num][yes_letter] = 1
        # At least one person didn't answer "yes"
        else:
            group_yes_answers[group_num][yes_letter] = 0

total_all_yes_answers_from_all_groups = sum(
    [
        num_yes_answers
        for group_answer_dict in group_yes_answers
        for num_yes_answers in group_answer_dict.values()
    ]
)

print(
    "The total amount of all yes answers from all groups is:",
    total_all_yes_answers_from_all_groups,
)