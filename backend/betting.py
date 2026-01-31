from enum import Enum
from pathlib import Path
import pandas as pd

def getFishCsv():
    filePath = Path("../fish.csv")
    df = pd.read_csv(filePath)
    return df

def findFishOdds(fishList):
    df = getFishCsv()
    fishOdds = []

    for fish in fishList:
        odds = df.loc[df["name"] == fish, "odds"]
        if not odds.empty and odds.count() == 1:
            fishOdds.append(odds.iloc[0, 0])
        else:
            fishOdds.append(0)

    return fishOdds

def payout(fish):
    print("")

def main():
    print("hi")

if __name__ == "__main__":
    main()
