"""GROOM AI - Website Engine: project manager for Website Builder."""
from flask import Blueprint, request, jsonify, session
import os, json, uuid, re

website_engine = Blueprint("website_engine", __name__)
WEBSITES_FOLDER = "websites"
os.makedirs(WEBSITES_FOLDER, exist_ok=True)

def get_user_id():
    user_id = session.get("user_id")
    if not user_id:
        user_id = uuid.uuid4().hex
        session["user_id"] = user_id
    return user_id

def get_user_websites_folder():
    folder = os.path.join(WEBSITES_FOLDER, get_user_id())
    os.makedirs(folder, exist_ok=True)
    return folder

def safe_project_id(project_id):
    if not project_id or not re.fullmatch(r"[a-zA-Z0-9_-]+", project_id):
        return None
    return project_id

def get_project_folder(project_id):
    project_id = safe_project_id(project_id)
    return os.path.join(get_user_websites_folder(), project_id) if project_id else None

def get_project_file(project_id):
    folder = get_project_folder(project_id)
    return os.path.join(folder, "project.json") if folder else None

@website_engine.route("/website/create", methods=["POST"])
def create_website():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "Untitled Website")).strip() or "Untitled Website"
    project_id = "website_" + uuid.uuid4().hex[:12]
    folder = get_project_folder(project_id)
    os.makedirs(folder, exist_ok=True)
    project = {"id": project_id, "name": name, "html": "", "css": "", "js": ""}
    with open(get_project_file(project_id), "w", encoding="utf-8") as f:
        json.dump(project, f, indent=4, ensure_ascii=False)
    return jsonify({"success": True, "project": project})

@website_engine.route("/website/list", methods=["GET"])
def list_websites():
    folder = get_user_websites_folder()
    projects = []
    for project_id in sorted(os.listdir(folder)):
        project_file = get_project_file(project_id)
        if not project_file or not os.path.isfile(project_file):
            continue
        try:
            with open(project_file, "r", encoding="utf-8") as f:
                project = json.load(f)
            projects.append({"id": project.get("id", project_id), "name": project.get("name", "Untitled Website")})
        except (OSError, json.JSONDecodeError):
            continue
    return jsonify({"success": True, "projects": projects})

@website_engine.route("/website/<project_id>", methods=["GET"])
def get_website(project_id):
    project_file = get_project_file(project_id)
    if not project_file or not os.path.isfile(project_file):
        return jsonify({"success": False, "error": "Website project not found."}), 404
    try:
        with open(project_file, "r", encoding="utf-8") as f:
            project = json.load(f)
    except (OSError, json.JSONDecodeError):
        return jsonify({"success": False, "error": "Could not read website project."}), 500
    return jsonify({"success": True, "project": project})

@website_engine.route("/website/<project_id>/save", methods=["POST"])
def save_website(project_id):
    project_file = get_project_file(project_id)
    if not project_file or not os.path.isfile(project_file):
        return jsonify({"success": False, "error": "Website project not found."}), 404
    data = request.get_json(silent=True) or {}
    try:
        with open(project_file, "r", encoding="utf-8") as f:
            project = json.load(f)
        if "name" in data:
            project["name"] = str(data["name"]).strip() or "Untitled Website"
        for key in ("html", "css", "js"):
            if key in data:
                project[key] = str(data[key])
        with open(project_file, "w", encoding="utf-8") as f:
            json.dump(project, f, indent=4, ensure_ascii=False)
    except (OSError, json.JSONDecodeError):
        return jsonify({"success": False, "error": "Could not save website project."}), 500
    return jsonify({"success": True, "project": project})

@website_engine.route("/website/<project_id>/delete", methods=["POST"])
def delete_website(project_id):
    folder = get_project_folder(project_id)
    if not folder or not os.path.isdir(folder):
        return jsonify({"success": False, "error": "Website project not found."}), 404
    for name in os.listdir(folder):
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            os.remove(path)
    os.rmdir(folder)
    return jsonify({"success": True, "message": "Website deleted."})
