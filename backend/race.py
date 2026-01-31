from enum import Enum

class BetType(Enum):
    WIN = "win"
    PLACE = "place"
    EACH_WAY = "each_way"

class Race:
    betType = BetType
    players = []

    def setBetType(type):
        betType = type

    def setStake(s):
        stake = s

class Player():
    fishName = str
    stake = float
