from functools import wraps

from flask import jsonify, request, session


def require_admin_session(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        login_user = session.get("login_user")
        if not login_user or login_user.get("role") != "admin":
            return jsonify({"error": "Solo administradores pueden subir archivos"}), 403
        return func(*args, **kwargs)

    return wrapper


class MiddlewareAuthUser:
    def __init__(self) -> None:
        pass

    def is_authenticated(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            print(f"Validando - Username: {username}, Password: {password}")
            if not username or not password:
                print("Error: Username o password vacíos")
                return {"error": "Usuario y contraseña son requeridos"}, 400
            
            if "@" not in username:
                print("Error: Username no contiene @")
                return {"error": "El usuario debe ser un email válido"}, 400
            
            print("Validación correcta, ejecutando función")
            return func(*args, **kwargs)
        
        return wrapper