
from flask import Flask, render_template
import os
from flask_cors import CORS
from dotenv import load_dotenv

from routes.user_routes.user_routes import users_bp


load_dotenv()

app = Flask(__name__, template_folder="../Client/templates")
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

CORS_ORIGINS = "*"
CORS(app, origins=CORS_ORIGINS, supports_credentials=False)


@app.route("/")
def home():
    return render_template("index.html")


app.register_blueprint(users_bp)


PORT = int(os.getenv("PORT", "5000"))
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
