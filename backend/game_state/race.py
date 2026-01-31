from enum import Enum
from player import Player
from fish import Fish

class BetType(Enum):
    WIN = "win"
    PLACE = "place"
    EACH_WAY = "each_way"

class Race:
    player: Player
    fish: list[Fish]
    bet_type: BetType

    def __init__(self, player: Player, fish : list[Fish], betType : BetType):
        self.player = player
        self.fish = fish
        self.bet_type = betType

    def getPlayer(self):
        return self.player
    
    def getFish(self):
        return self.fish
    
    def getBetType(self):
        return self.bet_type