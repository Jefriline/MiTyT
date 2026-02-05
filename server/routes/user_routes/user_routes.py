from flask import Blueprint, jsonify, render_template, request, session, redirect

from controllers.user_controller.users_upload import UsersUploadController
from controllers.user_controller.users_search import UsersSearchController
from controllers.user_controller.users_auth import ControllerAuth
from controllers.user_controller.users_credentials_code_controller import (
    CredentialsCodeController,
)
from middlewares.user_middlewares.validate_excel_upload_middleware import validate_excel_upload
from middlewares.user_middlewares.ValidateAuth import MiddlewareAuthUser, require_admin_session
from middlewares.user_middlewares.validate_turnstile_middleware import (
    validate_turnstile,
    validate_turnstile_json,
    validate_turnstile_login,
)
from middlewares.user_middlewares.validate_rate_limit_middleware import (
    validate_credentials_rate_limit,
)
from middlewares.user_middlewares.validate_brute_force_middleware import (
    check_brute_force_code,
    check_brute_force_login,
    increment_brute_force_login,
    clear_brute_force_login,
)
from services.user_service.user_service import UserService

user_service = UserService()
upload_controller = UsersUploadController()
auth_controller = ControllerAuth()
search_controller = UsersSearchController(user_service)
credentials_code_controller = CredentialsCodeController(user_service)
middleware_auth = MiddlewareAuthUser()

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route("/upload", methods=["POST"])
@require_admin_session
@validate_excel_upload
def users_upload():
    return upload_controller.upload()

@users_bp.route("/login", methods=["GET", "POST"])
@validate_turnstile_login
@check_brute_force_login
def login():
    import os
    turnstile_site_key = os.getenv("TURNSTILE_SITE_KEY", "")
    try: 
        if request.method == "GET":
            return render_template("login.html", turnstile_site_key=turnstile_site_key)
        
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = (request.form.get("password") or "").strip()
            if auth_controller.is_authenticated(username, password):
                clear_brute_force_login(username)
                return redirect("/users/perfil")
            else: 
                increment_brute_force_login(username)
                print("Autenticación fallida")
                return render_template("login.html", error="Credenciales inválidas", turnstile_site_key=turnstile_site_key)
    except Exception as error:
        print(f"Error en login: {error}")
        return render_template("login.html", error="Error al procesar la solicitud", turnstile_site_key=turnstile_site_key)
    return render_template("login.html", turnstile_site_key=turnstile_site_key)

@users_bp.route("/perfil")
def perfil():
    if "login_user" not in session:
        return redirect("/users/login")
    return render_template("perfil.html")

@users_bp.route("/logout")
def logout():
    session.pop("login_user", None)
    return redirect("/")

@users_bp.route("/search", methods=["POST"])
@validate_turnstile
def search_users():
    return search_controller.handle_search()


@users_bp.route("/credentials/send-code", methods=["POST"])
@validate_turnstile_json
@validate_credentials_rate_limit
def credentials_send_code():
    response, status = credentials_code_controller.send_code()
    return jsonify(response), status


@users_bp.route("/credentials/validate", methods=["POST"])
@validate_turnstile_json
@check_brute_force_code
def credentials_validate():
    response, status = credentials_code_controller.validate_code()
    return jsonify(response), status