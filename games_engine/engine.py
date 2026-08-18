
from pathlib import Path
import uuid
import json

BASE_DIR = Path(__file__).resolve().parent.parent
GAMES_DIR = BASE_DIR / "games"

def create_game_project(name="groom_game"):
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name).strip("_") or "groom_game"
    project_id = f"{safe_name}_{uuid.uuid4().hex[:8]}"
    project_dir = GAMES_DIR / project_id
    (project_dir / "assets").mkdir(parents=True, exist_ok=True)
    (project_dir / "game.json").write_text(json.dumps({
        "id": project_id, "name": safe_name,
        "engine": "Groom Game Engine", "version": "0.1.0"
    }, indent=2), encoding="utf-8")
    return project_dir

def write_game(project_dir, html, js):
    project_dir = Path(project_dir)
    (project_dir / "index.html").write_text(html, encoding="utf-8")
    (project_dir / "game.js").write_text(js, encoding="utf-8")
    return project_dir / "index.html"
