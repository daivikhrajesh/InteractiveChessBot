from flask import Flask, jsonify, request, send_from_directory, render_template
from chess_ai.main import is_valid_move, move_piece, check_game_status

app = Flask(__name__)

# Serve static files (CSS, JS, images)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Serve the HTML file from the templates directory
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_board', methods=['GET'])
def get_board():
    board_state = get_current_board_state()  # Implement this function
    return jsonify({'board': board_state})

@app.route('/move_piece', methods=['POST'])
def move_piece_endpoint():
    data = request.json
    move = data.get('move')
    success = move_piece(move)
    return jsonify({'success': success})

@app.route('/check_game_status', methods=['GET'])
def check_game_status_endpoint():
    status = check_game_status()
    return jsonify({'status': status})

def get_current_board_state():
    # Example implementation, replace with your actual board state retrieval
    board_state = [['.' for _ in range(8)] for _ in range(8)]
    return board_state

if __name__ == '__main__':
    app.run(debug=True)