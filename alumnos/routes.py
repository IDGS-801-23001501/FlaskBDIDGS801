from flask import render_template, request, redirect, url_for
from sqlalchemy.orm import joinedload

import form
from models import db, Alumnos
from . import alumnos


@alumnos.route("/alumnos")
@alumnos.route("/alumnos/index")
def index():
    create_form = form.UserForm(request.form)
    # ORM SELECT * FROM alumnos;
    alumnos = Alumnos.query.all()
    return render_template("index.html", form=create_form, alumnos=alumnos)


@alumnos.route("/alumnos/crear", methods=["GET", "POST"])
def create_alumnos():
    create_form = form.UserForm(request.form)
    if request.method == "POST":
        alumno = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.correo.data,
            telefono=create_form.telefono.data,
        )
        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("alumnos.index"))

    return render_template("alumnos.html", form=create_form)


@alumnos.route("/alumnos/detalles", methods=["GET", "POST"])
def detalles():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id", type=int)
        # select * from alumnos where id == id
        alumno = (
            db.session.query(Alumnos)
            .options(joinedload(Alumnos.cursos))
            .filter(Alumnos.id == id)
            .first()
        )

        if not alumno:
            return redirect(url_for("alumnos.index"))

        nombre = alumno.nombre
        apellidos = alumno.apellidos
        email = alumno.email
        telefono = alumno.telefono
        cursos = alumno.cursos

        return render_template(
            "detalles.html",
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
            cursos=cursos,
        )


@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        nombre = alumno.nombre
        apellidos = alumno.apellidos
        email = alumno.email
        telefono = alumno.telefono
        return render_template(
            "modificar.html",
            id=id,
            form=create_form,
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            telefono=telefono,
        )

    if request.method == "POST":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alumno.id = id
        alumno.nombre = create_form.nombre.data
        alumno.apellidos = create_form.apellidos.data
        alumno.email = create_form.correo.data
        alumno.telefono = create_form.telefono.data

        db.session.add(alumno)
        db.session.commit()
        return redirect(url_for("alumnos.index"))
    return None


@alumnos.route("/alumnos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alumno:
            create_form.matricula.data = alumno.id
            create_form.nombre.data = alumno.nombre
            create_form.apellidos.data = alumno.apellidos
            create_form.correo.data = alumno.email
            create_form.telefono.data = alumno.telefono
            return render_template(
                "eliminar.html",
                form=create_form,
                nombre=alumno.nombre,
                apellidos=alumno.apellidos,
                email=alumno.email,
                matricula=alumno.id,
                telefono=alumno.telefono,
            )

    if request.method == "POST":
        id = request.args.get("id")
        alumno = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alumno:
            db.session.delete(alumno)
            db.session.commit()
        return redirect(url_for("alumnos.index"))

    return render_template("eliminar.html", form=create_form)
