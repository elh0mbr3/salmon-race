import time
from player import Player
from fish import Fish
from race import Race, BetType
import pandas as pd
from pathlib import Path
import numpy as np


def getFishCsv():
    filePath = Path("../fish.csv")
    df = pd.read_csv(filePath)
    return df

def selectFish():
    df = getFishCsv()
    selectedFish = df.sample(n=10)

    return selectedFish

def selectFishNames(df: pd.DataFrame):
    selectedFish = df["Name"].tolist()
    return selectedFish

def getFishOdds(df: pd.DataFrame):
    return df.loc[:, "Odds"].to_list()

def updateFishLocations(fishes: list[Fish], odds : float):
    for i, fish in enumerate(fishes):
        random_multiplier = np.random.random()
        fish.setXPosition(fish.getXPosition() + (10 * random_multiplier * odds[i]))

def calculateAllFinished(fishes: list[Fish]):
    num_finished = 0
    for fish in fishes:
        if fish.getXPosition() >= 100:
            num_finished += 1
    if num_finished >= 3:
        return True
    return False

def getTopThree(fishes: list[Fish]):
    sorted_fish = sorted(fishes, key=lambda f: f.getXPosition(), reverse=True)
    return sorted_fish[:3]

def main():
    # Initialize game state
    tick_count = 0
    fishes = selectFish()
    fishNames = selectFishNames(fishes)
    
    # Get fish odds and normalize
    odds = getFishOdds(fishes)
    oddsNp = np.array(odds)
    normOdds = (oddsNp - oddsNp.min()) / (oddsNp.max() - oddsNp.min())
    normOdds += 0.05  # avoid zero odds
    player1 = Player("user1")
    race1 = Race(player1, [], BetType.WIN)

    # Add fishes to the race
    for fish in fishNames:
        tempFish = Fish(fish)
        race1.addFish(tempFish)

    # Let the player place a bet
    print(f"Available:\n {list(map(lambda x: x.getName(), race1.getAllFish()))}")
    fish = input("Select your fish: ")
    amount = input("Enter your stake amount: ")

    # Find the selected fish object
    for f in race1.getAllFish():
        if f.getName() == fish:
            selectedFish = f
            break
        else:
            selectedFish = None

    # Place the bet and add it to the fish
    if selectedFish:
        player1.place_bet(float(amount))
        selectedFish.addBet(player1.getBet())
    else:
        print("Invalid fish selection.")

    print(race1.getFishByName(fish).getBets()[0].getStake())

    # Start the race
    while not calculateAllFinished(race1.getAllFish()):
        updateFishLocations(race1.getAllFish(), normOdds)
        tick_count += 1
        time.sleep(1)
        print(f"Tick {tick_count}:")
        for fish in fishNames:
            print(f"{fish} position: {race1.getFishByName(fish).getXPosition()}")
        print("---------------------------------------")
        
    topThreeFish = getTopThree(race1.getAllFish())
    print(f"winners: {topThreeFish}\n positions: {list(map(lambda x: x.getName(), topThreeFish))}")


if __name__ == "__main__":
    main()