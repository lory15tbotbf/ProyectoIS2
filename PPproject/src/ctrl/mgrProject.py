from pruebita import db, app

class MgrProject():

    def guardar(self, project):
        """ guarda un registro project """
        db.session.add(project)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro project x name"""
        from models import Proyecto
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        db.session.delete(project)
        db.session.commit()
    
    def modificar(self, nombre, nombreNew, descripcionNew):
        """ modificar un registro project x name"""
        from models import Proyecto
        project = Proyecto.query.filter(Proyecto.nombre == nombre).first_or_404()
        project.nombre = nombreNew
        project.descripcion = descripcionNew
        db.session.commit()
