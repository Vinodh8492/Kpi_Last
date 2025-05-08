from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename

logo_bp = Blueprint("logo", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@logo_bp.route("/logo", methods=["GET", "POST"])
def handle_logo():
    if request.method == "POST":
        if "logo" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["logo"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            filename = f"logo.{ext}"  # Always overwrite with same filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            return jsonify({"logoUrl": f"/api/uploads/{filename}"}), 200
        else:
            return jsonify({"error": "Invalid file type"}), 400

    # GET: Return latest uploaded logo (assuming standard name)
    for ext in ALLOWED_EXTENSIONS:
        path = os.path.join(UPLOAD_FOLDER, f"logo.{ext}")
        if os.path.exists(path):
            return jsonify({"logoUrl": f"/api/uploads/logo.{ext}"})
    return jsonify({"logoUrl": ""})

@logo_bp.route("/uploads/<filename>")
def serve_logo(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
