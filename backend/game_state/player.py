from bet import Bet
from fish import Fish

class Player:
    id: str
    username: str
    balance: float
    is_locked: bool
    player_bet: Bet

    def __init__(self, id: str, username: str) {
        self.id = id
        self.username = username
    }

    def place_bet(self, stake: float, fish: Fish):
        if self.is_locked:
            print("[ERROR] You cannot place a bet while the race is active.")
        elif self.balance > 0:
            balance -= stake
            self.player_bet = Bet(self, fish, stake)
            print("[SYSTEM] Success. Your bet is locked. Please notice that you cannot withdraw or deposit your balance while the race is active.")
        else:
            print("[ERROR] Insufficient funds. Please deposit money to your balance to proceed.")

    def get_payout(self, amount):
        self.balance += amount

    def deposit_funds(self, deposit_amount):
        self.balance += deposit_amount