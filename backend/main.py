from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

board = [" " for x in range(9)]
last_player = "None"


# Helper function to check if there is a winner
def check_winner():
    # Define winning combinations
    winning_combinations = [
        # Rows
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        # Columns
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        # Diagonals
        (0, 4, 8),
        (2, 4, 6)
    ]

    # Check for a winner
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] != " ":
            return board[combination[0]]

    return None


# Helper function to check if this is a valid game move
def validate_move(move, player):
    if move is None or player is None:
        return jsonify({"message": "Invalid request. 'move' and 'player' fields are required."}), 400

    if player not in ["X", "O"]:
        return jsonify({"message": "Invalid player. Player must be 'X' or 'O'."}), 400

    if last_player is not None and player == last_player:
        return jsonify({"message": "Invalid move. It's the other player's turn."}), 400

    if move < 0 or move >= len(board) or board[move] != " ":
        return jsonify({"message": "Invalid move. Please choose an empty cell."}), 400

    if check_status() != "Game in progress":
        return jsonify({"message": "The game is over. Please start a new game."}), 400


# Helper function to check the status of the game
def check_status():
    winner = check_winner()
    if winner:
        return f"Player {winner} wins!"
    elif all(cell != " " for cell in board):
        return "It's a tie!"
    else:
        return "Game in progress"


"""
# API route to get the board game 
# for feature use with react frontend
@app.route('/api/board', methods=['GET'])
def get_board():
    return jsonify({"board": board, "status": check_status()})
"""

# API route to get the board game
@app.route('/api/board', methods=['GET'])
def get_board():
    with app.app_context():
        rendered = render_template('board.html', title="My Tic-Tac-Toe Game", board=board, status=check_status())
    return rendered


# API route to update a player's move
@app.route("/api/move", methods=["PUT"])
def update_move():
    global last_player
    move = request.json.get("move")
    player = request.json.get("player")

    validation_error = validate_move(move, player)
    if validation_error:
        return validation_error

    board[move] = player
    last_player = player
    return jsonify({"message": "Move updated successfully."})


if __name__ == '__main__':
    app.run(debug=True)

