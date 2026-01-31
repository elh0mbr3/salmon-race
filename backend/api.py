# importing external libraries
import time
import numpy as np
import pandas as pd
from pathlib import Path
from flask import Flask, request

# importing classes
from game_state.player import Player
from game_state.fish import Fish
from game_state.race import Race, BetType

app = Flask(__name__)

active_players = {}
# user = ""

def getFishCsv():
    filePath = Path("../fish.csv")
    if not filePath.exists():
        return None
    df = pd.read_csv(filePath)
    return df

def selectFish():
    df = getFishCsv()

    if df is None:
        return []

    n = min(10, len(df))
    selectedFish = df.sample(n=n)[["Name", "Odds", "Sprite"]].to_dict('records')
    return selectedFish

def updateFishLocations(fishes: list[Fish], tick_count: int):
    for fish in fishes:
        base_speed = (1 / fish.odds) * 50
        random_multiplier = np.random.uniform(0.5, 1.5)
        movement = base_speed * random_multiplier * tick_count
        fish.setXPosition(fish.getXPosition() + movement)

def calculateAllFinished(fishes: list[Fish]):
    for fish in fishes:
        if fish.getXPosition() < 5000:
            return False
    return True

# --- API ROUTES/CALLS ---

@app.route("/")
def blank():
    return "<p>Backend - running</p>"

@app.route("/<file>")
def page(file):
    return "<p>"+file+"</p>"

# for creating a player
@app.route("/api/sendUname", methods=['GET'])
def sendUname():
    username = request.args.get('username')

    if username:
        new_player = Player(username)
        # user = new_player.username
        active_players[username] = new_player
        return f"<p>Success. '{new_player.username}' is created with ID - {new_player.ID}</p>"

    else:
        return "<p>Error: No username provided.</p>"

# SEND_BET
@app.route("/api/sendBet", methods=['GET'])
def sendBet():
    username = request.args.get('username')
    stake = request.args.get('stake')

    if not username or not stake:
        return "<p>Error: Missing username or stake.</p>"
    
    current_player = active_players.get(username)

    if not current_player:
        return "<p>Error: Player not found. Please login first.</p>"
    
    try:
        stake_amount = float(stake)
        current_player.place_bet(stake_amount)
        return f"<p>Bet places. Balance: {current_player.balance}</p>"
    except ValueError:
        return "<p>Error: Stake must be a number</p>"
        
@app.route("/api/startRace", methods=["GET"])
def startRace():

    fish_data = selectFish()
    if not fish_data:
        return "<p>Error: fish.csv is missing or empty</p>"
    current_fishes = []
    for data in fish_data:
        f = Fish(data["Name"])
        f.odds = float(data["Odds"])
        f.sprite = data["Sprite"]

        current_fishes.append(f)

    tick_count = 0

    while not calculateAllFinished(current_fishes):
        tick_count += 1

        updateFishLocations(current_fishes, tick_count)

        if tick_count > 5000:
            break

    current_fishes.sort(key=lambda f: f.getXPosition(), reverse=True)
    winner = current_fishes[0]

    positions_str = ",".join([f"{f.getName()}={f.sprite}={round(f.getXPosition(), 2)}" for f in current_fishes])
    response_text = f"{winner.getName()}|{tick_count}|{positions_str}"

    return response_text

if __name__ == "__main__":
    app.run(port=5000, debug=True)

# @app.route("/test/<sendUname>")
# def sendUname(sendUname):
#     return "<p>username: "+sendUname+"</p>"


# if __name__ == "__main__":
#     app.run(debug=True)
