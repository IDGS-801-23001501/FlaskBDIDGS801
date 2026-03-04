from flask import render_template, request, redirect, url_for

import form
from models import Meestros
from models import db
from . import maestros


@maestros.route("/maestros", methods=["GET", "POST"])
def list_maestros():
    create_form = form.TeacherForm(request.form)
    maestros_list = Meestros.query.all()
    return render_template(
        "maestros/listadoMaes.html", form=create_form, maestros=maestros_list
    )


@maestros.route("/maestros/crear", methods=["GET", "POST"])
def create_maestros():
    create_form = form.TeacherForm(request.form)
    if request.method == "POST":
        maestro = Meestros(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.correo.data,
            especialidad=create_form.especialidad.data,
        )
        db.session.add(maestro)
        db.session.commit()
        return redirect(url_for("maestros.list_maestros"))
    return render_template("maestros/crear.html", form=create_form)


@maestros.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar_maestro():
    create_form = form.TeacherForm(request.form)

    if request.method == "GET":
        matricula = request.args.get("matricula")
        maestro = (
            db.session.query(Meestros).filter(Meestros.matricula == matricula).first()
        )

        print(maestro)

        if maestro:
            create_form.nombre.data = maestro.nombre
            create_form.apellidos.data = maestro.apellidos
            create_form.correo.data = maestro.email
            create_form.especialidad.data = maestro.especialidad

            return render_template(
                "maestros/eliminar.html",
                form=create_form,
                matricula=matricula,
                nombre=maestro.nombre,
                apellidos=maestro.apellidos,
                especialidad=maestro.especialidad,
                email=maestro.email,
            )

    if request.method == "POST":
        matricula = request.args.get("matricula")
        maestro = (
            db.session.query(Meestros).filter(Meestros.matricula == matricula).first()
        )

        if maestro:
            db.session.delete(maestro)
            db.session.commit()

        return redirect(url_for("maestros.list_maestros"))

    return render_template("maestros/eliminar.html", form=create_form)


@maestros.route("/maestros/modificar", methods=["GET", "POST"])
def modificar_maestro():
    create_form = form.TeacherForm(request.form)
    matricula = request.args.get("matricula")

    # Si no viene matricula, redirige
    if not matricula:
        return redirect(url_for("maestros.list_maestros"))

    maestro = db.session.query(Meestros).filter(Meestros.matricula == matricula).first()

    # Si no existe el maestro, redirige
    if not maestro:
        return redirect(url_for("maestros.list_maestros"))

    if request.method == "GET":
        create_form.nombre.data = maestro.nombre
        create_form.apellidos.data = maestro.apellidos
        create_form.correo.data = maestro.email
        create_form.especialidad.data = maestro.especialidad

        return render_template(
            "maestros/modificar.html",
            form=create_form,
            matricula=matricula,
            nombre=maestro.nombre,
            apellidos=maestro.apellidos,
            especialidad=maestro.especialidad,
            email=maestro.email,
        )

    if request.method == "POST":
        maestro.nombre = create_form.nombre.data
        maestro.apellidos = create_form.apellidos.data
        maestro.email = create_form.correo.data
        maestro.especialidad = create_form.especialidad.data

        db.session.commit()
        return redirect(url_for("maestros.list_maestros"))


@maestros.route("/maestros/detalles", methods=["GET", "POST"])
def detalles():
    create_form = form.UserForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")
        # select * from alumnos where id == id
        maestro = (
            db.session.query(Meestros).filter(Meestros.matricula == matricula).first()
        )

        nombre = maestro.nombre
        apellidos = maestro.apellidos
        email = maestro.email
        especialidad = maestro.especialidad

        return render_template(
            "maestros/detalles.html",
            nombre=nombre,
            apellidos=apellidos,
            email=email,
            especialidad=especialidad,
        )


@maestros.route("/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil {nombre}"
