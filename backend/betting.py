from enum import Enum
from pathlib import Path
import pandas as pd
import numpy as np

def getFishCsv():
    filePath = Path("../fish.csv")
    df = pd.read_csv(filePath)
    return df

def updateOdds(newOdds: list[float]):
    df = getFishCsv()
    oldOdds = df["Odds"].tolist()
    df["Odds"] = list(map(lambda old, new: (old + new) / 2, oldOdds, newOdds))
    # df.to_csv(Path("../fish.csv"), index=False) # overwrites the original csv file
    return df

def calculateNewOdds(positions: list[int]):
    # given a sigmoid distribution of fish positions, calculate new odds
    oddChanges = []
    for pos in positions:
        oddChanges.append((-(1/(1 + np.exp(5 - pos))) + 0.5) / 10)
    return oddChanges

def main():
    # print(f"Original odds:\n{getFishCsv()}\n")
    # print(f"Updated odds: {updateOdds([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])}\n")
    # print(f"New odds changes: {calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])}\n")
    newOdds = calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    updateOdds(newOdds)

if __name__ == "__main__":
    main()
