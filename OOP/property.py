'''
********************************************* @property & @f.setter *****************************
@property means get attributes from class.__init__ which is same as get func
@f.setter means set attributes val to class.__int__ which is same as set func
and property used to: make a func --> an attribute,
so getter func and setter func name should be all same.
attributor name can be different (meaning see below)
excute order:
setter -> __inti__ -> property
Notice:
if a func is decorated by @property and @f.setter means it can be reset
but if only with @property means the func can be used as attribute but cannot reset. 
*************************************************************************************************
'''
import re

class A(object):
    def __init__(self, name: str) -> None:
        self.set(name)

    def get(self):
        return self.__name
    
    def set(self, name: str):
        self.__name = 'In class A, ' + name

class_A = A("Joe")
print(f'class A name is {class_A.get()}')



class B(object):
    def __init__(self, name: str) -> None:
        self._fname = name
        self._sname = name
        print(f'into __init__ and _fname is {self._fname}, _sname is {self._sname}')
        # pass

    @property
    def _fname(self):
        # print(f'into \"name\" and self.__name is {self.__name} and self.name is {self._fname}')
        return self.__name
    
    @property
    def is_bro(self):
        print(f'into \"is_bro\" and self.__name is {self.__name} and self.name is {self._fname}')
        if re.search(r'li', self.__name):
            return True
        else:
            return False
        # return self.__name == 'In class B, Tom'
    
    @_fname.setter
    def _fname(self, name: str):
        self.__name = 'hallo' + name
        print(f'into setter and self.__name is {self.__name} and self.name is {self._fname}')

class_B = B('linda')
print(f'class B name is {class_B._fname} and -----is bro is {class_B.is_bro}')
class_B._fname = 'cheese'
print(f'class B name is {class_B._fname} and -----is bro is {class_B.is_bro}')

try:
    class_B.is_bro = True
except AttributeError:
    print(f'NOTICE: Cant set attribute, as there is not setter in class')