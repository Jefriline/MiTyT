from functools import wraps

from flask import request, jsonify

ALLOWED_EXTENSIONS = {"xlsx", "xls"}


def _allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def validate_excel_upload(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "file" not in request.files:
            return jsonify({"error": "Falta el archivo en la peticion"}), 400
        file = request.files["file"]
        if not file or not file.filename:
            return jsonify({"error": "No se selecciono ningun archivo"}), 400
        if not _allowed_file(file.filename):
            return jsonify({"error": "Extension no permitida. Use .xlsx"}), 400
        return fn(*args, **kwargs)
    return wrapper
