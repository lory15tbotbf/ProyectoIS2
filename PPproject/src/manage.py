from flask.ext.script import Manager
from pruebita import app, db


import models

manager = Manager(app)

""" Administra la Base de Datos """
@manager.command
def initdb():
    """ Inicializar base de datos """
    db.create_all()
    createAdministrador()
    createUser()
    createPermiso()
    createRol()


@manager.command
def createAdministrador():
    """ crea el usuario Admin """ 
    from models import User
    u=User("admin","admin","administrador","administrador","admin@gmail.com",1234,"usuario administrador")
    db.session.add(u)
    db.session.commit()
 
@manager.command
def createUser():
    """ crea usuarios """ 
    from models import User
    u1=User("stfy","stfy","estefanis","zamora","stfy@gmail.com",1111,"usuario nuevo")
    db.session.add(u1)
    db.session.commit()
    u2=User("vavi","vavi","victor","vera","vavi@gmail.com",2222,"usuario nuevo")
    db.session.add(u2)
    db.session.commit()
    u3=User("lory","lory","lorelay","ortiz","lory@gmail.com",3333,"usuario nuevo")
    db.session.add(u3)
    db.session.commit()
    u4=User("guille","guille","guillermo","gonzalez","guille@gmail.com",4444,"usuario nuevo")
    db.session.add(u4)
    db.session.commit()
    
@manager.command
def createRol():
    """ 
    Crea Roles de Sistema Pre establecidos 
    1. Administrador: -> Permite el acceso al Modulo de Administracion
        - administra usuarios
        - crea proyecto
        - elimina proyecto
        - asigna lider a proyecto
        - administra tipo de atributo
    2. Desarrollador: -> Permite el acceso al Modulo de Desarrollo
        - administra item
        - administra reportes
    3. Lider de Proyecto: -> Permite el acceso al Modulo de Gestion de Cambio
        - administra proyecto
        - administra fase
        - administra tipo de item
        - administra roles 
        - administra LB
        - calculo de costo
        - calculo de impacto
    """
    from models import Rol
    r1=Rol("Administrador","permite el acceso al modulo de administracion","all project")
    db.session.add(r1)
    db.session.commit()
    r2=Rol("Desarrollador","permite el acceso al modulo de desarrollo","all project")
    db.session.add(r2)
    db.session.commit()
    r3=Rol("LiderDeProyecto","permite el acceso al modulo de gestion","all project")
    db.session.add(r3)
    db.session.commit()
   
@manager.command
def createPermiso():
    """
    Crea Permisos Predefinidos a nivel de:
    - sistema
    - proyecto
    - fase
    - item
    """
    from models import Permiso
    # Los permisos a Nivel de Sistema son
    p=Permiso("CrearProyecto","Permite crear un proyecto en el sistema")
    db.session.add(p)
    db.session.commit()
    p=Permiso("CrearUsuario","Permite crear un usuario dentro de un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("CambiarEstadoUsuario","Permite cambiar el estado de un usuario dentro del proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarTipoDeAtributo","Permite administrar un tipo de atributo")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Proyecto son
    p=Permiso("CrearRol","Permite crear un rol en el sistema")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AsignarRolAUsuario","Permite asignar Rol a Usuario")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarFase","Permite administrar fase en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("ConsultaProyecto","Permite realizar consultas en un proyecto")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Fase son
    p=Permiso("AdministrarLineaBase","Permite administrar linea base en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarTiposDeItem","Permite administrar tipos de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    # Los Permisos a Nivel de Item son
    p=Permiso("AdministrarItem","Permite administrar item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AdministrarCambio","Permite administrar cambio en un item de un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("AprobacionItem","Permite administrar la aprobacion de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("DesaprobacionItem","Permite administrar la desaprobacion de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    p=Permiso("ConsultaItem","Permite consulta de item en un proyecto")
    db.session.add(p)
    db.session.commit()
    
@manager.command
def dropdb():
    """Elimino la base de datos."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()

