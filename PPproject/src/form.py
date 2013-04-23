from wtforms import Form, TextField, FileField, PasswordField, \
     validators, IntegerField, SelectField, SubmitField, DateTimeField
#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#

# Ingreso al Sistema

class LoginForm(Form):
    """ Formulario de logueo """
    username = TextField('Nick', [validators.required(), validators.Length(min=1, max=10)])
    password = PasswordField('Password', [validators.required(), validators.Length(min=1, max=15)])


# Administrar Usuarios

class CreateFormUser(Form):
    """ Formulario para crear un usuario"""
    name = TextField('Name', [validators.required(), validators.Length(min=1, max=10)])
    password = PasswordField('Password', [validators.required(), validators.Length(min=1, max=15)])
    confirmacion = PasswordField('Confirmacion', [validators.EqualTo('password')])
    nombre = TextField('Nombre', [validators.required(), validators.Length(min=1, max=45)])
    apellido = TextField('Apellido', [validators.required(), validators.Length(min=1, max=45)])
    email = TextField('Email', [validators.required(), validators.Length(min=1, max=45), validators.Email()])
    telefono = IntegerField('Telefono', [validators.required(), validators.NumberRange(min=None, max=None, message=None)])
    obs = TextField('Obs', [validators.required()])

class ShowFormUser(Form):
    """ Formulario para crear un usuario"""
    name = TextField('Name', [validators.required()])
    password = PasswordField('Password', [validators.required()])
    nombre = TextField('Nombre', [validators.required()])
    apellido = TextField('Apellido', [validators.required()])
    email = TextField('Email', [validators.required()])
    telefono = IntegerField('Telefono', [validators.required()])
    obs = TextField('Obs', [validators.required()])
    estado = TextField('Estado', [validators.required()])

class EditStateForm(Form):
    """ Formulario de modificacion de estado de usuario """
    estado = SelectField("Estado", choices = [
        ("Inactivo", "Inactivo"),
        ("Activo", "Activo")])
    submit = SubmitField("POST")


# Administrar RolXPermiso

class CreateFormRol(Form):
    """ Formulario para crear rol"""
    nombre = TextField('Nombre', [validators.required(), validators.Length(min=1, max=45)])
    ambito = TextField('Ambito', [validators.required(), validators.Length(min=1, max=45)])
    descripcion = TextField('Descripcion', [validators.required(), validators.Length(min=1, max=45)])


# Administrar Proyecto

class CreateFormProject(Form):
    """ Formulario para crear proyecto"""
    nombre = TextField('Nombre', [validators.Length(min=1, max=45)])
    descripcion = TextField('Descripcion', [ validators.Length(min=1, max=150)])
    fechaDeInicio = DateTimeField('FechaDeInicio',[validators.Length(min=1, max=45)])
    fechaDeFin = DateTimeField('FechaDeFin', [validators.Length(min=1, max=45)])
 
# Administrar tipo de atributos

class CreateFormAtrib(Form):
    """ Formulario para crear un atributo"""
    nombre = TextField('Nombre', [validators.required(),validators.Length(min=1, max=45)])
    tipoDeDato = SelectField("Tipo de Dato", choices = [
        ("Numerico", "Numerico"),
        ("Texto", "Texto"),
        ("Booleano", "Booleano"),
        ("Fecha", "Fecha")])
    detalle = IntegerField('Detalle', [validators.required()])
    descripcion = TextField('Descripcion', [validators.required(), validators.Length(min=1, max=150)])
    
class ShowFormAtrib(Form):
    """ Formulario para mostrar un atributo"""
    nombre = TextField('Nombre', [validators.required(),validators.Length(min=1, max=45)])
    tipoDeDato = TextField("Tipo de Dato", [validators.required()])
    detalle = IntegerField('Detalle', [validators.required()])
    descripcion = TextField('Descripcion', [validators.required(),validators.Length(min=1, max=150)])


