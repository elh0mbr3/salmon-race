# from player import Player
# from fish import Fish
import itertools

class Bet:
    iter_id = itertools.count()

    id: str
    # player: Player
    stake: float
    # bet_on: Fish

    def __init__(self, stake: float):
        self.id = self.iter_id # for testing purposes
        # self.player = player
        # self.bet_on = bet_on
        self.stake = stake

    def getStake(self):
        return self.stake
    
