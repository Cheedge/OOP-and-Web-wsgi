
"""
Basic version: 0.8 (with min_oop_wsgi_server_v08.py)
TODO:
    1. route
DONE:
    1. invoke Server 'set_request_head' to make HEAD,
        and construct BODY then send BODY to Server
    2. application func
    3. in set_response_head use 'environ' dict to recv
        func_name
    4. diff apps:
        + produce diff html code
    5. use dict instead of application if sentence
"""

URL_DICT = dict()

# decorator with params
def router(url):
    def out_func(func):
        URL_DICT[url] = func
        def in_func(*ars, **kwargs):
            print('inside will never be called...')
            return func(*ars, **kwargs)
        return in_func
    return out_func


def login():
    return "please login"


def register():
    return "please register"


@router('/index.py')
def index():
    with open('./templates/index.html', 'rb') as f:
        content = f.read()
    return content.decode()


@router('/home.py')
def home():
    with open('./templates/home.html', 'rb') as f:
        content = f.read()
    return content.decode()


# URL_DICT = {
#     '/index.py': index,
#     '/home.py': home
# }


def application(environ: dict, set_request_head):
    func_name = environ['Request_Path']
    """
    NOTIC: WSGI invoke Server 'set_request_head' func
        not return HEAD directly.
    """
    set_request_head('200 OK', [{'Content-Type': 'text/html; charset=utf-8'},])

    # request_head = set_request_head(environ)
    # if func_name=='/login.py':
    #     request_body = login()
    # elif func_name=='/register.py':
    #     request_body = register()
    # elif func_name=='/index.py':
    #     request_body = index()
    # elif func_name=='/home.py':
    #     request_body = home()
    # else:
    #     request_body = 'there is no .py file are found......'
    # print(f'{URL_DICT=}')
    try:
        request_func = URL_DICT[func_name]
        request_body = request_func()

        return request_body
    except Exception as e:
        return f'there is no corresponding file, error:{e}'
