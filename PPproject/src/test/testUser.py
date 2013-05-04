# To change this template, choose Tools | Templates
# and open the template in the editor.

import unittest


class  TestUserCase(unittest.TestCase):
    #def setUp(self):
    #    self.foo = New_()
    #

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def testUserGuardar(self):
        from models import User
        from ctrl.mgrUser import MgrUser
        name = "admin2"
        u =User("admin2","admin2","administrador","administrador","admin@gmail.com",1234,"usuario administrador")
        #MgrUser().guardar(u)
        #assert name == u.name
        #MgrUser().guardar(u)
        #assert name == u.name
        u=User("","","","",0,"")
        MgrUser().guardar(u)
        assert name == u.name



if __name__ == '__main__':
    unittest.main()

