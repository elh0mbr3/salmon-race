from race import BetType
from pathlib import Path
import pandas as pd
import numpy as np

def getFishCsv():
    filePath = Path(r"C:\Files\Local Git\hackaway-project-01\fish.csv")
    df = pd.read_csv(filePath)
    return df

def findFishOdds(fishList):
    df = getFishCsv()
    fishOdds = []

    for fish in fishList:
        odds = df.loc[df["Name"] == fish, "Odds"]
        if not odds.empty:
            fishOdds.append(odds.iloc[0])
        else:
            fishOdds.append(0)

    return fishOdds

def payout(fish):
    print("")

def betTypeBias(betType, pot):
    match betType:
        case BetType.PLACE:
            return pot/2
        case BetType.EACH_WAY:
            return pot/3
        case _:
            return pot

def updateOdds(position, participants):
    newOdds = []
    currentOdds = findFishOdds(participants)
    for i in range (len(participants)):
        print(currentOdds[i])
        newOdds.append((-(1/1+np.exp(1.5-position[i]))+(1/2))*currentOdds[i])    
    return newOdds

def main():
    # df = getFishCsv()
    # print(findFishOdds(["Holy Carp"]))
    print(updateOdds([1, 2, 3], ["Holy Carp", "Eel Pie", "Ray Parker Jr."]))

if __name__ == "__main__":
    main()
