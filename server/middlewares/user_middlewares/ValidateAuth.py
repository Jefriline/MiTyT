from flask import request
from functools import wraps

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