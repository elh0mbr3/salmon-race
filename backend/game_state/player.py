# from bet import Bet
import itertools
# from fish import Fish
from enum import Enum

#added
class BetType(Enum):
    WIN = "win"
    PLACE = "place"
    EACH_WAY = "each_way"

class Player:
    # iterable player id
    iter_id = itertools.count()

    # id: str
    username: str
    balance: float
    is_locked: bool
    player_bet: float #Bet
    on_fish: str

    def __init__(self, username: str):
        self.id = next(Player.iter_id)
        self.username = username
        self.balance = 10000
        self.is_locked = False
        self.on_fish = None

    def place_bet(self, stake: float, on_fish: str, typeBet: BetType): # added to
        if self.is_locked:
            print("[ERROR] You cannot place a bet while the race is active.")
        elif self.balance-stake > 0:
            self.balance = self.balance - stake
            self.player_bet = stake #Bet(stake)
            self.bet_type = typeBet
            self.on_fish = on_fish
            # self.is_locked = True ???
            print("[SYSTEM] Success. Your bet is locked. Please notice that you cannot withdraw or deposit your balance while the race is active.")
        else:
            print("[ERROR] Insufficient funds. Please deposit money to your balance to proceed.")

    def get_payout(self, amount):
        self.balance = self.balance + amount

    def deposit_funds(self, deposit_amount):
        self.balance = self.balance + deposit_amount

    def getBet(self):
        return self.player_bet
    
    def getUsername(self):
        return self.username
    
    def getBalance(self):
        return self.balance
    
    def getIsLocked(self):
        return self.is_locked
    
    # def setBetType(self, bet_type: BetType):
    #     self.bet_type = bet_type

    def getBetType(self):
        return self.bet_type