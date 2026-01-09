from flask import Flask

app = Flask("MiTyT-Server")

@app.route("/", methods=["GET"])
def status():
    return "app funcionando"

app.run(port=5000)