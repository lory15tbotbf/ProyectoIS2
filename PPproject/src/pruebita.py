
#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash, escape, request
from werkzeug.routing import Rule
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature
from flaskext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, FileField, PasswordField, \
     validators, IntegerField, SelectField, SubmitField, DateTimeField
import unittest
#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.secret_key = 'A0Zr234j234yXR~XasdN]LWRT'
#app.session_interface = ItsdangerousSessionInterface()
app.config.from_object('config')
db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# MIDDLEWARE (to serve static files)
#------------------------------------------------------------------------------#
# Middleware to serve the static files
from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})


#------------------------------------------------------------------------------#
# MODELS
#------------------------------------------------------------------------------#

class User(db.Model):
    """ Modelo de Usuario """
    __tablename__ = 'User'

    idUser = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    passwd = db.Column(db.String(15))
    nombre = db.Column(db.String(45))
    apellido = db.Column(db.String(45))
    email = db.Column(db.String(45))
    telefono = db.Column(db.Integer)
    obs = db.Column(db.String(100))
    estado = db.Column(db.String(20), default ='Inactivo')
    
    # un usuario tiene 0 a n roles
    roles = db.relationship("UserXRol")
    
    

    def __init__(self, name=None, passwd=None):
        """ constructor de user """
        self.name = name
        self.passwd = passwd
    
    def __init__(self,name=None, passwd=None, nombre=None, apellido=None, email=None, telefono=None, obs=None):
        """ constructor de user """
        self.name = name
        self.passwd = passwd
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.obs = obs
           


class Rol(db.Model):
    """ Modelo de Rol """
    __tablename__ = 'Rol'
    
    idRol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True)
    ambito = db.Column(db.String(45))
    descripcion = db.Column(db.String(100))
    
    # un rol tiene 0 a n permisos
    permisos = db.relationship("RolXPermiso")

    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Rol """
        self.nombre = nombre
        self.descripcion = descripcion
    
    
    def __init__(self, nombre=None, descripcion=None, ambito=None,):
        """ constructor de Rol """
        self.nombre = nombre
        self.ambito = ambito
        self.descripcion = descripcion
        

class Permiso(db.Model):
    """ Modelo de Permiso """
    __tablename__ = 'Permiso'
    
    idPermiso = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True)
    descripcion = db.Column(db.String(100))
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Permiso """
        self.nombre = nombre
        self.descripcion = descripcion
    

class Proyecto(db.Model):
    """ Modelo de Proyecto """
    __tablename__ = 'Proyecto'
    
    idProyecto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True)
    descripcion = db.Column(db.String(150))
    fechaDeCreacion = db.Column(db.DateTime)
    fechaDeInicio = db.Column(db.DateTime)
    fechaDeFin = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default ='Pendiente')
    
    def __init__(self, nombre=None, descripcion=None, fechaDeCreacion=None):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaDeCreacion = fechaDeCreacion
        
    def __init__(self, nombre=None, descripcion=None, fechaDeCreacion=None, fechaDeInicio=None, fechaDeFin=None):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaDeCreacion = fechaDeCreacion
        self.fechaDeInicio = fechaDeInicio
        self.fechaDeFin = fechaDeFin
    

class TipoDeAtributo(db.Model):
    """ Modelo de Tipo de Atributo """
    __tablename__ = 'TipoDeAtributo'
    
    idTipoDeAtributo = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), unique=True)
    tipoDeDato = db.Column(db.String(20)) # numerico, texto, fecha, boolean
    detalle = db.Column(db.Integer) # si tipoDeDato es numerico, corresponde a la presicion, si tipoDeDato es texto, corresponde a la cantidad de caracteres  
    descripcion = db.Column(db.String(150))
    
    
    def __init__(self, nombre=None, tipoDeDato=None, detalle=None, descripcion=None):
        """ constructor de Tipo de Atributo"""
        self.nombre = nombre
        self.tipoDeDato = tipoDeDato
        self.detalle = detalle
        self.descripcion = descripcion
    

class UserXRol(db.Model):
    """ Modelo Usuario por Rol """
    __tablename__ = 'UserXRol'
    idUserXRol = db.Column(db.Integer, primary_key=True)
    idUser = db.Column(db.Integer, db.ForeignKey('User.idUser'), primary_key=True)
    idRol = db.Column(db.Integer, db.ForeignKey('Rol.idRol'), primary_key=True)
    
    rol = db.relationship("Rol")
    
    def __init__(self, idUser=None, idRol=None):
        """ constructor de la Asociacion Usuario por Rol"""
        self.idUser = idUser
        self.idRol = idRol
  

