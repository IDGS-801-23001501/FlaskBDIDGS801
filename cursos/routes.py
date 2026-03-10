from flask import render_template, request, redirect, url_for

import form
from models import db, Curso, Maestros, Alumnos
from . import cursos


@cursos.route("/cursos")
@cursos.route("/cursos/index")
def index():
    cursos_list = Curso.query.all()
    return render_template("cursos/index.html", cursos=cursos_list)


@cursos.route("/cursos/crear", methods=["GET", "POST"])
def crear_curso():

    create_form = form.CursoForm(request.form)

    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]

    if request.method == "POST" and create_form.validate():
        nuevo_curso = Curso(
            nombre=create_form.nombre.data, maestro_id=create_form.maestro_id.data
        )

        db.session.add(nuevo_curso)
        db.session.commit()

        return redirect(url_for("cursos.index"))

    return render_template("cursos/crear.html", form=create_form)


@cursos.route("/cursos/detalles")
def detalles():

    id = request.args.get("id")
    curso = Curso.query.get_or_404(id)

    alumnos = curso.alumnos  # ya inscritos

    return render_template("cursos/detalles.html", curso=curso, alumnos=alumnos)


@cursos.route("/cursos/inscribir", methods=["GET", "POST"])
def inscribir():

    curso_id = request.args.get("id")
    curso = Curso.query.get_or_404(curso_id)

    if request.method == "POST":
        alumno_id = request.form.get("alumno_id")
        alumno = Alumnos.query.get(alumno_id)

        if alumno not in curso.alumnos:
            curso.alumnos.append(alumno)
            db.session.commit()

        return redirect(url_for("cursos.detalles", id=curso_id))

    # Solo mostrar alumnos que NO estén inscritos
    alumnos_disponibles = Alumnos.query.filter(
        ~Alumnos.id.in_([a.id for a in curso.alumnos])
    ).all()

    return render_template(
        "cursos/inscribir.html", curso=curso, alumnos=alumnos_disponibles
    )


@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar():

    if request.method == "GET":
        id = request.args.get("id")
        curso = Curso.query.get_or_404(id)
        return render_template("cursos/eliminar.html", curso=curso)

    if request.method == "POST":
        id = request.form.get("id")
        curso = Curso.query.get_or_404(id)
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for("cursos.index"))


@cursos.route("/cursos/modificar", methods=["GET", "POST"])
def modificar_curso():

    id = request.args.get("id")

    if not id:
        return redirect(url_for("cursos.index"))

    curso = Curso.query.get_or_404(id)

    create_form = form.CursoForm(request.form)
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos}") for m in Maestros.query.all()
    ]

    if request.method == "GET":
        create_form.nombre.data = curso.nombre
        create_form.maestro_id.data = curso.maestro_id
        return render_template("cursos/modificar.html", form=create_form, curso=curso)

    if request.method == "POST" and create_form.validate():
        curso.nombre = create_form.nombre.data
        curso.maestro_id = create_form.maestro_id.data
        db.session.commit()
        return redirect(url_for("cursos.index"))
