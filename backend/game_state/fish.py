# from bet import Bet

class Fish():
    fish_name : str
    player_bets : list[str] #Bet]
    x_position : float

    def __init__(self, fish_name: str):
        self.fish_name = fish_name
        self.player_bets = []
        self.x_position = 0

    def getName(self):
        return self.fish_name
    
    def getBets(self):
        return self.player_bets
    
    def getXPosition(self):
        return self.x_position
    
    def setXPosition(self, new_x_position: int):
        self.x_position = new_x_position

    def addBet(self, new_bet: str): #Bet):
        self.player_bets.append(new_bet)