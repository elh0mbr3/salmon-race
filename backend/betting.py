from enum import Enum
from pathlib import Path
import pandas as pd
import numpy as np

def getFishCsv():
    base_path = Path(__file__).parent.resolve()
    filePath = base_path / ".." / "fish.csv"
    df = pd.read_csv(filePath)
    return df

def updateOdds(positions: list[int]):
    df = getFishCsv()
  
    # given a sigmoid distribution of fish positions, calculate new odds
    newOdds = []
    for pos in positions:
        newOdds.append((-(1/(1 + np.exp(5 - pos))) + 0.5) / 10)
    
    oldOdds = df["Odds"].tolist()
    df["Odds"] = list(map(lambda old, new: (old + new) / 2, oldOdds, newOdds))
    print(f"[DEBUG] Updated odds:\n{df}\n")
    # df.to_csv(Path("../fish.csv"), index=False) # overwrites the original csv file
    return df

# def calculateNewOdds(positions: list[int]):
    


def main():
    # print(f"Original odds:\n{getFishCsv()}\n")
    # print(f"Updated odds: {updateOdds([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])}\n")
    # print(f"New odds changes: {calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])}\n")
    # newOdds = calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    updateOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

if __name__ == "__main__":
    main()
