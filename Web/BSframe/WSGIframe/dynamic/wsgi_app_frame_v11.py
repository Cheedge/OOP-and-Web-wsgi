
"""
Basic version: 0.11 (with min_oop_wsgi_server_v011.py)

TODO:
    9. add/delete func
        + eg. add/delete new words
    10. realize group func
        + basic: from url eg. /2012.html to find all 2012 data
        + advanced: from Search
    11. advance: 
        + realize plot func
            - use python plot and then return the img to html
        + realize analysis func
            - use python analysis and return results to html

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
    8. add data
        + realize to use diff content in func to substitute
        %content% in html;
        + realize importing databases.
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


"""
here 
"""
@router(r'/add/(\d+)\.html')
def add(rematch):
    # 1. get id
    add_id = rematch.group(1)
    print(add_id)
    # 2. wether it exist (sql)
    conn = connect(
        host='localhost',
        port=3306,
        user='sharma',
        password='666666',
        database='crime',
    )
    sql_cur = conn.cursor()
    """
    in order to avert info injection
    put params to 'cursor.execute(sql, arg)'
    """
    sql = 'select * from berlin_crime where id=%s;'
    sql_cur.execute(sql, add_id)
    if not sql_cur.fetchone():
        sql_cur.close()
        conn.close()
        return f'There is no such item {add_id=}'
    # 3. wether already add
    sql = 'select * from focus where id=%s;'
    sql_cur.execute(sql, add_id)
    if sql_cur.fetchone():
        sql_cur.close()
        conn.close()
        return f'Already add such item {add_id=}'
    # 4. Add item
    sql ="""insert into focus (select * from berlin_crime where id=%s);"""
    sql_cur.execute(sql, add_id)
    conn.commit()
    sql_cur.close()
    conn.close()

    return f'add {add_id} successfully!'


@router(r"/del/(\d+)\.html")
def delete(rematch):
    # 1. get id
    del_id = rematch.group(1)
    # connect to mysql
    conn = connect(
        host='localhost',
        port=3306,
        user='sharma',
        password='666666',
        database='crime',        
    )
    data_cur = conn.cursor()
    # 2. check exist in home
    sql = "select * from berlin_crime where id=%s"
    data_cur.execute(sql, (del_id,))
    if not data_cur.fetchone():
        data_cur.close()
        conn.close()
        return f"{del_id=} not exist in database"
    # 3. check exist in focus
    sql = "select * from focus where id=%s"
    try:
        data_cur.execute(sql, (del_id,))
    except Exception as e:
        data_cur.close()
        conn.close()
        return f"Focus table not exist or {e}"
    else:
        if not data_cur.fetchone():
            data_cur.close()
            conn.close()
            return f"{del_id} not stored in Focus"
    # 4. delete item
    sql = "delete from focus where id=%s"
    data_cur.execute(sql, (del_id,))
    conn.commit()
    data_cur.close()
    conn.close()
    return f"{del_id} delete successfully!"


def group(rematch):
    pass


@router('/myfocus.html')
def myfocus(rematch):
    with open('./templates/myfocus.html', 'r') as f:
        content = f.read()
    # 1. check wether 'focus' table exist, if not create
    conn = connect(
        host='localhost',
        port=3306,
        user='sharma',
        password='666666',
        database='crime',
    )
    data_cur = conn.cursor()
    sql = "select * from focus;"
    try:
        data_cur.execute(sql)
    except Exception:
        create_sql = "create table if not exists focus like berlin_crime"
        data_cur.execute(create_sql)
        return f'table Focus not exist or empty.'
    else:
        add_data = data_cur.fetchall()
        print(add_data)
        sql = """
        select column_name from information_schema.columns where table_name='focus'\
            ORDER BY ORDINAL_POSITION;
        """
        data_cur.execute(sql)
        colnames = data_cur.fetchall()# return a list [(),()...]
        data_cur.close()
        conn.close()


    # data_cur.execute(sql)
    # add_data = data_cur.fetchall()
    # sql = """
    # select column_name from information_schema.columns where table_name='focus'\
    #     ORDER BY ORDINAL_POSITION;
    # """
    # data_cur.execute(sql)
    # colnames = data_cur.fetchall()# return a list [(),()...]
    # data_cur.close()
    # conn.close()

    # print('out of try')
    col_html, data_html = ret_html_content(colnames, add_data, 'del')
    # content = re.sub(r'\{%content%\}', str(add_data), content)
    new_content = re.sub(r'\{%table_head%\}', col_html, content)
    new_content = re.sub(r'\{%table_content%\}', data_html, new_content)
    return new_content


# @router('/index.py')
@router('/index.html')
def index(rematch):
    with open('./templates/index.html', 'r') as f:
        content = f.read()
    add_data = 'in INDEX func'
    content = re.sub(r'\{%content%\}', add_data, content)
    return content


# @router('/home.py')
@router('/home.html')
def home(rematch):
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
    data_cur.execute(
        "select column_name from information_schema.columns where table_name='berlin_crime'\
            ORDER BY ORDINAL_POSITION;")
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

    col_html, data_html = ret_html_content(colnames, add_data, 'add')
    # content = re.sub(r'\{%content%\}', str(add_data), content)
    new_content = re.sub(r'\{%table_head%\}', col_html, content)
    new_content = re.sub(r'\{%table_content%\}', data_html, new_content)
    return new_content


def ret_html_content(colnames, add_data, add_del_sign):
    """
    used when home.html and focus.html
    """
    if add_del_sign=='add':
        show_name = "Add"
        id_name = "toAdd"
    elif add_del_sign=='del':
        show_name = "Del"
        id_name = "toDel"
    data_html = ""
    col_name = [n[0] for n in colnames]
    col_html=f"""<tr class='head_tb'>
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
                <th>{show_name}<th>
            </tr>
    """

    for data in add_data:
        tb_template = f"""<tr class='data_tb'>
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
            <td>
                <input type="button" value={show_name} id={id_name} name={id_name} systemidvalue={data[20]}>
            </td>
        </tr>
        """
        data_html += tb_template
    return col_html, data_html


def application(environ: dict, set_request_head):
    func_name = environ['Request_Path']
    """
    NOTIC: WSGI invoke Server 'set_request_head' func
        not return HEAD directly.
    """
    set_request_head('200 OK', [{'Content-Type': 'text/html; charset=utf-8'},])
    # print(URL_DICT, func_name)
    try:
        # request_func = URL_DICT[func_name]
        # request_body = request_func()
        """
        NOTICE: here use for/else loop!!!
        """
        for url, func in URL_DICT.items():
            # print(url, func)
            rematch = re.match(url, func_name)
            if rematch:
                request_body = func(rematch)
                return request_body
                break
        else:
            return f'no such file...{func_name}'
    except Exception as e:
        return f'there is no corresponding file, error: {e}'
    else:
        return f'{str(environ)} 404'
