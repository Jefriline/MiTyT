from flask import Blueprint, render_template, request, session, redirect

from controllers.user_controller.users_upload import UsersUploadController
from controllers.user_controller.users_search import UsersSearchController
from controllers.user_controller.users_auth import ControllerAuth
from middlewares.user_middlewares.validate_excel_upload_middleware import validate_excel_upload
from middlewares.user_middlewares.ValidateAuth import MiddlewareAuthUser, require_admin_session
from services.user_service.user_service import UserService

upload_controller = UsersUploadController()
auth_controller = ControllerAuth()
search_controller = UsersSearchController(UserService())
middleware_auth = MiddlewareAuthUser()

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route("/upload", methods=["POST"])
@require_admin_session
@validate_excel_upload
def users_upload():
    return upload_controller.upload()

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    try: 
        if request.method == "GET":
            return render_template("login.html")
        
        if request.method == "POST":
            username = (request.form.get("username") or "").strip()
            password = (request.form.get("password") or "").strip()
            if auth_controller.is_authenticated(username, password):
                return redirect("/users/perfil")
            else: 
                print("Autenticación fallida")
                return render_template("login.html", error="Credenciales inválidas")
    except Exception as e:
        return render_template("login.html", error="Error al procesar la solicitud")
    return render_template("login.html")

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
def searchUsers():
    return search_controller.handle_search()