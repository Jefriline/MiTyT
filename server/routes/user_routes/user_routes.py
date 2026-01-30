from flask import Blueprint
from controllers.user_controller.users_upload import UsersUploadController
from middlewares.user_middlewares.validate_excel_upload_middleware import validate_excel_upload

upload_controller = UsersUploadController()

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route("/upload", methods=["POST"])
@validate_excel_upload
def users_upload():
    return upload_controller.upload()
