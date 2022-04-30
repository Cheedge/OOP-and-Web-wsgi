
"""
Basic version: 0.1 (with min_oop_wsgi_server_v01.py)
TODO:
    1. dynamic source (apps)
    2. frame:
        + get response HEAD and BODY
            and assemble then send to 
            Server
        + diff apps
        + application func
        Advanced version:
            * route
"""
def login():
    return "please login"

def register():
    return "please register"

def application(func_name):
    if func_name=='/login.py':
        return login()
    elif func_name=='/register.py':
        return register()
    else:
        return 'no py file found!'
