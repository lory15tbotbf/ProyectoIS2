import os
from datetime import datetime
from pruebita import db

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
    fechaDeCreacion = db.Column(db.DateTime, default = datetime.now())
    fechaDeInicio = db.Column(db.DateTime)
    fechaDeFin = db.Column(db.DateTime)
    estado = db.Column(db.String(20), default ='Pendiente')
    
    def __init__(self, nombre=None, descripcion=None):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        
    def __init__(self, nombre=None, descripcion=None, fechaDeInicio=None, fechaDeFin=None):
        """ constructor de Proyecto """
        self.nombre = nombre
        self.descripcion = descripcion
        date = datetime.strptime(fechaDeInicio, '%Y-%m-%d %I:%M:%S')
        self.fechaDeInicio = date
        date = datetime.strptime(fechaDeFin, '%Y-%m-%d %I:%M:%S')
        self.fechaDeFin = date
    

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



