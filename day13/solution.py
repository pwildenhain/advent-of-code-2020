# courtesy of https://github.com/sotsoguk/adventOfCode2020/blob/860e7da734f8fc1fbf144fb4b76f2a4cd3e2d749/python/day13/day13.py
import os
import time
#import timeit
from collections import Counter
from itertools import groupby
from functools import reduce
from operator import mul
import copy
import sys


def part2_crt(input):
    m = [i[0] for i in input]
    a = [i[0]-i[1] for i in input]
    mm = reduce(mul,m,1)
    z = [mm // mi for mi in m]
    y = [pow(i,-1,j) for i,j in zip(z,m)]
    w = [(i*j)% mm for i,j in zip(y,z)]

    return  sum((a*w) for a,w in zip(a,w)) % mm
    

def main():

    # input
    print(os.getcwd())
    print(sys.version)
    day = "13"
    part1, part2 = 0, 0
    star_line = "*" * 19
    inputFile = f'day13/input.txt'
    start_time = time.time()
    with open(inputFile) as f:
        lines = f.read().splitlines()

    
    target = int(lines[0])
    ids = [int(i) for i in lines[1].split(',') if i != 'x']
    ids2 = [(int(i),j) for j,i in enumerate(lines[1].split(',')) if i != 'x']
    
    # part 1 & 2
    idssorted = sorted(ids,key = lambda x:abs((target %x)-x))
    part1 = abs(target%idssorted[0]-idssorted[0]) * idssorted[0]
    part2 = part2_crt(ids2)
    
    # output
    duration = int((time.time() - start_time) * 1000)

    print(
        f"\n{star_line}\n AoC 2020 - Day {day}\n{star_line}\n\nPart 1:\t\t{part1}\nPart 2:\t\t{part2}\nDuration:\t{duration} ms")


if __name__ == "__main__":
    main()


