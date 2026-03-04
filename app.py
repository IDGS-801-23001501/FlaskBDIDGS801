from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from alumnos import alumnos
from config import DevelopmentConfig
from maestros import maestros
from models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
csrf.init_app(app)
app.register_blueprint(maestros)
app.register_blueprint(alumnos)
db.init_app(app)
migrate = Migrate(app, db)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
