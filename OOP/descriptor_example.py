class Property:
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

class A(object):

    def __init__(self, prop):
        self.prop = prop
    
    @Property
    def prop(self):
        print("The Property 'prop' will be returned now:")
        return self.__prop
    
    @prop.setter
    def prop(self, prop):
        print("prop will be set")
        self.__prop = prop


print("Initializing the Property 'prop' with the value 'Python'")
x = A("Python")
print("The value is: ", x.prop)
print("Reassigning the Property 'prop' to 'Python descriptors'")
x.prop = "Python descriptors"
print("The value is: ", x.prop)

