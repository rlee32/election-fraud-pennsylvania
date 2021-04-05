# Voting Machine Fraud in the State of Pennsylvania

This exposes the pattern between voter turnout and age caused by voting machine fraud in Pennsylvania in the 2020 General Presidential Election.

## Setup

Requires python3. Before running, be sure you have enough free space for the downloaded and decompressed CSV files, about 6.6 GB.

## Running

1. Download voter registration database (see 'Data Source' section).
2. Move and rename decompressed folder to `./data/Statewide`.
3. To plot voter turnout lines vs. age for all counties on the same plot: `./plot_turnout_by_age.py`.

## Data Source

Pennsylvania requires a $20.00 fee to download the voter registration database, and prohibits some forms of distribution.

Pennsylvania Full Voter Export (voter registration database): https://www.pavoterservices.pa.gov/Pages/PurchasePAFULLVoterExport.aspx

