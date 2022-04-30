'''
**************************how the decorator work*****************************************
As we see below, python is explaination language, so it excute line by line:

1st run into @call_counter and pass the "succ" and "mul1" func into "call_counter" as parameters.
2nd then run to the line where the "succ" or "mul1" be called.
3rd if excute "succ" or "mul1" (here call this "succ.calls") then
     first pass "x" into "helper and then excute "helper" func
4th return "helper" func and excute "succ"'s or "mul1"'s and return
*****************************************************************************************
'''

def call_counter(func):
    # count times of call func, use attr "calls" denote the call times.
    print('**************init decorator********************')
    print(f'in \"call_counter\", {func.__name__=}, outer func only used for initiallization')
    def helper(*args, **kwargs):
        print(f'in \"helper\", and {helper.calls= }, {helper.__dict__= }')
        helper.calls += 1
        print(f'after \"helper.calls += 1\", and {helper.calls= }, {helper.__dict__= }')
        print(f'{args=}, {kwargs=}', '*args=',*args)
        return func(*args, **kwargs)+1000# helper return val is the final func("succ", "mul1") return val
    helper.calls = 0
    print(f'After \"helper\", and {helper.__dict__=}')
    print('************************************************')
    return helper
print(f'before \"succ\" func')

@call_counter
def succ(x):
    print(f'here succ attr \"calls\" inheirate from helper')
    print(f'in \"succ\", input {x= }, {succ.calls= }, {succ.__dict__= }')
    return x * 2
print(f'before \"mul1\" func')
@call_counter
def mul1(x, y=1):
    print(f'in \"mul1\", input x, y = {x, y}, {mul1.calls= }, {mul1.__dict__= }')
    return x*y + 1

print(f'initial {succ.calls=}')
print(f'%%%%%%%%%%%%%%%%%loop%%%%%%%%%%%%%%%%%%%%')
for i in range(5):
    print(succ.__dict__)
    res_succ = succ(i)
    print(f'{res_succ= }, which is helper func return')
print(f'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
mul1(3, 4)
mul1(4)
res_mul1=mul1(y=3, x=2)
print(f'{res_mul1= }, which is helper func return')

print(f'final {succ.calls= }')
print(f'final {mul1.calls= }')