from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import CSRFProtect

import form
from config import DevelopmentConfig
from models import db, Alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


@app.route("/")
@app.route("/index")
def index():
    create_form = form.UserForm(request.form)
    # ORM SELECT * FROM alumnos;
    alumnos = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumnos=alumnos)


@app.route("/alumnos", methods=["GET", "POST"])
def alumnos():
    create_form = form.UserForm(request.form)
    if request.method == "POST":
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellido=create_form.apaterno.data,
            email=create_form.correo.data,
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("alumnos.html", form=create_form)


@app.route("/detalles", methods=["GET", "POST"])
def detalles():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        # select * from alumnos where id == id
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        nombre = alumno.nombre
        apellido = alumno.apellido
        email = alumno.email

        return render_template(
            "detalles.html", nombre=nombre, apellido=apellido, email=email
        )


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        nombre = alumno.nombre
        apellido = alumno.apellido
        email = alumno.email
        return render_template(
            "modificar.html",
            id=id,
            form=create_form,
            nombre=nombre,
            apellido=apellido,
            email=email,
        )

    if request.method == "POST":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alumno.id = id
        alumno.nombre = create_form.nombre.data
        alumno.apellido = create_form.apaterno.data
        alumno.email = create_form.correo.data

        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("index"))
    return None


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()
    app.run()
