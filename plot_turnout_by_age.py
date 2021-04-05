#!/usr/bin/env python3

DATA_FOLDER = './data/Statewide/'

import os
from typing import Dict

# Data files (tab-separated) do not contain header files, so you need to consult the included 'Voter Export' doc,
# and hard-code the indices here.

ELECTION_YEAR = 2020 # choose presidential election years from 2000 - 2020
ELECTION_DAY = {
    2020: '03',
    2016: '08',
    2012: '06',
    2008: '04',
    2004: '02',
    2000: '07'
}
ELECTION_DATE = f'11/{ELECTION_DAY[ELECTION_YEAR]}/{ELECTION_YEAR}'

VOTER_ID_INDEX = 0
DOB_INDEX = 7
REGISTRATION_DATE_INDEX = 8
BASE_ELECTION_VOTE_INDEX = 70

MINIMUM_REGISTERED_VOTERS = 50
TOTAL_COUNTIES = 67

KEY_FILE = './key.json' # file that contains the 'conversion key' that will allow you to predict votes cast in each county.

def str_to_int(date):
    """Converts date in form MM/DD/YYYY to and integer of form YYYYMMDD. """
    tokens = date.strip().split('/')
    return int(f'{tokens[2]}{tokens[0]}{tokens[1]}')

def get_age(start_date, end_date):
    """Returns integer age given dates in form MM/DD/YYYY. """
    start = str_to_int(start_date)
    end = str_to_int(end_date)
    diff = end - start
    if diff < 0:
        return diff / 10000.0
    else:
        return int(diff / 10000)

def get_county_files(county: str):
    return [f'{DATA_FOLDER}/{x}' for x in os.listdir(DATA_FOLDER) if x[0] != '.' and f'{county} ' in x] # ignore hidden files.

def get_all_counties():
    counties = set()
    for f in os.listdir(DATA_FOLDER):
        if f[0] == '.':
            continue
        counties.add(f.strip().split()[0])
    return counties

def get_election_id(county: str):
    files = get_county_files(county)
    election_map_file = [x for x in files if ' Election Map ' in x]
    assert(len(election_map_file) == 1)
    with open(election_map_file[0], 'r') as f:
        for line in f:
            if ELECTION_DATE in line:
                return int(line.strip().split()[1])

def get_voters(county: str):
    """Returns registered list of voters, each described as:
    {
        'age': int, # age at specified election date
        'voted': str # acronym of vote method if voted in specified election, blank if no vote.
    }
    """
    election_id = get_election_id(county)
    vote_method_index = BASE_ELECTION_VOTE_INDEX + (election_id - 1) * 2
    files = get_county_files(county)
    vote_file = [x for x in files if ' FVE ' in x]
    assert(len(vote_file) == 1)
    voters = []
    with open(vote_file[0], 'r') as f:
        for line in f:
            fields = line.strip().split('\t')
            dob = fields[DOB_INDEX]
            if not dob:
                print(f'voter with no dob, voter ID: {fields[VOTER_ID_INDEX]}')
                continue
            reg = fields[REGISTRATION_DATE_INDEX]
            vote = fields[vote_method_index].replace('"', '')
            if reg:
                if str_to_int(reg) > str_to_int(ELECTION_DATE):
                    continue
            else:
                print(f'voter with no registration date, voter ID: {fields[VOTER_ID_INDEX]}')
                if not vote:
                    continue
            age = get_age(dob, ELECTION_DATE)
            if age < 18:
                continue
            if age > 119:
                print(f'skipping unreasonable age: {age}')
                continue
            voters.append({'age': age, 'vote': vote})
    return voters

def normalized_turnout_by_age(voters):
    voters_by_age = {}
    votes_by_age = {}
    for v in voters:
        a = v['age']
        if a not in voters_by_age:
            voters_by_age[a] = 0
        voters_by_age[a] += 1
        if v['vote']:
            if a not in votes_by_age:
                votes_by_age[a] = 0
            votes_by_age[a] += 1
    turnout = {}
    total_votes = sum([votes_by_age[a] for a in votes_by_age])
    total_voters = sum([voters_by_age[a] for a in voters_by_age])
    overall_turnout = total_votes / total_voters
    for a in voters_by_age:
        if voters_by_age[a] < MINIMUM_REGISTERED_VOTERS:
            continue
        turnout[a] = votes_by_age[a] / voters_by_age[a] / overall_turnout
    return turnout

from matplotlib import pyplot as plt

def plot_turnout(turnout: Dict[int, int]):
    tt = list(turnout.items())
    tt.sort()
    plt.plot([x[0] for x in tt], [x[1] for x in tt])

import json

if __name__ == '__main__':
    plotted = 0
    key = {}
    for county in get_all_counties():
        print(f'reading county {county}')
        voters = get_voters(county)
        turnout = normalized_turnout_by_age(voters)
        if not turnout:
            continue
        plotted += 1
        for a in turnout:
            if a not in key:
                key[a] = []
            key[a].append(turnout[a])
        plot_turnout(turnout)

    for a in key:
        avg = sum(key[a]) / len(key[a])
        key[a] = avg
    json.dump(key, open(KEY_FILE, 'w'))
    print(f'wrote key to {KEY_FILE}')

    print(f'plotted {plotted} counties.')
    plt.xlabel(f'Age (ages with less than {MINIMUM_REGISTERED_VOTERS} registered voters are hidden)')
    plt.ylabel('Normalized voter turnout (votes / registered voters / overall turnout fraction)')
    plt.title(f'{ELECTION_YEAR} Pennsylvania Voter Turnout vs. Age ({plotted} of {TOTAL_COUNTIES} counties; each line = 1 county)')
    plt.show()

