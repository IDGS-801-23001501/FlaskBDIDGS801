import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Alumnos(db.Model):
    __tablename__ = "alumnos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(200))
    email = db.Column(db.String(50))
    telefono = db.Column(db.String(20))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Meestros(db.Model):
    __tablename__ = "meestros"
    matricula = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(200))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))
