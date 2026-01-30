from flask import Flask, render_template

app = Flask("MiTyT-Server")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/perfil")
def perfi():
    return render_template("perfil.html")


app.run(debug=True, port=5000)