class RolXPermiso(db.Model):
    """ Modelo Rol por Permiso """
    __tablename__ = 'RolXPermiso'
    idRolXPermiso = db.Column(db.Integer, primary_key=True)
    idRol = db.Column(db.Integer, db.ForeignKey('Rol.idRol'), primary_key=True)
    idPermiso = db.Column(db.Integer, db.ForeignKey('Permiso.idPermiso'), primary_key=True)
    
    permiso = db.relationship("Permiso")
    
    def __init__(self, idRol=None, idPermiso=None):
        """ constructor de la Asociacion Rol por Permiso """
        self.idRol = idRol
        self.idPermiso = idPermiso

class ItsdangerousSession(CallbackDict, SessionMixin):
 
    def __init__(self, initial=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = False
 
 
class ItsdangerousSessionInterface(SessionInterface):
    salt = 'cookie-session'
    session_class = ItsdangerousSession
 
    def get_serializer(self, app):
        if not app.secret_key:
            return None
        return URLSafeTimedSerializer(app.secret_key,
                                      salt=self.salt)
 
    def open_session(self, app, request):
        s = self.get_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = app.permanent_session_lifetime.total_seconds()
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()
 
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                   domain=domain)
            return
        expires = self.get_expiration_time(app, session)
        val = self.get_serializer(app).dumps(dict(session))
        response.set_cookie(app.session_cookie_name, val,
                            expires=expires, httponly=True,
                            domain=domain)
        
#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#

class CreateFormUser(Form):
    """ Formulario para crear un usuario"""
    name = TextField('Name', [validators.required()])
    password = PasswordField('Password', [validators.required()])
    nombre = TextField('Nombre', [validators.required()])
    apellido = TextField('Apellido', [validators.required()])
    email = TextField('Email', [validators.required()])
    telefono = IntegerField('Telefono', [validators.required()])
    obs = TextField('Obs', [validators.required()])
    estado = TextField('Estado', [validators.required()])

class CreateFormProject(Form):
    """ Formulario para crear proyecto"""
    nombre = TextField('Nombre', [validators.required()])
    descripcion = TextField('Descripcion', [validators.required()])
    fechaDeCreacion = DateTimeField('FechaDeCreacion', format='%d-%m-%Y %H:%M:%S')
    fechaDeInicio = DateTimeField('FechaDeInicio', format='%d-%m-%Y %H:%M:%S')
    fechaDeFin = DateTimeField('FechaDeFin', format='%d-%m-%Y %H:%M:%S')
    
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

   
class LoginForm(Form):
    """ Formulario de logueo """
    username = TextField('Nick', [validators.required()])
    password = PasswordField('Password', [validators.required()])


class EditStateForm(Form):
    """ Formulario de modificacion de estado de usuario """
    estado = SelectField("Estado", choices = [
        ("Inactivo", "Inactivo"),
        ("Activo", "Activo")])
    submit = SubmitField("POST")
    
#------------------------------------------------------------------------------#
# CONTROLLERS
#------------------------------------------------------------------------------#

@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@app.route('/')
def index():
    return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    users = User.query.order_by(User.name.desc()).all(),)
                            

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Nick o Password incorrecto.'
            else:
                print u.idUser
                session['logged_in'] = True
                session['user_id'] = u.idUser
                session['user_name'] = u.name
                flash('Usted se ha conectado')
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        session["__invalidate__"] = True
        flash('Usted se ha desconectado')
    return redirect(url_for('index'))


@app.route('/rolPermiso', methods=['GET','POST'])
def rolPermiso():
     return render_template(app.config['DEFAULT_TPL']+'/rolPermiso.html',
			    conf = app.config,)

#  Modulo del Sistema

@app.route('/administracion', methods=['GET','POST'])
def administracion():
    """ Modulo Administracion """
    return render_template(app.config['DEFAULT_TPL']+'/administracion.html',
			    conf = app.config,)
                                             

@app.route('/gestion', methods=['GET','POST'])
def gestion():
    """ Modulo Gestion """
    return render_template(app.config['DEFAULT_TPL']+'/gestion.html',
			    conf = app.config,)


# Administracion de Usuario

