# Voting Machine Fraud in the State of Pennsylvania

This exposes the pattern between voter turnout and age that proves voting machine fraud in Pennsylvania was used in the 2020 General Presidential Election.

## Setup

Requires python3. Before running, be sure you have enough free space for the downloaded CSV files and converted JSON files, on the order of several GB.

## Running

1. Download voter registration database (see 'Data Source' section).
2. (TODO) Convert raw csv data to json (may take a while): `./jsonify.py`
3. (TODO) Finally, plot voter turnout lines vs. age for all counties on the same plot: `./plot_turnout_by_age.py`

## Data Source

Pennsylvania requires a $20.00 fee to download the voter registration database, and prohibits some forms of distribution.

Pennsylvania Full Voter Export (voter registration database): https://www.pavoterservices.pa.gov/Pages/PurchasePAFULLVoterExport.aspx

