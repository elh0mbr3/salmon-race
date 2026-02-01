# importing external libraries
import time
import numpy as np
import pandas as pd
from pathlib import Path
from flask import Flask, request, session, jsonify

# importing classes
from game_state.player import Player
from game_state.fish import Fish
# from game_state.race import Race, BetType

app = Flask(__name__)

active_players = {}
active_race_data = []
# user = ""

def getFishCsv():
    base_path = Path(__file__).parent.resolve()
    filePath = base_path / ".." / "fish.csv"
    if not filePath.exists():
        return None
    df = pd.read_csv(filePath)
    return df

def selectFish():
    df = getFishCsv()

    if df is None:
        return None

    n = min(10, len(df))
    if n == 0:
        return None
    return df.sample(n=n)

def updateFishLocations(fishes: list[Fish], odds : float):
    for i, fish in enumerate(fishes):
        random_multiplier = np.random.random()
        fish.setXPosition(fish.getXPosition() + (10 * random_multiplier * odds[i]))

def calculateAllFinished(fishes: list[Fish]):
    num_finished = 0

    for fish in fishes:
        if fish.getXPosition() >= 100:
            num_finished += 1

    if num_finished >= 3:
        return True
    
    if num_finished == len(fishes):
        return True

    return False

def process_payouts(winning_fish_name, winning_odds):
    print(f"\n[DEBUG] --- PROCESSING PAYOUTS ---")
    print(f"[DEBUG] Winner: '{winning_fish_name}' | Odds: {winning_odds}")

    for username in active_players:
        player = active_players[username]

        if player.on_fish == winning_fish_name:
            stake = player.getBet()
            payout = stake * winning_odds
            player.get_payout(payout)
            print(f"[SYSTEM] {username} won! New balance: {player.balance}")
        
        player.on_fish = None
        player.player_bet = 0

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

        return f"<p>Success. '{new_player.username}' is created with ID - {new_player.id}</p>"

    else:
        return "<p>Error: No username provided.</p>"

# SEND_BET
@app.route("/api/sendBet", methods=['GET'])
def sendBet():
    username = request.args.get('username')
    stake = request.args.get('stake')
    on_fish = request.args.get('on_fish')

    if not username or not stake:
        return "<p>Error: Missing username or stake.</p>"
    
    current_player = active_players.get(username)

    if not current_player:
        return "<p>Error: Player not found. Please login first.</p>"
    
    try:
        stake_amount = float(stake)
        current_player.place_bet(stake_amount, on_fish) # adds amount to player's bet
        return f"<p>Bet places. Balance: {current_player.balance}</p>"
    except ValueError:
        return "<p>Error: Stake must be a number</p>"

@app.route("/api/getFishNames", methods=["GET"])
def getFishNames():
    global active_race_data
    df = selectFish()
    if df is None or df.empty:
        return jsonify({"error": "No fish found"}), 404
    
    active_race_data = df.to_dict('records')
    names_list = df["Name"].tolist()

    return jsonify({
        "fish_names": names_list,
        "count": len(names_list)
    })

@app.route("/api/debugState")
def debug_state():
    return jsonify({
        "players_online": list(active_players.keys()),
        "race_data_loaded": len(active_race_data) > 0,
        "fish_count": len(active_race_data)
    }) 

@app.route("/api/startRace", methods=["GET"])
def startRace():
    global active_race_data

    if not active_race_data:
        df_backup = selectFish()
        if df_backup is not None:
            active_race_data = df_backup.to_dict('records')
        else:
            return jsonify({"error": "CSV is missing and no fish is selected"})

    df_selected = pd.DataFrame(active_race_data)

    if df_selected is None or df_selected.empty:
        return "<p>Error: fish.csv is missing or empty</p>"
    
    oddsNp = df_selected["Odds"].to_numpy()

    range_val = oddsNp.max() - oddsNp.min()
    if range_val == 0:
        normOdds = np.full_like(oddsNp, 0.5)
    else:
        normOdds = (oddsNp - oddsNp.min()) / range_val
    
    normOdds += 0.05

    df_selected["NormOdds"] = normOdds

    fish_data = df_selected[["Name", "Odds", "Sprite", "NormOdds"]].to_dict('records')
    current_fishes = []
    for data in fish_data:
        f = Fish(data["Name"])

        # if players "on_fish" value == fish name, add the bet to the fish class
        for player in active_players.values():
            if player.on_fish == f.getName():
                f.addBet(player.getUsername())

        f.odds = float(data["Odds"])
        f.normalised_odds = float(data["NormOdds"])
        f.sprite = data["Sprite"]

        current_fishes.append(f)

    race_history = []
    tick_count = 0

    while not calculateAllFinished(current_fishes):
        tick_count += 1
        updateFishLocations(current_fishes, normOdds)
        snapshot = {
            "positions": {f.getName(): round(f.getXPosition(), 2) for f in current_fishes},
            "tick": tick_count
            }
        race_history.append(snapshot)

        # DEBUG MESSAGES    
        print(f"Tick {tick_count}:")
        for fish in current_fishes:
            print(f"{fish.getName()} position: {fish.getXPosition()}")
        print("---------------------------------------")

        if tick_count > 5000:
            break

    current_fishes.sort(key=lambda f: f.getXPosition(), reverse=True)
    winner = current_fishes[0]

    # positions_str = ",".join([f"{f.getName()}={f.sprite}={round(f.getXPosition(), 2)}" for f in current_fishes])
    # response_text = f"{winner.getName()}|{tick_count}|{positions_str}"
    
    print(f"\n[DEBUG] Race Finished. Winner identified as: {winner.getName()}")
    process_payouts(winner.getName(), winner.odds)

    return jsonify({
        "winner": winner.getName(),
        "total_ticks": tick_count,
        "history": race_history
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)