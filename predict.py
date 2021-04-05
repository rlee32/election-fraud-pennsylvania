#!/usr/bin/env python3

import json
from plot_turnout_by_age import ELECTION_YEAR, KEY_FILE, get_voters
from matplotlib import pyplot as plt
from typing import Dict, Set

import sys

MINIMUM_REGISTERED_VOTERS = 50

def plot_votes(votes: Dict[int, int], exclude: Set[int], style: str):
    vv = list(votes.items())
    vv.sort()
    plt.plot([x[0] for x in vv if x[0] not in exclude], [x[1] for x in vv if x[0] not in exclude], style)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('arguments: county_name')
        sys.exit()

    county = sys.argv[1]

    key = json.load(open(KEY_FILE, 'r'))

    voters = get_voters(county)

    vote_count = {}
    voter_count = {}
    for v in voters:
        a = v['age']
        if a not in voter_count:
            voter_count[a] = 0
        voter_count[a] += 1
        if v['vote']:
            if a not in vote_count:
                vote_count[a] = 0
            vote_count[a] += 1

    exclude = set()
    for a in voter_count:
        if voter_count[a] < MINIMUM_REGISTERED_VOTERS:
            exclude.add(a)

    plot_votes(vote_count, exclude, 'r-')

    overall_turnout = sum([vote_count[x] for x in vote_count]) / sum([voter_count[x] for x in voter_count])
    prediction = {}
    for a in voter_count:
        k = key.get(str(a))
        if k is None:
            prediction[a] = 0
        else:
            prediction[a] = voter_count[a] * overall_turnout * key[str(a)]

    plot_votes(prediction, exclude, 'b:')

    plt.xlabel(f'Age (ages with less than {MINIMUM_REGISTERED_VOTERS} registered voters are hidden)')
    plt.ylabel('Votes (blue is prediction, red is actual)')
    plt.title(f'{ELECTION_YEAR} Pennsylvania County {county}: Prediction of Votes Cast vs. Age')
    plt.show()





