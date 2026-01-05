# Rock–Paper–Scissors–Plus Referee (Google ADK)

This repository implements a minimal **Rock–Paper–Scissors–Plus** game referee chatbot using **Python** and **Google ADK**.

The project focuses on correct game logic, explicit state management, and tool-based reasoning, rather than UI or external integrations.

---

## Game Overview

The chatbot acts as a referee between a user and a bot in a **best-of-3** game.

### Rules
- Best of 3 rounds  
- Valid moves: `rock`, `paper`, `scissors`, `bomb`  
- `bomb` can be used once per player  
- `bomb` beats all other moves  
- `bomb` vs `bomb` → draw  
- Invalid input wastes the round  
- Game ends automatically after 3 rounds  

---

## Architecture

### State Model

Game state is stored in a `GameState` dataclass:
- Current round
- User and bot scores
- Bomb usage (per player)
- Game completion flag

State persists across turns and is **not stored in the prompt**.

---

### Tools (Google ADK)

Two explicit ADK tools are defined:

#### `validate_move`
- Validates user input  
- Enforces bomb usage constraints  

#### `resolve_round`
- Determines the bot move  
- Resolves round outcome  
- Updates scores, rounds, and game state  

All state mutation happens through these tools.

---

### Agent Design

A single Google ADK `Agent` is used to:
- Define the game rules and behavior  
- Register tools for validation and logic  
- Act as the game referee  

The conversational loop is driven via a **simple CLI**, keeping I/O separate from logic.

---

## Execution Flow

1. Rules are displayed to the user  
2. User inputs a move  
3. Input is validated using an ADK tool  
4. If valid, the round is resolved using an ADK tool  
5. Round result and scores are displayed  
6. Game ends automatically after 3 rounds  

---

## How to Run
Activate your virtual environment and run the below commands:

```bash
pip install -r requirements.txt
python main.py
