# Chess AI with Flask and Pygame

This project is a Chess game powered by a combination of a simple AI using Q-learning and a graphical user interface (GUI) using Pygame. It also includes a Flask server for handling web-based interactions, allowing integration with a web frontend. 

## Features
- **Chess AI**: An AI that plays against the user, using a Q-learning algorithm.
- **Graphical Interface**: The chessboard and game pieces are displayed using Pygame, enabling a rich, interactive user experience.
- **User Input**: Players can make moves by typing them in the textbox or directly interacting with the chessboard.
- **Game Status Alerts**: Real-time feedback, including "Check", "Checkmate", "Stalemate", and other game-ending conditions.
- **Web Integration**: Provides a web API to interact with the game state and move pieces through a Flask backend.

## Prerequisites
- Python 3.x
- Pygame
- Flask
- Python-Chess

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chess-ai.git
   cd chess-ai
   ```

2. **Install dependencies**:
   Ensure that you have the required Python libraries installed. You can do this by running:

   ```bash
   pip install -r requirements.txt
   ```

   Make sure your `requirements.txt` file includes:
   ```txt
   pygame
   Flask
   python-chess
   numpy
   ```

3. **Download Chess Piece Images**:
   Make sure you have PNG images for the chess pieces in an `images/` folder under your project directory. The filenames should be in the format `wP.png`, `bP.png`, `wK.png`, etc., where `w` stands for white, `b` for black, and the capital letter represents the piece type (P = Pawn, N = Knight, B = Bishop, R = Rook, Q = Queen, K = King).

## Running the Game

### Running the Chess Game with Pygame
1. **Run the Python Game**:
   To play the game with the GUI, run:

   ```bash
   python chess_ai/board.py
   ```

2. **Gameplay**:
   - The AI will make the first move. You can enter your move in standard algebraic notation (e.g., `e2e4` or `Nf3`) and press enter.
   - Game status alerts like "Checkmate" and "Check" will appear during play.
   - If the game ends, you will be notified with an appropriate message.

### Running the Flask Web App
1. **Start the Flask Server**:
   To interact with the chess game over a web interface, run:

   ```bash
   python chess_ai/app.py
   ```

2. **Access the Web App**:
   Open a web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

   The Flask app provides endpoints for moving pieces and checking game status:
   - `GET /get_board` – Returns the current state of the chessboard.
   - `POST /move_piece` – Moves a piece based on the user input.
   - `GET /check_game_status` – Returns the current status of the game.


## How Q-Learning Works
The AI uses a basic Q-learning algorithm to play the game:
- **State Representation**: The chessboard state is represented by the FEN (Forsyth-Edwards Notation) string.
- **Q-Table**: A Q-table is used to store and update the value of state-action pairs.
- **Rewards**:
  - `10` points for checkmate.
  - `1` point for putting the opponent in check.
  - `0` points for other actions.
  
The AI uses an epsilon-greedy strategy to balance exploration and exploitation during play. The Q-values are updated after each move according to the Q-learning formula.

## Contributing
Feel free to fork this repository, open issues, or submit pull requests if you find any bugs or want to add new features.
