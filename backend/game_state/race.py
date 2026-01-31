from enum import Enum
from player import Player
from bet import Bet

class BetType(Enum):
    WIN = "win"
    PLACE = "place"
    EACH_WAY = "each_way"

class Race:
    betType = BetType
    bets: Bet = []

    def setBetType(type):
        betType = type

    def setStake(s):
        stake = s




    
