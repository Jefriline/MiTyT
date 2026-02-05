from functools import wraps

from flask import request, jsonify

ALLOWED_EXTENSIONS = {"xlsx"}
MAX_FILE_SIZE_MB = 20


def _allowed_file(filename: str) -> bool:
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def validate_excel_upload(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "file" not in request.files:
            return jsonify({"error": "Falta el archivo en la petición"}), 400
        file = request.files["file"]
        if not file or not file.filename:
            return jsonify({"error": "No se seleccionó ningún archivo"}), 400
        if not _allowed_file(file.filename):
            return jsonify({"error": "Extensión no permitida. Use .xlsx"}), 400
        file.seek(0, 2)
        size_bytes = file.tell()
        file.seek(0)
        if size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024:
            return jsonify({
                "error": f"El archivo supera el límite de {MAX_FILE_SIZE_MB} MB. "
                         f"Comprima o divida el archivo."
            }), 400
        return fn(*args, **kwargs)
    return wrapper