@app.route('/addUser', methods=['GET','POST'])
def addUser():
    if request.method == 'POST':
		user = User(name = request.form['name'], passwd = request.form['password'],
                nombre = request.form['nombre'], apellido = request.form['apellido'],
                email = request.form['email'], telefono = request.form['telefono'], 
                obs = request.form['obs'])    
		db.session.add(user)
		db.session.commit()
                flash('Se ha creado correctamente el usuario')
		return redirect(url_for('listEdit'))
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
			       conf = app.config,
			       form = CreateFormUser())


@app.route('/deleteUser/<path:nombre>.html')
def deleteUser(nombre):
        """ Elimina un usuario """
        user = User.query.filter(User.name == nombre).first_or_404()
        db.session.delete(user)
        db.session.commit()
        flash('Se ha borrado correctamente')
        return redirect(url_for('listEdit'))
                             

@app.route('/edit/<path:nombre>.html', methods=['GET','POST'])
def editState(nombre):
    """ Modifica el estado de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = User.query.filter(User.name == nombre).first_or_404()
        form = EditStateForm(request.form, estado = user.estado)
	if request.method == 'POST' and form.validate():
                user.estado = request.form['estado']
                db.session.commit()
		return redirect(url_for('listEdit'))
	return render_template(app.config['DEFAULT_TPL']+'/editState.html',
			       conf = app.config,
			       form = EditStateForm())


@app.route('/listEdit')
def listEdit():
    """ Lista todos los usuarios usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listEdit.html',
                           conf = app.config,
                           list = User.query.all(),) 


@app.route('/editUser/<path:nombre>.html', methods=['GET','POST'])
def editUser(nombre):
    """ Modifica los datos de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = User.query.filter(User.name == nombre).first_or_404()
        form = CreateFormUser(request.form, name = user.name, 
               password = user.passwd, nombre = user.nombre,
               apellido = user.apellido, email = user.email,
               telefono = user.telefono, obs = user.obs)
	if request.method == 'POST' and form.validate():
            user.name = request.form['name']
            user.passwd = request.form['password']
            user.nombre = request.form['nombre'] 
            user.apellido = request.form['apellido']
            user.email = request.form['email']
            user.telefono = request.form['telefono'] 
            user.obs = request.form['obs']
            db.session.commit()
            flash('Se ha modificado correctamente el usuario')
            return redirect(url_for('listEdit'))
    return render_template(app.config['DEFAULT_TPL']+'/editUser.html',
			       conf = app.config,
			       form = form)
                               

@app.route('/showUser/<path:nombre>.html', methods=['GET','POST'])
def showUser(nombre):
    """ Muestra los datos de un usuario """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        user = User.query.filter(User.name == nombre).first_or_404()
        form = CreateFormUser(request.form, name = user.name, 
               password = user.passwd, nombre = user.nombre,
               apellido = user.apellido, email = user.email,
               telefono = user.telefono, obs = user.obs,
               estado = user.estado)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Usuario":
                return redirect(url_for('editUser', nombre = user.name))
            elif request.form.get('delete', None) == "Eliminar Usuario":
                return redirect(url_for('deleteUser', nombre = user.name))
            elif request.form.get('state', None) == "Modificar Estado de Usuario":
                return redirect(url_for('editState', nombre = user.name))
	return render_template(app.config['DEFAULT_TPL']+'/showUser.html',
			       conf = app.config,
			       form = form)



# ADMINISTRAR PROYECTO

@app.route('/listEditProject')
def listEditProject():
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listEditProject.html',
                           conf = app.config,
                           list = Proyecto.query.all(),) 


@app.route('/showProject/<path:nombre>.html', methods=['GET','POST'])
def showProject(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        form = CreateFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, fechaDeCreacion = project.fechaDeCreacion,
                fechaDeInicio = project.fechaDeInicio, fechaDeFin = project.fechaDeFin)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Proyecto":
                return redirect(url_for('editProject', nombre = project.name))
            elif request.form.get('delete', None) == "Eliminar Proyecto":
                return redirect(url_for('deleteProject', nombre = project.name))
            
	return render_template(app.config['DEFAULT_TPL']+'/showProject.html',
			       conf = app.config,
			       form = form)


@app.route('/editProject/<path:nombre>.html', methods=['GET','POST'])
def editProject(nombre):
    if g.user is None:
        return redirect(url_for('login'))
    else:
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        form = CreateFormProject(request.form, nombre = project.nombre,
               descripcion = project.descripcion, fechaDeCreacion = project.fechaDeCreacion,
                fechaDeInicio = project.fechaDeInicio, fechaDeFin = project.fechaDeFin)
	if request.method == 'POST' and form.validate:
            project.nombre = request.form['nombre'] 
            project.descripcion = request.form['descripcion']
            project.fechaDeCreacion = request.form['fechaDeCreacion']
            project.fechaDeInicio = request.form['fechaDeInicio']
            project.fechaDeFin = request.form['fechaDeFin']
            db.session.commit()
            flash('Se ha modificado correctamente el proyecto')
            return redirect(url_for('listEditProject'))
    return render_template(app.config['DEFAULT_TPL']+'/editProject.html',
			       conf = app.config,
			       form = form)


@app.route('/deleteProject/<path:nombre>.html')
def deleteProject(nombre):
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        db.session.delete(project)
        db.session.commit()
        flash('Se ha borrado correctamente')
        return redirect(url_for('listEditProject'))
                             

@app.route('/addProject', methods=['GET','POST'])
def addProject():
    if request.method == 'POST':
        project = Proyecto(nombre = request.form['nombre'], descripcion = request.form['descripcion'],
        fechaDeCreacion = request.form['fechaDeCreacion'], fechaDeInicio = request.form['fechaDeInicio'], 
        fechaDeFin = request.form['fechaDeFin'])    
        db.session.add(project)
        db.session.commit()
        flash('Se ha creado correctamente el proyecto')
        return redirect(url_for('listEditProject'))
    return render_template(app.config['DEFAULT_TPL']+'/formProject.html',
			       conf = app.config,
			       form = CreateFormProject())

@app.route('/listAtrib')
def listAtrib():
    """ Lista todos los tipos de atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        return render_template(app.config['DEFAULT_TPL']+'/listAtrib.html',
                           conf = app.config,
                           list = TipoDeAtributo.query.all(),) 
                           
