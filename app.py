from flask import Flask, render_template
from flask_wtf import CSRFProtect

from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/alumnos")
def alumnos():
    return render_template("alumnos.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
