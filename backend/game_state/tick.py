import time
from player import Player
from fish import Fish
from race import Race, BetType
import pandas as pd
from pathlib import Path
import numpy as np

# start_time = time.time()
# tick = 1.0

tick_count = 0

# while True:
#     new_time = time.time()
#     tick_count += 1

def getFishCsv():
    filePath = Path("../fish.csv")
    df = pd.read_csv(filePath)
    return df

def selectFish():
    df = getFishCsv()
    selectedFish = df.sample(n=10)["Name"].tolist()
    return selectedFish

def updateFishLocations(fishes: list[Fish], tick_count: int):
    for fish in fishes:
        random_multiplier = np.random.random()
        fish.setXPosition(fish.getXPosition() + (1 * random_multiplier * tick_count))

def calculateAllFinished(fishes: list[Fish]):
    for fish in fishes:
        if fish.getXPosition() < 100:
            return False
    return True

def main():

    # Initialize game state
    tick_count = 0
    fishes = selectFish()
    player1 = Player("user1")
    race1 = Race(player1, [], BetType.WIN)

    # Add fishes to the race
    for fish in fishes:
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
        updateFishLocations(race1.getAllFish(), tick_count)
        tick_count += 1
        time.sleep(1)
        print(f"Tick {tick_count}:")
        for fish in fishes:
            print(f"{fish} position: {race1.getFishByName(fish).getXPosition()}")
        print("---------------------------------------")
        # print(f"{fish} position: {race1.getFishByName(fish).getXPosition()}")

if __name__ == "__main__":
    main()