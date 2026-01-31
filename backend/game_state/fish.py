from bet import Bet

class Fish():
    fish_name : str
    player_bets : list[Bet]

    def __init__(self, fish_name: str, player_bets: Bet):
        self.fish_name = fish_name
        self.player_bets = [player_bets]

    def getName(self):
        return self.fish_name