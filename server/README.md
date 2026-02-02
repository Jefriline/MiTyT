# Server MiTyT

## Variables de entorno

Definir en un archivo `.env` en la **raíz del proyecto** (carpeta que contiene `server/`):

| Variable      | Descripcion |
|---------------|-------------|
| `PORT`        | Puerto del servidor (ej: `5000`). Si no se define, se usa `5000`. |
| `SECRET_KEY`  | Clave secreta usada por Flask para firmar la sesión. |
| `CORS_ORIGINS` | Origenes permitidos para CORS. Si no se define, se usa `*`. En produccion  (ej: `https://miapp.com` o varias separadas por coma: `https://miapp.com,https://www.miapp.com`). |



---

## Archivo JSON de configuracion (Firebase)

**Donde crearlo:** `server/config/firebase/config-firebase.json`

El servidor usa Pyrebase y lee la config desde ese archivo. Sin el archivo, la app falla al importar Firebase.

**Estructura del JSON** (claves requeridas):

```json
{
  "apiKey": "...",
  "authDomain": "...",
  "databaseURL": "https://TU-PROYECTO-default-rtdb.firebaseio.com",
  "projectId": "...",
  "storageBucket": "...",
  "messagingSenderId": "...",
  "appId": "...",
  "measurementId": "..."
}
```

---

## Ejecucion

**Desarrollo (desde la carpeta `server/`):**

```bash
python server.py
```


**Produccion con Waitress (Windows, desde la carpeta `server/`):**

```bash
waitress-serve --host=0.0.0.0 --port=5000 server:app
```

Si se ejecuta desde la raiz del proyecto (carpeta que contiene `server/`), usar en su lugar:

```bash
waitress-serve --host=0.0.0.0 --port=5000 server.server:app
```

**Produccion con Gunicorn (Linux/Docker, desde la raiz del proyecto):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "server.server:app"
```

Gunicorn no soporta Windows; en Windows usar Waitress o `python server.py`.
