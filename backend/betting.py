from enum import Enum
from pathlib import Path
import pandas as pd
import numpy as np
# from backend.game_state.fish import Fish

def getFishCsv():
    base_path = Path(__file__).parent.resolve()
    filePath = base_path / ".." / "fish.csv"
    df = pd.read_csv(filePath)
    return df

# def updateCsvOdds(fish_names: list[Fish]):
#     df = getFishCsv()
  
#     # given a sigmoid distribution of fish positions, calculate new odds
#     newOdds = []
#     for pos in range(len(fish_names)):
#         newOdds.append((-(1/(1 + np.exp(5 - pos))+ 0.5)) / 10)
    
#     #find odds missing in program and copy across csv odds
#     for i, fish_name in enumerate(fish_names):
#         for index, row in df.iterrows():
#             if row["Name"] == fish_name:
#                 df.at[index, "Odds"] = fish_name.getOdds() + newOdds[i]

    # oldOdds = df["Odds"].tolist()
    # df["Odds"] = list(map(lambda old, new: (old + new) / 2, oldOdds, newOdds))
    print(f"[DEBUG] Updated odds:\n{df}\n")
    # df.to_csv(Path("../fish.csv"), index=False) # overwrites the original csv file
    return df
    


def main():
    # print(f"Original odds:\n{getFishCsv()}\n")
    # print(f"Updated odds: {updateOdds([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10])}\n")
    # print(f"New odds changes: {calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])}\n")
    # newOdds = calculateNewOdds([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # updateCsvOdds(Fish())
    print((np.sigmoid(1)+0.5)/10)

if __name__ == "__main__":
    main()
