"""
UVM SAC
NFL elo model exploration
Author: Henry Kraessig
"""

import pandas as pd

TEAMS = ["Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals",
         "Kansas City Chiefs", "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers",
         "Chicago Bears", "Detroit Lions", "Minnesota Vikings", "Green Bay Packers",
         "Cleveland Browns", "Pittsburgh Steelers", "Baltimore Ravens", "Cincinnati Bengals",
         "Carolina Panthers", "Atlanta Falcons", "New Orleans Saints", "Tampa Bay Buccaneers",
         "Tennessee Titans", "Indianapolis Colts", "Houston Texans", "Jacksonville Jaguars", 
         "Dallas Cowboys", "New York Giants", "Washington Commanders", "Philadelphia Eagles",
         "New England Patriots", "New York Jets", "Buffalo Bills", "Miami Dolphins"]


def expected(home_elo, away_elo):
    # take two teams' elo's
    # calculate expected result of the game (0 to 1)
    # I want a difference in 1000 elo to be about an 87 percent win probability
    # thats where 1200 comes from
    e = 1 / (1 + 10 ** ((away_elo - home_elo) / 1200))
    return e


def game(home_score, home_elo, away_score, away_elo, k):
    # take two teams and the score of their game
    # return a tuple of the elo adjustments for each team
    if home_score > away_score:
        result = 1
    elif home_score < away_score:
        result = 0
    else:
        result = .5

    home_adjustment = k * (result - expected(home_elo, away_elo))
    away_adjustment = k * ((1 - result) - expected(away_elo, home_elo))

    return home_adjustment, away_adjustment


elo = {}

# initialize every team's elo at 1000
for team in TEAMS:
    elo[team] = 1000

week1 = pd.read_csv("data/week1.csv")

for i, e in week1.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

# every team should have had 50/50 odds in week one
# based on k value, that means that winners now have an elo of 1100, losers 900

# same process for next weeks

week2 = pd.read_csv("data/week2.csv")
week3 = pd.read_csv("data/week3.csv")
week4 = pd.read_csv("data/week4.csv")
week5 = pd.read_csv("data/week5.csv")
week6 = pd.read_csv("data/week6.csv")
week7 = pd.read_csv("data/week7.csv")
week8 = pd.read_csv("data/week8.csv")



for i, e in week2.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

for i, e in week3.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

for i, e in week4.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

for i, e in week5.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2
    
for i, e in week6.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

for i, e in week7.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2

for i, e in week8.iterrows():
    # calculate elo adjustments
    a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], 200)
    # apply
    elo[e["home"]] += a1
    elo[e["away"]] += a2



# formatting output in a raking by elo after 4 weeks
elo_list = []
for key, value in elo.items():
    elo_list.append((value, key))

elo_list.sort()

print(f"{'team':<18}\t{'elo':<5}")
for e in elo_list[::-1]:
    print(f"{e[1]:<18}\t{e[0]:<6.2f}")

# which teams are over valued? - Under valued?
# how can we improve on this model?