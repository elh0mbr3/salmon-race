from player import Player
from fish import Fish
import random

class Bet:
    id: str
    player: Player
    stake: float
    bet_on: Fish

    def __init__(self, player: Player, bet_on: Fish, stake: float):
        self.id = random(0, 1000) # for testing purposes
        self.player = player
        self.bet_on = bet_on
        self.stake = stake
    
