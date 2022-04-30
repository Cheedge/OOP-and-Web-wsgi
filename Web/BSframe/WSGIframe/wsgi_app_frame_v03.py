
"""
Basic version: 0.3 (with min_oop_wsgi_server_v03.py)
TODO:
    1. in set_response_head use 'environ' dict to recv
        func_name
    2. diff apps
    3. application func
    Advanced version:
        * route
DONE:
    1. invoke Server 'set_request_head' to make HEAD,
        and construct BODY then send BODY to Server
"""
def login():
    return "please login"

def register():
    return "please register"

def application(environ: dict, set_request_head):
    func_name = environ['Request_Path']
    if func_name=='/login.py':
        request_body = login()
    elif func_name=='/register.py':
        request_body = register()
    else:
        request_body = 'there is no .py file are found......'
    """
    NOTIC: WSGI invoke Server 'set_request_head' func
        not return HEAD directly.
    """
    set_request_head('200 OK', [{'Content-Type': 'text/html; charset=utf-8'},])
    # request_head = set_request_head(environ)
    return request_body
