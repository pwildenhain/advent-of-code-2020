# puzzle_input = """939
# 7,13,x,x,59,x,31,19"""

# airport_arrival_time, bus_schedules = puzzle_input.splitlines()
# Part 1 find the earliest departing bus
with open("day13/input.txt") as puzzle_input:
    airport_arrival_time, bus_schedules = puzzle_input.read().splitlines()

airport_arrival_time = int(airport_arrival_time)
bus_schedules = [int(schedule) for schedule in bus_schedules.split(",") if schedule != 'x']

closest_departure_bus = [0, 1000000000]
for schedule in bus_schedules:
    departure_time = schedule

    while departure_time < airport_arrival_time:
        departure_time += schedule

    depature_diff = departure_time - airport_arrival_time
    if depature_diff < closest_departure_bus[1]:
        closest_departure_bus[0] = schedule
        closest_departure_bus[1] = depature_diff

print(closest_departure_bus)
print(closest_departure_bus[0] * closest_departure_bus[1])
# Part 2 find the earliest time stamp where all the buses leave one minute
# after each other
with open("day13/input.txt") as puzzle_input:
    _, bus_schedules = puzzle_input.read().splitlines()
# puzzle_input = """939
# 1789,37,47,1889"""
# _, bus_schedules = puzzle_input.splitlines()

bus_schedules = [schedule for schedule in bus_schedules.split(",")]
fixed_bus_schedules = [schedule for schedule in bus_schedules if schedule != 'x']

schedule_remainders = {}
schedule_diff = 0
for idx, schedule in enumerate(fixed_bus_schedules):
    schedule = int(schedule)
    if idx == 0:
        # beginning of list, always will be a remainder of 0
        schedule_remainders[schedule] = schedule_diff
        continue

    previous_schedule = fixed_bus_schedules[idx - 1]
    schedule_diff = schedule_diff + (bus_schedules.index(str(schedule)) - bus_schedules.index(previous_schedule))

    schedule_remainder = schedule - schedule_diff
    if schedule_remainder < 0:
        # can't have a negative remainder, get the true remainder
        schedule_remainder = abs(schedule_remainder) % schedule
    
    schedule_remainders[schedule] = schedule_remainder
# Use these position diffs to try and figure out when everything will line up perfectly
print(schedule_remainders)
# t0 = 1068781
# for schedule, schedule_remainder in schedule_remainders.items():
#     print(f"{t0 % schedule == schedule_remainder}")
# so if we dont get a match, then we have to increment up by the highest number in the schedule list?
# max_schedule_possible_departure_times = [x for x in range(max_schedule_remainder, 1000, max_schedule) if (x - max_schedule_remainder) % max_schedule == 0]
# max_schedule_possible_departure_times = [x for x in range(max_schedule_remainder, 1000, max_schedule)]
# just add the max_schedule to the max_schedule remainder on each loop increment
# to get the earliest_departure_time
# if the earliest_depature_time % schedule != schedule_reminder
# then break and move on
# this may not work if the remainders are < 0, need to figure that part out
# print(max_schedule_possible_departure_times)

# for departure_time in range(min_departure_time, max_departure_time):
#     for schedule, schedule_reminder in schedule_remainders.items():

# while number not found, do for loop over all numbers, expect the remainders

earliest_time_found = False
schedule_step_size = max(schedule_remainders.keys())
#departure_time = schedule_remainders[schedule_step_size]
# Hopefully it's at least this (from a previous run)
departure_time = 25963905501572
checkpoint = 26000000000000
try:
    while not earliest_time_found:
        for schedule, schedule_remainder in schedule_remainders.items():
            if departure_time > checkpoint:
                checkpoint += 1000000000000
                print(departure_time)
            if departure_time % schedule != schedule_remainder:
                departure_time += schedule_step_size
                break
        else:
            earliest_time_found = True
except KeyboardInterrupt:
    print(departure_time)

print(departure_time)
    