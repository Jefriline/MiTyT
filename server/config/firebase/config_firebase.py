import json
import os

import pyrebase

_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATH_TO_JSON = os.path.join(_DIR, "config-firebase.json")


def _load_config() -> dict:
    json_from_env = os.getenv("FIREBASE_CONFIG_JSON")
    if json_from_env and json_from_env.strip():
        return json.loads(json_from_env)

    path_from_env = os.getenv("FIREBASE_CONFIG")
    path_to_json = path_from_env if path_from_env else DEFAULT_PATH_TO_JSON
    if not os.path.exists(path_to_json):
        raise FileNotFoundError(
            f"No se encontró el JSON de credenciales. "
            f"Define FIREBASE_CONFIG_JSON (JSON completo) o FIREBASE_CONFIG (ruta al archivo), "
            f"o coloca config-firebase.json en: {DEFAULT_PATH_TO_JSON}"
        )
    with open(path_to_json, encoding="utf-8") as file:
        return json.load(file)


def initialize_firebase():
    config = _load_config()
    database_url = config.get("databaseURL", "")
    if database_url.endswith("/"):
        config["databaseURL"] = database_url.rstrip("/")
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    try:
        print("Conectando a Firebase...")
        database.child("usuarios").get()
        print("Conexión exitosa")
    except Exception as error:
        print(f"Error de conexión: {error}")
    return database


db = initialize_firebase()
