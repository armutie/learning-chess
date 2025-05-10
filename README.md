# Pygame Chess

A classic game of Chess implemented in Python using the Pygame library. This project features all standard chess rules, including piece movements, captures, check, checkmate, stalemate, castling, en passant, and pawn promotion.

## Features

*   **Graphical User Interface:** Play chess on a visual board using Pygame.
*   **Standard Piece Movements:** All pieces (Pawn, Rook, Knight, Bishop, Queen, King) move according to official chess rules.
*   **Special Moves:**
    *   **Castling:** Kingside and Queenside castling are implemented.
    *   **En Passant:** Pawns can capture en passant.
    *   **Pawn Promotion:** Pawns reaching the opposite end of the board can be promoted to a Queen, Rook, Bishop, or Knight.
*   **Game End Conditions:**
    *   **Check:** The game indicates when a King is in check.
    *   **Checkmate:** Detects and declares a winner upon checkmate.
    *   **Stalemate:** Detects and declares a draw in stalemate situations.
*   **Turn-Based Gameplay:** Alternating turns for white and black players.
*   **Legal Move Highlighting:** When a piece is selected, its legal moves and potential captures are visually indicated on the board.

## Screenshot / GIF

<img width="386" alt="Image" src="https://github.com/user-attachments/assets/a583dbf7-8140-46ba-a42b-d23f102ae1a3" />

## How to Run

### Prerequisites

*   Python 3.x
*   Pygame library

### Installation

1.  **Clone the repository (or download the files):**
    ```bash
    git clone https://github.com/armutie/learning-chess
    cd learning-chess
    ```

2.  **Install Pygame:**
    ```bash
    pip install pygame
    ```

3.  **Ensure assets are present:**
    The game requires images for the chess pieces and board elements. Make sure the `imgs` folder with all necessary `.png` files is in the same directory as `chess.py`. The required images are:
    *   `Board.png`
    *   `legal_move.png`
    *   `capturable.png`
    *   `promotion_white.png`
    *   `promotion_black.png`
    *   `black_rook.png`, `black_knight.png`, `black_bishop.png`, `black_queen.png`, `black_king.png`, `black_pawn.png`
    *   `white_rook.png`, `white_knight.png`, `white_bishop.png`, `white_queen.png`, `white_king.png`, `white_pawn.png`

### Running the Game

Execute the main game file:

```bash
python chess.py
```

## Project Structure

*   `chess.py`: The main game file. It initializes Pygame, sets up the game window, handles the game loop, player input, and manages overall game state. It also defines the `Game` and `Renderer` classes.
*   `chess_pieces.py`: Defines the classes for each chess piece (`Piece`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`, `Pawn`). Each piece class handles its own movement logic and drawing.
*   `imgs/`: A directory containing all the image assets used for the chess board, pieces, and UI elements.

## Code Overview

### `chess_pieces.py`

*   **`Piece` (Base Class):**
    *   Attributes: color, image, position, rectangle (`rect`), `active` status, `first_move` flag.
    *   Methods: `draw()` (to draw the piece), `legal_moves()` (placeholder, overridden by subclasses), `draw_legal()` (to show move/capture indicators), `move()` (to update piece position on the board).
*   **Specific Piece Classes (`Rook`, `Knight`, etc.):**
    *   Inherit from `Piece`.
    *   Override `legal_moves(self, board, previous_move=None)` to implement their specific movement rules, including checking board boundaries and interactions with other pieces.
    *   `King` and `Pawn` classes have more complex logic for special moves (castling, en passant, initial two-square move).
    *   `King.move()` is overridden to handle the Rook's movement during castling.

### `chess.py`

*   **Global Setup:** Initializes Pygame, loads images, defines constants like `TILE_SIZE`.
*   **`Game` Class:**
    *   Manages the game board (`self.board`), current turn (`self.turn`), last move (`self.last_move`).
    *   `mouse_to_square()`: Converts mouse click coordinates to board grid coordinates.
    *   `validated_moves()`: Filters a piece's raw legal moves to ensure a move does not leave the player's own King in check. This is critical for chess legality.
    *   `in_check()`: Determines if a given side's King is currently under attack.
    *   `pawn_promotion()`: Handles the logic for promoting a pawn.
    *   `checkmate()`: Checks for checkmate or stalemate conditions.
    *   `play()`: The main game loop, handling events, player turns, move execution, and game state updates.
*   **`Renderer` Class:**
    *   `redraw_board()`: Draws the entire game state (board, pieces, legal move indicators).
    *   `render_promotion()`: Displays the UI for pawn promotion choices.

## Potential Future Improvements & Refinements

*   **Refactor Castling Validation Undo:** The undo logic within `Game.validated_moves` for castling checks could be made more robust and generalized.
*   **AI Opponent:** Implement an AI using algorithms like Minimax with Alpha-Beta Pruning.
*   **Move History & Notation:** Display a list of moves made during the game using algebraic notation.
*   **Sound Effects:** Add sounds for piece movements, captures, check, etc.
*   **More UI/UX Enhancements:**
    *   Highlight the last move made.
    *   Clearer indication of whose turn it is.
    *   A menu system (New Game, Options, Exit).
    *   Selectable piece sets/themes.
*   **Configuration File:** For settings like `TILE_SIZE`, colors, etc.
*   **Test Suite:** Implement unit tests for piece movements and game logic.
