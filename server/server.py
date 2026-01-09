from flask import Flask

app = Flask("MiTyT-Server")

@app.route("/", methods=["GET"])
def status():
    return "App Funcionando"

app.run(port=5000)