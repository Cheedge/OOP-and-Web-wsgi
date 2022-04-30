
"""
Basic version: 0.10 (with min_oop_wsgi_server_v010.py)

TODO:
    8. add data
        + realize to use diff content in func to substitute
        %content% in html;
        + realize importing databases.

DONE:
    1. invoke Server 'set_request_head' to make HEAD,
        and construct BODY then send BODY to Server
    2. application func
    3. in set_response_head use 'environ' dict to recv
        func_name
    4. diff apps:
        + produce diff html code
    5. use dict instead of application if sentence
    6. route
        + decorator with param and dict
    7. pseudo-static
        change all /***.py to /***.html
    
"""
import re
from pymysql import connect
# import mysql.connector

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


# @router('/index.py')
@router('/index.html')
def index():
    with open('./templates/index.html', 'r') as f:
        content = f.read()
    add_data = 'in INDEX func'
    content = re.sub(r'\{%content%\}', add_data, content)
    return content


# @router('/home.py')
@router('/home.html')
def home():
    with open('./templates/home.html', 'r') as f:
        content = f.read()
    # add_data = 'in HOME func'
    data_conn = connect(
        host='localhost',
        port=3306,
        user='sharma',
        password='666666',
        database='crime',
        )
    data_cur = data_conn.cursor()
    data_cur.execute('SELECT * FROM berlin_crime')
    add_data = data_cur.fetchall()
    data_cur.execute("select column_name from information_schema.columns where table_name='berlin_crime';")
    colnames = data_cur.fetchall()# return a list [(),()...]
    data_cur.close()
    data_conn.close()

    # data_conn = mysql.connector.connect(
    #     host='localhost',
    #     port=3306,
    #     user='sharma',
    #     password='666666',
    #     database='crime',
    #     )
    # data_cur = data_conn.cursor()
    # data_cur.execute('SELECT * FROM berlin_crime')
    # add_data = data_cur.fetchall()
    # data_cur.close()
    # data_conn.close()

    data_html = ""
    col_name = [n[0] for n in colnames]
    col_html=f"""
                <th>{col_name[0]}</th>
                <th>{col_name[1]}</th>
                <th>{col_name[2]}</th>
                <th>{col_name[3]}</th>
                <th>{col_name[4]}</th>
                <th>{col_name[5]}</th>
                <th>{col_name[6]}</th>
                <th>{col_name[7]}</th>
                <th>{col_name[8]}</th>
                <th>{col_name[9]}</th>
                <th>{col_name[10]}</th>
                <th>{col_name[11]}</th>
                <th>{col_name[12]}</th>
                <th>{col_name[13]}</th>
                <th>{col_name[14]}</th>
                <th>{col_name[15]}</th>
                <th>{col_name[16]}</th>
                <th>{col_name[17]}</th>
                <th>{col_name[18]}</th>
                <th>{col_name[19]}</th>
    """
    new_content = re.sub(r'\{%content1%\}', col_html, content)
    for data in add_data:
        tb_template = f"""<tr>
            <td>{data[0]}</td>
            <td>{data[1]}</td>
            <td>{data[2]}</td>
            <td>{data[3]}</td>
            <td>{data[4]}</td>
            <td>{data[5]}</td>
            <td>{data[6]}</td>
            <td>{data[7]}</td>
            <td>{data[8]}</td>
            <td>{data[9]}</td>
            <td>{data[10]}</td>
            <td>{data[11]}</td>
            <td>{data[12]}</td>
            <td>{data[13]}</td>
            <td>{data[14]}</td>
            <td>{data[15]}</td>
            <td>{data[16]}</td>
            <td>{data[17]}</td>
            <td>{data[18]}</td>
            <td>{data[19]}</td>
        </tr>
        """
        data_html += tb_template


    # content = re.sub(r'\{%content%\}', str(add_data), content)
    new_content = re.sub(r'\{%content%\}', data_html, new_content)
    return new_content


def application(environ: dict, set_request_head):
    func_name = environ['Request_Path']
    """
    NOTIC: WSGI invoke Server 'set_request_head' func
        not return HEAD directly.
    """
    set_request_head('200 OK', [{'Content-Type': 'text/html; charset=utf-8'},])

    try:
        request_func = URL_DICT[func_name]
        request_body = request_func()

        return request_body
    except Exception as e:
        return f'there is no corresponding file, error: {e}'
