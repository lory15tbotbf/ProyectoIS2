from pruebita import db, app

class MgrRol():

    def guardar(self, rol):
        """ guarda un registro rol """
        db.session.add(rol)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro project x name"""
        from models import Rol
        rol = Rol.query.filter(Rol.nombre == nombre).first_or_404()
        db.session.delete(rol)
        db.session.commit()


