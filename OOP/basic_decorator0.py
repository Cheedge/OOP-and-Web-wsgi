'''
**************************how the decorator work*****************************************
As we see below, python is explaination language, so it excute line by line:

1st No matter in class or just func, decorator excuted firstly, 
     that is first excute "@decorator" !
     run into class excute @a and pass the "b" func into "a" as parameters.
2nd then run 1st-line begin to run code.
3rd if instance "Dec_cls" class then
     first pass "x" into "helper and then excute "helper" func first
4th return "helper" func and excute "b"'s and return
*****************************************************************************************
'''

class Dec_cls:
    
    def a(func):
        print('**************init decorator********************')
        print(f'in \"a\": the outer func \"a\" only plays in initialization the decorator')
        def helper(self, x):
            print(f'in \"helper\", now x pass into helper, x = {x}')
            return 5 * func(self, x)# helper return val is the final func "b" return val
        print(f'helper.dict = {helper.__dict__}')
        print('************************************************')
        return helper

    # first run decorator outer func
    @a
    def b(self, x):
        print(f'in \"b\", x is in func b, x = {x}')
        return x + 1

print(f'before excute')
ins = Dec_cls()

print(f'HERE {ins.__dict__}')
print('&&&&&&&&&&&&&&&& begin use instance &&&&&&&&&&&&&&&&&&&&&&')
print(f'ins.b(4) = {ins.b(4)}')