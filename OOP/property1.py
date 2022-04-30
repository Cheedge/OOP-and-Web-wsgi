import re

class B(object):
    def __init__(self, name: str) -> None:
        print(f'\"__init__\"')
        self.__sname = name
        self._fname = name

    @property
    def _fname(self) -> str:
        return self.__name

    @property
    def _surname(self) -> str:
        return self.__sname
    
    @_fname.setter
    def _fname(self, name: str) -> str:
        self.__name = "hello " + name
        print(f'\"fname setter\", {self._fname}')
        # return self.__name
    
    @_surname.setter
    def _surname(self, name) -> str:
        self.__sname = 'Morgen ' + name
        print(f'into \"surname setter\"')
        # return 'Morgen' + name

    @property
    def is_bro(self) -> bool:
        if re.search(r'hua', self._fname):
            return True
        else:
            return False

class_b = B('linda')
print(f'class B fname is \"{class_b._fname}\" and -----is bro is {class_b.is_bro}')
print(f'reset _fname')
class_b._fname = 'huahua'
print(f'class B fname is \"{class_b._fname}\" and -----is bro is {class_b.is_bro}')
class_b._surname = 'Joe'
print(f'class B surname is \"{class_b._surname}\"')