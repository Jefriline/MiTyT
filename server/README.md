# Server MiTyT

## Variables de entorno

Definir en un archivo `.env` en la **raíz del proyecto** (carpeta que contiene `server/`):

| Variable      | Descripción |
|---------------|-------------|
| `PORT`        | Puerto del servidor (ej: `5000`). Si no se define, se usa `5000`. |
| `SECRET_KEY`  | Clave secreta usada por Flask para firmar la sesión. En producción usar un valor aleatorio largo (ej: `python -c "import secrets; print(secrets.token_hex())"`). |
| `CORS_ORIGINS` | Origenes permitidos para CORS. Si no se define, se usa `*`. En producción: `https://tu-dominio.com` o varios separados por coma. |
| `FIREBASE_CONFIG_JSON` | (Opcional) JSON completo de Firebase como texto. Si se define, no se usa el archivo. |
| `FIREBASE_CONFIG` | (Opcional) Ruta al archivo JSON de Firebase. Si no se define y tampoco `FIREBASE_CONFIG_JSON`, se usa `config-firebase.json` en la carpeta del script. |
| `TURNSTILE_SITE_KEY` | Site key del widget Cloudflare Turnstile (formulario de búsqueda). |
| `TURNSTILE_KEY` | Secret key de Turnstile para validar el token en el servidor (Siteverify). |
| `EMAIL_SEND` | Cuenta desde la que se envían correos (Gmail API OAuth2). |
| `CLIENT_ID` | OAuth2 Client ID de Google Cloud (tipo aplicación de escritorio o web). |
| `SECRET_CLIENT_ID` | OAuth2 Client Secret. |
| `REFRESH_TOKEN` | Refresh token obtenido con OAuth 2.0 Playground (scope https://mail.google.com). |
| `REDIS_URL` | URL de Redis para la cola de correos (credenciales) y rate limit. Ej: `redis://localhost:6379`. |
| `SITE_URL` | (Opcional) URL publica del sitio |


**Dónde definir:** `.env` en la raíz del proyecto o en `server/`. Con docker-compose se usa `server/.env` si existe.

### Claves de prueba Turnstile (desarrollo / localhost)

Para que la validación **pase** siempre:

| Variable | Valor |
|----------|--------|
| `TURNSTILE_SITE_KEY` | `1x00000000000000000000AA` |
| `TURNSTILE_KEY` | `1x0000000000000000000000000000000AA` |

Para que la validación **falle**:

| Variable | Valor |
|----------|--------|
| `TURNSTILE_SITE_KEY` | `2x00000000000000000000AB` |
| `TURNSTILE_KEY` | `2x0000000000000000000000000000000AA` |

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

## Ejecución

**Desarrollo (desde la carpeta `server/`):**

```bash
python server.py
```


**Produccion con Waitress (Windows, desde la carpeta `server/`):**

```bash
waitress-serve --host=0.0.0.0 --port=5000 server:app
```

Si se ejecuta desde la raíz del proyecto (carpeta que contiene `server/`), usar en su lugar:

```bash
waitress-serve --host=0.0.0.0 --port=5000 server.server:app
```

**Producción con Gunicorn (Linux/Docker, desde la raíz del proyecto):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "server.server:app"
```

Gunicorn no soporta Windows; en Windows usar Waitress o `python server.py`.

---

## Worker de cola de correos

La app encola el envío de correos (credenciales) en Redis. Para que se envíen, **debe estar corriendo el worker** que procesa esa cola.

**Con Docker (docker-compose):** el worker se levanta solo como servicio `email_worker`; no hace falta hacer nada más.

**En desarrollo local:** ejecutar en **otra terminal** (desde la carpeta `server/`):

```bash
python scripts/run_email_worker.py
```

Si no se ejecuta el worker, los correos quedarán en cola y no se enviarán hasta que el worker esté activo. Requiere las mismas variables de entorno que el servidor (sobre todo `REDIS_URL`, `EMAIL_SEND`, `CLIENT_ID`, `SECRET_CLIENT_ID`, `REFRESH_TOKEN`).

