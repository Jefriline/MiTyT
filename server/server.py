from flask import Flask, render_template, request, redirect, session

app = Flask("MiTyT-Server")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    try: 
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if username == "admin@mityt.com" and password == "admin123":
                session["login_user"] = {
                    "username": username,
                    "role": "admin"
                }
                return redirect("/perfil")
    except Exception as e:
        return render_template("login.html", error="Error al procesar la solicitud")
    return render_template("login.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/logout")
def logout():
    session.pop("login_user", None)
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    # Aquí iría la lógica para buscar la información basada en la consulta
    results = ["Resultado 1 para " + query, "Resultado 2 para " + query]
    return render_template("results.html", query=query, results=results)
app.run(debug=True, port=5000)