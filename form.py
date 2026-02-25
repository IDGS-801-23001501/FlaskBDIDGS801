from wtforms import EmailField
from wtforms import Form
from wtforms import IntegerField, StringField
from wtforms import validators


class UserForm(Form):
    matricula = IntegerField(
        "Matricula",
        [
            validators.number_range(min=100, max=1000, message="Ingrese valor valido"),
        ],
    )
    nombre = StringField(
        "Ingrese su nombre",
        [
            validators.DataRequired(message="El nombre es requerido"),
            validators.length(min=4, max=20, message="Requiere min=4 max=20"),
        ],
    )
    apellidos = StringField(
        "Ingrese sus apellidos",
        [
            validators.DataRequired(message="Los apellidos son requeridos"),
            validators.length(min=4, max=20, message="Requiere min=4 max=20"),
        ],
    )

    correo = EmailField(
        "Ingrese su correo",
        [
            validators.DataRequired(message="El correo es requerido"),
            validators.Email(message="Ingresa correo valido"),
        ],
    )

    telefono = StringField(
        "Ingrese su telefono",
        [
            validators.DataRequired(message="El telefono es requerido"),
            validators.length(min=4, max=20, message="Requiere min=4 max=20"),
        ],
    )
