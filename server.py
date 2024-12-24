from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Backend.Backtracking import Backtracking
from Backend.utils.algorithms import backtracking_with_forward_checking, BTS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/api/game/easy', methods=['GET'])
def generate_easy():
    sudoko = Backtracking()
    sudoko.generate_puzzle("Easy")
    sudoko.print_board()
    return jsonify({"board": sudoko.board}), 200


@app.route('/api/game/medium', methods=['GET'])
def generate_medium():
    sudoko = Backtracking()
    sudoko.generate_puzzle("Medium")
    sudoko.print_board()
    return jsonify({"board": sudoko.board}), 200

@app.route('/api/game/hard', methods=['GET'])
def generate_hard():
    sudoko = Backtracking()
    sudoko.generate_puzzle("Hard")
    sudoko.print_board()
    return jsonify({"board": sudoko.board}), 200

@app.route('/api/game/validate_input', methods=['POST'])
def validate_input():
    if not request.json:
        print("request is not json")
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json
    board = data['board']
    sudoko = Backtracking()
    return jsonify({"board": sudoko.validate_input(board)}), 200


@app.route('/api/game/validate_move', methods=['POST'])
def validate_move():
    if not request.json:
        print("request is not json")
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json
    board = data['board']
    move = data['move']
    sudoko = Backtracking()
    sudoko.board = board
    return jsonify({"isValid": sudoko.is_valid(move[0]['row'],move[0]['col'], move[0]['value'])}), 200


@app.route('/api/game/solve', methods=['POST'])
def solve():
    if not request.json:
        print("request is not json")
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.json
    board = data['board']
    original_board = board.copy()
    # addLogs = data['addLogs']
    print("Solving using Backtracking with forward checking" )
    # for i in range(9):
    #     print(board[i])
    assignment = {}
    # if (BTS(assignment,board)):
    if(backtracking_with_forward_checking(board, assignment, True)):
        print("Solved Successfully")
        moves = [(key[0], key[1], value) for key, value in assignment.items()]
    else :
        print("Unsolvable")
        board = original_board
        moves = []

    # sudoko = Backtracking()
    # sudoko.board = board
    # sudoko.solve_sudoku(False)
    # sudoko.ai_moves.reverse()
    # return jsonify({"board": sudoko.board, "moves": sudoko.ai_moves}), 200

    return jsonify({"board": board, "moves": moves}), 200



if __name__ == '__main__':
    app.run(debug=True)
