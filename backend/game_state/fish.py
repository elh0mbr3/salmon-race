from bet import Bet

class Fish:
    fish_name: str
    players_bets: Bet = []
    total_of_stake: float
    has_won: bool

    def render_bets(self, bet: Bet):
        if bet.bet_on == self:
            self.players_bets.append(bet)

    def __init__(self, fish_name: str, player_bets: Bet):
        self.fish_name = fish_name
        self.player_bets = player_bets

    def generateOdds():
        