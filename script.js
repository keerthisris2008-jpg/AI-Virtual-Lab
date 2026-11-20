const game = new Chess();

const board = document.getElementById("board");

let selectedSquare = null;

const pieces = {
    wK: "♔", wQ: "♕", wR: "♖",
    wB: "♗", wN: "♘", wP: "♙",
    bK: "♚", bQ: "♛", bR: "♜",
    bB: "♝", bN: "♞", bP: "♟"
};

function drawBoard() {
    board.innerHTML = "";

    const position = game.board();

    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {

            const square = document.createElement("div");

            square.className = "square " +
                ((row + col) % 2 === 0 ? "white" : "black");

            const piece = position[row][col];

            if (piece) {
                square.textContent =
                    pieces[piece.color + piece.type.toUpperCase()];
            }

            const file = "abcdefgh"[col];
            const rank = 8 - row;
            const squareName = file + rank;

            square.onclick = () => selectSquare(squareName);

            board.appendChild(square);
        }
    }
}

function selectSquare(square) {

    if (selectedSquare === null) {
        selectedSquare = square;
    } else {
        const move = game.move({
            from: selectedSquare,
            to: square,
            promotion: "q"
        });

        selectedSquare = null;

        if (move) {
            drawBoard();

            if (game.game_over()) {
                setTimeout(() => {
                    alert("Game Over!");
                }, 100);
            }
        }
    }
}

drawBoard();
