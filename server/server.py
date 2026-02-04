import os
from flask import Flask, render_template
from flask_cors import CORS
from dotenv import load_dotenv

from routes.user_routes.user_routes import users_bp
from routes.help_routes.help_routes import help_bp


load_dotenv()

base_dir = os.path.abspath(os.path.dirname(__file__))

template_dir = os.path.join(base_dir, '..', 'Client', 'templates')
static_dir = os.path.join(base_dir, "..", "Client", "static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = os.getenv("SECRET_KEY")

_raw_cors = (os.getenv("CORS_ORIGINS") or "*").strip()
CORS_ORIGINS = "*" if _raw_cors == "*" else [origin.strip() for origin in _raw_cors.split(",")]
CORS(app, origins=CORS_ORIGINS, supports_credentials=False)


@app.route("/")
def home():
    turnstile_site_key = os.getenv("TURNSTILE_SITE_KEY", "")
    return render_template("index.html", turnstile_site_key=turnstile_site_key)

app.register_blueprint(users_bp)
app.register_blueprint(help_bp)


PORT = int(os.getenv("PORT", "5000"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
