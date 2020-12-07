# puzzle_input = """light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags."""

# puzzle_input = """shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags."""

import re
from typing import Dict, Set

with open("day7/input.txt") as input_file:
    puzzle_input = input_file.read()

# Build rules dict
bag_rules_dict = {}
for rule in puzzle_input.split(".\n"):
    bag, contained_bags = rule.split(" contain ")
    contained_bags_list = contained_bags.split(", ")
    contained_bags_dict = {}
    
    for contained_bag in contained_bags_list:
        try:
            _, num_contained_bag, contained_bag = re.split("(\d+)\s", contained_bag)
            # Get rid of plural + punctuation
            contained_bag = contained_bag.rstrip("s")
            contained_bags_dict[contained_bag] = int(num_contained_bag)
        except ValueError:
            # If we get here it means that the contained_bags_list is 'no other bags'
            # so we'll just pass the empty dictionary through
            pass
    # Get rid of plural for bag
    bag_rules_dict[bag.rstrip("s")] = contained_bags_dict
# Part 1, how many possible bags could we use to contain our shiny gold bag?
def find_outer_bags(bag: str, bag_rules_dict: Dict[str, dict]) -> Set[str]:
    """A recursive function that searches for how many different color bags
    could hold another bag, given the bag holding rules"""
    outer_bags = []
    for outer_bag, inner_bags in bag_rules_dict.items():
        if bag in inner_bags.keys():
            outer_bags += [outer_bag]
            outer_bags += find_outer_bags(outer_bag, bag_rules_dict)
    
    return set(outer_bags)

our_bag = "shiny gold bag"
outer_bags = find_outer_bags(our_bag, bag_rules_dict)
print(len(outer_bags), "bags can hold a", our_bag)
# Part 2, how many bags are contained in our shiny gold bag?
def find_num_inner_bags(bag: str, bag_rules_dict: Dict[str, dict]) -> int:
    """A recursive function that searches for how many total bags are
    contained within another bag, given the bag holding rules"""
    total_inner_bags = 0
    inner_bags = bag_rules_dict[bag]
    total_inner_bags += sum(inner_bags.values())
    
    for inner_bag, num_inner_bag in inner_bags.items():
        total_inner_bags += find_num_inner_bags(inner_bag, bag_rules_dict) * num_inner_bag

    return total_inner_bags

our_bag = "shiny gold bag"
num_inner_bags = find_num_inner_bags(our_bag, bag_rules_dict)
print("A", our_bag, "holds", num_inner_bags, "other bags")