import time
from player import Player
from fish import Fish
from race import Race, BetType
import pandas as pd
from pathlib import Path

start_time = time.time()
tick = 1.0

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
    selectedFish = df.sample(n=9)["name"].tolist()

    return selectedFish

def main():

    # fishes = selectFish()

    # for fish in fishes:
    #     Fish(fish, 0)


    player1 = Player("test1")
    player1.place_bet(100)
    fish1 = Fish("testFish", player1.getBet())
    race1 = Race(player1, [fish1], BetType.WIN)
    print(race1.getFish()[0].getName())

if __name__ == "__main__":
    main()