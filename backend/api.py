from flask import Flask, request
from game_state.player import Player

app = Flask(__name__)

active_players = []
user = ""

@app.route("/")
def blank():
    return "<p>nothing</p>"

@app.route("/<file>")
def page(file):
    return "<p>"+file+"</p>"

# for creating a player
@app.route("/api/sendUname", methods=['GET'])
def sendUname():
    username = request.args.get('username')

    if username:
        new_player = Player(username)
        user = new_player.username
        active_players.append(new_player)
        return f"<p>Success. '{new_player.username}' is created with ID - {new_player.ID}</p>"

    else:
        return "<p>Error: No username provided.</p>"
    
@app.route("/api/sendBet", method=['GET'])
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
    except ValueError:
        return "<p>Error: Stake must be a number</p>"
        

if __name__ == "__main__":
    app.run(port=5000, debug=True)