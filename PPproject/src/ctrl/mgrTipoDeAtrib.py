from pruebita import db, app

class MgrTipoDeAtrib():

    def guardar(self, tipoDeAtributo):
        """ guarda un registro tipoDeAtributo """
        db.session.add(tipoDeAtributo)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro tipoDeAtributo x name"""
        from models import TipoDeAtributo
        tipoDeAtributo = TipoDeAtributo.query.filter(TipoDeAtributo.nombre == nombre).first_or_404()
        db.session.delete(tipoDeAtributo)
        db.session.commit()

