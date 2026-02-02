# Server MiTyT

## Variables de entorno

Definir en un archivo `.env` en la **raíz del proyecto** (carpeta que contiene `server/`):

| Variable      | Descripcion |
|---------------|-------------|
| `PORT`        | Puerto del servidor (ej: `5000`). Si no se define, se usa `5000`. |
| `SECRET_KEY`  | Clave secreta usada por Flask para firmar la sesión. Debe ser un string aleatorio largo. |



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
