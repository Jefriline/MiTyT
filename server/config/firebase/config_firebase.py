import json
import os

import pyrebase

_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_JSON = os.path.join(_DIR, "config-firebase.json")


def initialize_firebase():
    if not os.path.exists(PATH_TO_JSON):
        raise FileNotFoundError(f"No se encontro el JSON de credenciales en: {PATH_TO_JSON}")
    with open(PATH_TO_JSON, encoding="utf-8") as file:
        config = json.load(file)
    database_url = config.get("databaseURL", "")
    if database_url.endswith("/"):
        config["databaseURL"] = database_url.rstrip("/")
    firebase = pyrebase.initialize_app(config)
    database = firebase.database()
    try:
        print("Conectando a Firebase...")
        database.child("usuarios").get()
        print("Conexion exitosa")
    except Exception as error:
        print(f"Error de conexion: {error}")
    return database


db = initialize_firebase()
