
import streamlit as st
import chess
import chess.svg
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI Virtual Chess",
    page_icon="♟️",
    layout="wide"
)

st.title("♟️ AI Virtual Chess")
st.caption("Play chess against an AI opponent!")

# Initialize game
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

if "game_over" not in st.session_state:
    st.session_state.game_over = False

board = st.session_state.board

# AI move
def ai_move(board):
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return

    # Simple AI: prioritize captures
    captures = [
        move for move in legal_moves
        if board.is_capture(move)
    ]

    if captures:
        move = random.choice(captures)
    else:
        move = random.choice(legal_moves)

    board.push(move)

# Display chessboard
def show_board():
    svg = chess.svg.board(
        board=board,
        size=500,
        coordinates=True
    )

    components.html(svg, height=530)

# Game controls
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 New Game"):
        st.session_state.board = chess.Board()
        st.rerun()

with col2:
    if st.button("↩️ Undo Move"):
        if len(board.move_stack) > 0:
            board.pop()

        if len(board.move_stack) > 0 and not board.turn:
            board.pop()

        st.rerun()

# Display board
show_board()

# Move input
st.subheader("Make Your Move")

if not board.is_game_over():

    if board.turn == chess.WHITE:

        move_text = st.text_input(
            "Enter your move (example: e2e4)",
            placeholder="e2e4"
        )

        if st.button("Make Move"):
            try:
                move = chess.Move.from_uci(move_text.strip())

                if move in board.legal_moves:
                    board.push(move)

                    if not board.is_game_over():
                        ai_move(board)

                    st.rerun()

                else:
                    st.error("Illegal move! Try another move.")

            except ValueError:
                st.error("Invalid format! Use notation like e2e4.")

    else:
        st.info("AI is thinking...")

# Game status
if board.is_checkmate():
    st.success(
        "Checkmate! " +
        ("Black wins!" if board.turn == chess.WHITE else "White wins!")
    )

elif board.is_stalemate():
    st.warning("Draw by stalemate!")

elif board.is_game_over():
    st.info(f"Game Over: {board.result()}")

elif board.is_check():
    st.warning("Check!")

st.subheader("Game Information")

st.write("**Current turn:**",
         "White" if board.turn == chess.WHITE else "Black")

st.write("**Moves played:**", len(board.move_stack))

with st.expander("Move History"):
    st.write(" ".join(
        f"{i // 2 + 1}. {move.uci()}"
        for i, move in enumerate(board.move_stack)
    ))

