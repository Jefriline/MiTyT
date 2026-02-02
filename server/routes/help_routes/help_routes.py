from flask import Blueprint, render_template


help_bp = Blueprint('Help', __name__, url_prefix='/Help')

@help_bp.route("/video", methods=["GET"])
def help_page():
    return render_template("support_guide.html")