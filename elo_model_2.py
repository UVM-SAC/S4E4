"""
UVM SAC
Improving our NFL elo model
Author: Henry Kraessig
"""

# goals for the new model:
    # account for margin of victory
    # account for home field advantage
    # account for injuries

import pandas as pd
from colorama import Fore, Style

TEAMS = ["Los Angeles Rams", "San Francisco 49ers", "Seattle Seahawks", "Arizona Cardinals",
         "Kansas City Chiefs", "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers",
         "Chicago Bears", "Detroit Lions", "Minnesota Vikings", "Green Bay Packers",
         "Cleveland Browns", "Pittsburgh Steelers", "Baltimore Ravens", "Cincinnati Bengals",
         "Carolina Panthers", "Atlanta Falcons", "New Orleans Saints", "Tampa Bay Buccaneers",
         "Tennessee Titans", "Indianapolis Colts", "Houston Texans", "Jacksonville Jaguars", 
         "Dallas Cowboys", "New York Giants", "Washington Commanders", "Philadelphia Eagles",
         "New England Patriots", "New York Jets", "Buffalo Bills", "Miami Dolphins"]

elo = {}
for team in TEAMS:
    elo[team] = 1000
records = {}
for team in TEAMS:
    records[team] = [0, 0, 0]


# homefield - constant to determine how valuable homefield advantage is
HOMEFIELD = 0.018
# home teams win 51.8 percent of the time


def expected_margin(team1, team2):
    e = (14/800) * (team1 - team2) # 800 point difference means 14 point spread
    return e # positive if home expected to win, negative if away is expected to win

# for team1
def expected_result(team1, team2):
    e = 1 / (1 + 10 ** ((team2 - team1) / 800)) # 800 means 1000 elo dif -> ~95% chance of winning
    return e


def k_scale(margin, expected_margin):
    # potentially add injury exception here
    margin_dif = margin - expected_margin
    # lets teams that over perform expectation gain more points, and teams that underperform lose points
    if margin > 0:
        return (.06 / 2) * margin_dif + .42 #if you win, the win matters more by how many scores you overperformed by
    elif margin < 0:
        return (-.06 / 2) * margin_dif + .42 
    else: 
        return 1


def game(home_score, home_elo, away_score, away_elo, k):
    if home_score > away_score:
        result = 1
    elif home_score < away_score:
        result = 0
    else:
        result = .5

    margin = home_score - away_score
    # if expected is very large and actual is not, elos should get closer
    a1 = k * (k_scale(margin, expected_margin(home_elo, away_elo))) * (result - expected_result(home_elo, away_elo))
    a2 = k * (k_scale(-margin, expected_margin(away_elo, home_elo))) * (1 - result - expected_result(away_elo, home_elo))
    # change so that when expected margin is very large and margin is very small, have negative adjustment for a winner
    return a1, a2


def update_elo(lst, k = "descending", show=False):
    if k == "descending":
        k = 200
    for week, df in enumerate(lst):
        if show:
            print(f"Week {week + 1} results:\n")
            #home away
        for i, e in df.iterrows():
            # calculate elo adjustments
            if k == "descending":
                if k > 50:
                    k -= (50 / i)
                a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], k)
            else:
                a1, a2 = game(e["home_score"], elo[e["home"]], e["away_score"], elo[e["away"]], k)

            #shows individual elo adjustments after each game
            if show:
                if expected_margin(elo[e["home"]], elo[e["away"]]) >= 0:
                    favorite = 'home'
                else:
                    favorite = 'away'

                if e['home_score'] >= e['away_score']:
                    winner = 'home'
                    score_dif = e['home_score'] - e['away_score']
                else:
                    winner = 'away'
                    score_dif = e['away_score'] - e['home_score']

                if a1 > 0:
                    color1 = Fore.GREEN
                    sign1 = '+'
                    color2 = Fore.RED
                    sign2 = ''
                else: 
                    color1 = Fore.RED   
                    sign1 = ''
                    color2 = Fore.GREEN    
                    sign2 = '+'         

                em = abs(expected_margin(elo[e['home']], elo[e['away']]))

                if winner == favorite:
                    moe = score_dif - em
                else:
                    moe = score_dif + em

                print(f"{e['home']:<25}: {e['home_score']:<4}{e['away']:>28}: {e['away_score']:<3}\t\t Expected: {e[favorite]} by {em:.0f}")

                print(f"{e['home']:<25}: " + color1 + f"{sign1}{a1:<4.0f}" + Style.RESET_ALL + f"{e['away']:>27}: " + color2 + f"{sign2}{a2:<4.0f}" + Style.RESET_ALL + f"\t\t MOE: {moe:<3.0f}\n")
            
            # apply
            elo[e["home"]] += a1
            elo[e["away"]] += a2
            # apply records
            if e['home_score'] > e['away_score']:
                records[e['home']][0] += 1
                records[e['away']][1] += 1
            elif e['home_score'] < e['away_score']:
                records[e['home']][1] += 1
                records[e['away']][0] += 1
            else:
                records[e['home']][2] += 1
                records[e['away']][2] += 1



# show current rankings by elo
def show_rankings(elo_d, records_d):
    elo_list = []
    for key, value in elo_d.items():
        elo_list.append((value, key, records_d[key]))


    elo_list.sort()

    print(f"{'team':<18}\t\t{'elo':<5}")
    for e in elo_list[::-1]:
        print(f"{e[1]:<21} ({e[2][0]}-{e[2][1]})\t{e[0]:<6.2f}")


week1 = pd.read_csv("data/week1.csv")
week2 = pd.read_csv("data/week2.csv")
week3 = pd.read_csv("data/week3.csv")
week4 = pd.read_csv("data/week4.csv")
week5 = pd.read_csv("data/week5.csv")
week6 = pd.read_csv("data/week6.csv")
week7 = pd.read_csv("data/week7.csv")
week8 = pd.read_csv("data/week8.csv")

datalist = [week1, week2, week3, week4, week5, week6, week7, week8]


update_elo(datalist, 200, show=True)
show_rankings(elo, records)
