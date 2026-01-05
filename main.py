import random
from dataclasses import dataclass
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# -------------------------
# Game State
# -------------------------

@dataclass
class GameState:
    round: int = 1
    user_score: int = 0
    bot_score: int = 0
    user_bomb_used: bool = False
    bot_bomb_used: bool = False
    game_over: bool = False


STATE = GameState()
VALID_MOVES = ["rock", "paper", "scissors", "bomb"]

# -------------------------
# Tool Functions
# -------------------------

def validate_move(move: str) -> dict:
    move = move.lower().strip()

    if move not in VALID_MOVES:
        return {"valid": False, "reason": "Invalid move"}

    if move == "bomb" and STATE.user_bomb_used:
        return {"valid": False, "reason": "Bomb already used"}

    return {"valid": True, "move": move}


def resolve_round(user_move: str) -> dict:
    if STATE.game_over:
        return {"error": "Game already ended"}

    bot_move = random.choice(VALID_MOVES)

    if bot_move == "bomb" and STATE.bot_bomb_used:
        bot_move = random.choice(["rock", "paper", "scissors"])

    if bot_move == "bomb":
        STATE.bot_bomb_used = True
    if user_move == "bomb":
        STATE.user_bomb_used = True

    if user_move == bot_move:
        winner = "draw"
    elif user_move == "bomb":
        winner = "user"
    elif bot_move == "bomb":
        winner = "bot"
    elif (
        (user_move == "rock" and bot_move == "scissors") or
        (user_move == "paper" and bot_move == "rock") or
        (user_move == "scissors" and bot_move == "paper")
    ):
        winner = "user"
    else:
        winner = "bot"

    if winner == "user":
        STATE.user_score += 1
    elif winner == "bot":
        STATE.bot_score += 1

    current_round = STATE.round
    STATE.round += 1

    if STATE.round > 3:
        STATE.game_over = True

    return {
        "round": current_round,
        "user_move": user_move,
        "bot_move": bot_move,
        "winner": winner,
        "user_score": STATE.user_score,
        "bot_score": STATE.bot_score,
        "game_over": STATE.game_over
    }

# -------------------------
# ADK Tools
# -------------------------

validate_tool = FunctionTool(validate_move)
resolve_tool = FunctionTool(resolve_round)

# -------------------------
# ADK Agent
# -------------------------

agent = Agent(
    name="rps_plus_referee",
    instruction="""
You are a referee for Rock–Paper–Scissors–Plus.

Rules:
- Best of 3 rounds
- Moves: rock, paper, scissors, bomb
- Bomb can be used once per player
- Invalid input wastes the round
- Game ends automatically after 3 rounds
""",
    tools=[validate_tool, resolve_tool]
)

# -------------------------
# CLI Game Loop
# -------------------------

def run_game():
    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Best of 3 rounds | bomb usable once\n")

    while not STATE.game_over:
        user_input = input("Your move: ")

        validation = validate_move(user_input)

        if not validation["valid"]:
            print(f"Invalid move ({validation['reason']})")
            STATE.round += 1
            if STATE.round > 3:
                STATE.game_over = True
            continue

        result = resolve_round(validation["move"])

        print(f"\nRound {result['round']}")
        print(f"You played: {result['user_move']}")
        print(f"Bot played: {result['bot_move']}")

        if result["winner"] == "user":
            print("You win the round!")
        elif result["winner"] == "bot":
            print("Bot wins the round!")
        else:
            print("Draw!")

        print(f"Score → You: {result['user_score']} | Bot: {result['bot_score']}\n")

    print("Game Over!")
    if STATE.user_score > STATE.bot_score:
        print("You win the game!")
    elif STATE.bot_score > STATE.user_score:
        print("Bot wins the game!")
    else:
        print("Game Draw!")

if __name__ == "__main__":
    run_game()
