"""
Souken NAC — Breakthrough Console Web Server
Flask app serving the Breakthrough Console UI.

© 2019-2026 Souken Industries. All rights reserved.
"""

import json
import os
import sys
import threading

from flask import Flask, request, jsonify, send_from_directory, Response
import time

# Ensure sibling imports work
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)

from breakthrough import (
    generate_breakthrough, ship_breakthrough,
    load_state, save_state, UPLOADS_DIR
)

app = Flask(__name__, static_folder=None)

# Global state for current session
_current_result = None
_ship_log = []
_ship_done = False
_ship_error = None


@app.route("/")
def index():
    """Serve the console HTML."""
    templates_dir = os.path.join(_THIS_DIR, "templates")
    return send_from_directory(templates_dir, "console.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Generate a new breakthrough artifact."""
    global _current_result
    state = load_state()
    image_path = request.json.get("image_path") if request.json else None
    mermaid_code = request.json.get("mermaid_code") if request.json else None

    result = generate_breakthrough(state, image_path=image_path, mermaid_code=mermaid_code)
    _current_result = result

    return jsonify({
        "type": result["type"],
        "content": result["content"],
        "summary": result["summary"],
        "metadata": result["metadata"],
    })


@app.route("/regenerate", methods=["POST"])
def regenerate():
    """Regenerate with optional feedback (just re-rolls with new seed)."""
    global _current_result
    state = load_state()
    data = request.json or {}
    image_path = data.get("image_path")
    mermaid_code = data.get("mermaid_code")

    # Bump run_count to get a different seed
    state["run_count"] = state.get("run_count", 0) + 100

    result = generate_breakthrough(state, image_path=image_path, mermaid_code=mermaid_code)
    _current_result = result

    return jsonify({
        "type": result["type"],
        "content": result["content"],
        "summary": result["summary"],
        "metadata": result["metadata"],
    })


@app.route("/upload-image", methods=["POST"])
def upload_image():
    """Accept an image upload, save to uploads/, return the path."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    os.makedirs(UPLOADS_DIR, exist_ok=True)
    save_path = os.path.join(UPLOADS_DIR, f.filename)
    f.save(save_path)

    # If we have a current result, re-inject the image
    global _current_result
    if _current_result:
        _current_result["image_path"] = save_path

    return jsonify({"path": save_path, "filename": f.filename})


@app.route("/update-content", methods=["POST"])
def update_content():
    """Update the current result's content (user edited it)."""
    global _current_result
    if not _current_result:
        return jsonify({"error": "No breakthrough generated yet"}), 400

    data = request.json or {}
    if "content" in data:
        _current_result["content"] = data["content"]
        # Update the file content in files_to_commit
        for i, (path, _) in enumerate(_current_result["files_to_commit"]):
            if path == _current_result["metadata"]["file_path"]:
                _current_result["files_to_commit"][i] = (path, data["content"])
                break

    if "mermaid_code" in data and data["mermaid_code"]:
        mermaid_code = data["mermaid_code"]
        content = _current_result["content"]
        # Insert mermaid block if not already present
        if "```mermaid" not in content:
            mermaid_block = f"\n\n### System Architecture\n\n```mermaid\n{mermaid_code.strip()}\n```\n"
            if "## Architecture" in content:
                content = content.replace("## Architecture", f"## Architecture\n{mermaid_block}", 1)
            elif "## Design" in content:
                content = content.replace("## Design", f"## Design\n{mermaid_block}", 1)
            elif "## Methodology" in content:
                content = content.replace("## Methodology", f"## Methodology\n{mermaid_block}", 1)
            else:
                content += mermaid_block
            _current_result["content"] = content
            for i, (path, _) in enumerate(_current_result["files_to_commit"]):
                if path == _current_result["metadata"]["file_path"]:
                    _current_result["files_to_commit"][i] = (path, content)
                    break

    return jsonify({"ok": True})


@app.route("/ship", methods=["POST"])
def ship():
    """Ship the current breakthrough (async)."""
    global _current_result, _ship_log, _ship_done, _ship_error

    if not _current_result:
        return jsonify({"error": "No breakthrough to ship"}), 400

    _ship_log = []
    _ship_done = False
    _ship_error = None

    def _do_ship():
        global _ship_done, _ship_error
        try:
            def log_cb(msg):
                _ship_log.append(msg)

            result = ship_breakthrough(_current_result, status_callback=log_cb)
            if not result["success"]:
                _ship_error = result.get("error", "Unknown error")
        except Exception as e:
            _ship_error = str(e)
        finally:
            _ship_done = True

    thread = threading.Thread(target=_do_ship, daemon=True)
    thread.start()

    return jsonify({"started": True})


@app.route("/ship-status")
def ship_status():
    """SSE endpoint for shipping progress."""
    def event_stream():
        seen = 0
        while True:
            if len(_ship_log) > seen:
                for msg in _ship_log[seen:]:
                    yield f"data: {json.dumps({'msg': msg})}\n\n"
                seen = len(_ship_log)
            if _ship_done:
                if _ship_error:
                    yield f"data: {json.dumps({'done': True, 'error': _ship_error})}\n\n"
                else:
                    yield f"data: {json.dumps({'done': True})}\n\n"
                break
            time.sleep(0.3)

    return Response(event_stream(), mimetype="text/event-stream")


@app.route("/state")
def get_state():
    """Return current breakthrough state."""
    return jsonify(load_state())


if __name__ == "__main__":
    print("\n  SOUKEN INDUSTRIES — Breakthrough Console")
    print("  http://localhost:5555\n")
    app.run(host="127.0.0.1", port=5555, debug=False)
