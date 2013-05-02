from pruebita import db, app

class MgrUser():

    def guardar(self, usuario):
        """ guarda un registro usuario """
        db.session.add(usuario)
        db.session.commit()
    
    def borrar(self,nombre):
        """ borra un registro usuario x name"""
        from models import User
        user = User.query.filter(User.name == nombre).first_or_404()
        db.session.delete(user)
        db.session.commit()
    
         
    