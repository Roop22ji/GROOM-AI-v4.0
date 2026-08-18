
from pathlib import Path

def serve_game(game_id, games_dir):
    game_dir = Path(games_dir) / game_id
    return game_dir if game_dir.is_dir() else None
