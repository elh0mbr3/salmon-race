from bet import Bet
import itertools

class Player:
    # iterable player id
    iter_id = itertools.count()

    id: str
    username: str
    balance: float
    is_locked: bool
    player_bet: Bet

    def __init__(self, username: str):
        self.id = next(Player.iter_id)
        self.username = username
        self.balance = 10000
        self.is_locked = False

    def place_bet(self, stake: float):
        if self.is_locked:
            print("[ERROR] You cannot place a bet while the race is active.")
        elif self.balance-stake > 0:
            self.balance = self.balance - stake
            self.player_bet = Bet(stake)
            print("[SYSTEM] Success. Your bet is locked. Please notice that you cannot withdraw or deposit your balance while the race is active.")
        else:
            print("[ERROR] Insufficient funds. Please deposit money to your balance to proceed.")

    def get_payout(self, amount):
        self.balance = self.balance + amount

    def deposit_funds(self, deposit_amount):
        self.balance = self.balance + deposit_amount

    def getBet(self):
        return self.player_bet