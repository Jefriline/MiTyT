# Server MiTyT

## Variables de entorno

Definir en un archivo `.env` en la **raíz del proyecto** (carpeta que contiene `server/`):

| Variable      | Descripcion |
|---------------|-------------|
| `PORT`        | Puerto del servidor (ej: `5000`). Si no se define, se usa `5000`. |
| `SECRET_KEY`  | Clave secreta usada por Flask para firmar la sesión. En producción usar un valor aleatorio largo (ej: `python -c "import secrets; print(secrets.token_hex())"`). |
| `CORS_ORIGINS` | Origenes permitidos para CORS. Si no se define, se usa `*`. En producción: `https://tu-dominio.com` o varios separados por coma. |
| `FIREBASE_CONFIG_JSON` | (Opcional) JSON completo de Firebase como texto. Si se define, no se usa el archivo. Útil en Render y entornos sin archivos. |
| `FIREBASE_CONFIG` | (Opcional) Ruta al archivo JSON de Firebase. Si no se define y tampoco `FIREBASE_CONFIG_JSON`, se usa `config-firebase.json` en la carpeta del script. |

**Dónde definir:** `.env` en la raíz del proyecto o en `server/`. Con docker-compose se usa `server/.env` si existe.

---

## Configuracion Firebase

**Opción A – Archivo local (desarrollo / Docker con volumen):**

Crear `server/config/firebase/config-firebase.json` con la config de tu proyecto Firebase.

**Opción B – Variable de entorno (Render, etc.):**

Definir `FIREBASE_CONFIG_JSON` con el **contenido completo** del JSON (una sola línea o multilínea). El servidor lo usa en lugar del archivo.

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