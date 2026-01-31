from enum import Enum
from pathlib import Path
import pandas as pd

class BetType(Enum):
    WIN = "win"
    PLACE = "place"
    EACH_WAY = "each_way"

class Round:
    betType = BetType
    stake = int
    betFish = str


def getFishCsv():
    filePath = Path("../fish.csv")
    df = pd.read_csv(filePath)
    return df

def findFishOdds(fish):
    df = getFishCsv()
    odds = df.loc[df["name"] == fish, "odds"]
    if not odds.empty:
        print("")


