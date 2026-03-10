import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    # Relación muchos cursos pueden pertenecer a un Maestro
    maestro_id = db.Column(db.Integer, db.ForeignKey("maestros.matricula"), nullable=False)
    maestro = db.relationship("Maestros", back_populates="cursos")

    # Relación muchos a muchos con Alumno
    alumnos = db.relationship(
        "Alumnos", secondary="inscripciones", back_populates="cursos"
    )


class Alumnos(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(200))
    email = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    cursos = db.relationship(
        "Curso", secondary="inscripciones", back_populates="alumnos"
    )


class Maestros(db.Model):
    __tablename__ = "maestros"
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(200))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
    cursos = db.relationship("Curso", back_populates="maestro")


class Inscripcion(db.Model):
    __tablename__ = "inscripciones"

    alumno_id = db.Column(db.Integer, db.ForeignKey("alumnos.id"), primary_key=True)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint("alumno_id", "curso_id", name="unique_inscripcion"),
    )
