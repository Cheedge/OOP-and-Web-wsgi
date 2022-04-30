
"""
Basic version: 0.6 (with min_oop_wsgi_server_v06.py)
    this version is totally same as 0.5 version
TODO:
    Advanced version:
        * route
DONE:
    1. invoke Server 'set_request_head' to make HEAD,
        and construct BODY then send BODY to Server
    2. application func
    3. in set_response_head use 'environ' dict to recv
        func_name
    4. diff apps:
        + produce diff html code
"""

def login():
    return "please login"

def register():
    return "please register"

def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content.decode()

def home():
    with open('./templates/home.html', 'rb') as f:
        content = f.read()
    return content.decode()

def application(environ: dict, set_request_head):
    func_name = environ['Request_Path']
    if func_name=='/login.py':
        request_body = login()
    elif func_name=='/register.py':
        request_body = register()
    elif func_name=='/index.py':
        request_body = index()
    elif func_name=='/home.py':
        request_body = home()
    else:
        request_body = 'there is no .py file are found......'
    """
    NOTIC: WSGI invoke Server 'set_request_head' func
        not return HEAD directly.
    """
    set_request_head('200 OK', [{'Content-Type': 'text/html; charset=utf-8'},])
    # request_head = set_request_head(environ)
    return request_body