@app.route('/addAtrib', methods=['GET','POST'])
def addAtrib():
    """ Agrega un nuevo tipo de atributo """
    if request.method == 'POST':
        form = CreateFormAtrib(request.form, nombre = request.form['nombre'], 
                tipoDeDato = request.form['tipoDeDato'], 
                detalle = request.form['detalle'], 
                descripcion = request.form['descripcion']) 
        if form.validate():
                atrib = TipoDeAtributo(nombre = request.form['nombre'], tipoDeDato = request.form['tipoDeDato'],
                detalle = request.form['detalle'], descripcion = request.form['descripcion'])    
                db.session.add(atrib)
		db.session.commit()
                flash('Se ha creado correctamente el atributo')
		return redirect(url_for('listAtrib'))
        else:
                return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
			       conf = app.config,
			       form = form)
    return render_template(app.config['DEFAULT_TPL']+'/addAtrib.html',
			       conf = app.config,
			       form = CreateFormAtrib())
                               
@app.route('/showAtrib/<path:nombre>.html', methods=['GET','POST'])
def showAtrib(nombre):
    """ Muestra los datos de un atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        form = ShowFormAtrib(request.form, nombre = atrib.nombre,
               tipoDeDato = atrib.tipoDeDato, detalle = atrib.detalle, 
               descripcion = atrib.descripcion)
        if request.method == 'POST':
            if request.form.get('edit', None) == "Modificar Atributo":
                return redirect(url_for('editAtrib', nombre = atrib.nombre))
            elif request.form.get('delete', None) == "Eliminar Atributo":
                return redirect(url_for('deleteAtrib', nombre = atrib.nombre))
	return render_template(app.config['DEFAULT_TPL']+'/showAtrib.html',
			       conf = app.config,
			       form = form)
                               
@app.route('/editAtrib/<path:nombre>.html', methods=['GET','POST'])
def editAtrib(nombre):
    """ Modifica los datos de un atributo """
    if g.user is None:
        return redirect(url_for('login'))
    else:
        atrib = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        form = CreateFormAtrib(request.form, nombre = atrib.nombre,
               tipoDeDato = atrib.tipoDeDato, detalle = atrib.detalle, 
               descripcion = atrib.descripcion)
	if request.method == 'POST' and form.validate():
            atrib.nombre = request.form['nombre'] 
            atrib.tipoDeDato = request.form['tipoDeDato']
            atrib.detalle = request.form['detalle'] 
            atrib.descripcion = request.form['descripcion']
            db.session.commit()
            flash('Se ha modificado correctamente el atributo')
            return redirect(url_for('listAtrib'))
    return render_template(app.config['DEFAULT_TPL']+'/editAtrib.html',
			       conf = app.config,
			       form = form)
                               

#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    #app.session_interface = ItsdangerousSessionInterface()
    app.run()
    
    



