from wtforms import EmailField
from wtforms import Form
from wtforms import IntegerField, StringField
from wtforms import validators


class UserForm(Form):
    matricula = IntegerField(
        "id",
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
    apaterno = StringField(
        "Ingrese su apellido",
        [
            validators.DataRequired(message="El apellido es requerido"),
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
