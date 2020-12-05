# puzzle_input = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
# byr:1937 iyr:2017 cid:147 hgt:183cm

# iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
# hcl:#cfa07d byr:1929

# hcl:#ae17e1 iyr:2013
# eyr:2024
# ecl:brn pid:760753108 byr:1931
# hgt:179cm

# hcl:#cfa07d eyr:2025 pid:166559648
# iyr:2011 ecl:brn hgt:59in"""

with open("day4/input.txt") as input_file:
    raw_passports = [credentials.split() for credentials in input_file.read().split("\n\n")]

passports = []
for passport in raw_passports:
    passport_dict = {}
    
    for value_pairs in passport:
        field, value = value_pairs.split(":")
        passport_dict[field] = value
    
    passports += [passport_dict]

# Part 1: check how many passports have valid fields
# all passport fields except country ID (cid)
valid_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
num_passports_with_valid_fields = 0
for passport in passports:
    # all valid fields exist in the passport
    if valid_fields.intersection(passport.keys()) == valid_fields:
        num_passports_with_valid_fields += 1

print("The number of passports with valid fields is:", num_passports_with_valid_fields)

# Part 2, ensure that the values of the fields are valid
import re
# passport field validation functions
def range_is_valid(x: str, min: int, max:int ):
    try:
        x = int(x)
    except ValueError:
        return False

    return min <= x <= max

def byr_is_valid(byr: str):
    return range_is_valid(byr, 1920, 2002)

assert byr_is_valid("2002")
assert not byr_is_valid("2003")

def iyr_is_valid(iyr: str):
    return range_is_valid(iyr, 2010, 2020)

def eyr_is_valid(eyr: str):
    return range_is_valid(eyr, 2020, 2030)

def hgt_is_valid(hgt: str):
    if hgt.endswith("in"):
        return range_is_valid(hgt.rstrip("in"), 59, 76)
    elif hgt.endswith("cm"):
        return range_is_valid(hgt.rstrip("cm"), 150, 193)

    return False

assert hgt_is_valid("60in")
assert hgt_is_valid("190cm")
assert not hgt_is_valid("190in")
assert not hgt_is_valid("190")

def hcl_is_valid(hcl: str):
    if hcl.startswith("#"):
        hcl = hcl.lstrip("#")
        return bool(re.fullmatch("^[a-f0-9]{6}$", hcl))
    
    return False

assert hcl_is_valid("#123abc")
assert not hcl_is_valid("#123abz")
assert not hcl_is_valid("123abc")

def ecl_is_valid(ecl: str):
    return ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

assert ecl_is_valid("brn")
assert not ecl_is_valid("wat")

def pid_is_valid(pid: str):
    return bool(re.fullmatch("^[0-9]{9}$", pid))

assert pid_is_valid("000000001")
assert not pid_is_valid("0123456789")

def cid_is_valid(cid):
    return True

valid_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
validation_dict = {
    "byr": byr_is_valid,
    "iyr": iyr_is_valid,
    "eyr": eyr_is_valid,
    "hgt": hgt_is_valid,
    "hcl": hcl_is_valid,
    "ecl": ecl_is_valid,
    "pid": pid_is_valid,
    "cid": cid_is_valid
}
num_valid_passports = 0
for passport in passports:
    # all valid fields exist in the passport
    if not valid_fields.intersection(passport.keys()) == valid_fields:
        continue
    # all fields contain valid values
    for field, value in passport.items():
        validation_fx = validation_dict[field]
        if not validation_fx(value):
            break
    else:
        num_valid_passports += 1

print("The number of valid passports is:", num_valid_passports)
