import psycopg2
from psycopg2.extras import DictCursor


# データベースを開く --- (*1)
def get_connection():
    #接続
    connector =  psycopg2.connect('postgresql://{user}:{password}@{host}:{port}/{dbname}'.format(
                user="postgres",        #ユーザ
                password="postgres",     #パスワード
                host="db",       #ホスト名 host="localhost"
                port="5432",            #ポート
                dbname="postgres"))    #データベース名
    return connector


# SQLを実行する --- (*3)
def exec(sql, *args):
    res = None
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql,*args)
            res = cur.statusmessage
    return res



# SQLを実行して結果を得る --- (*4)
def select(sql, *args):
    res = None
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql,*args)
            res = cur.fetchall()
    return res

# SQLを実行して結果を得る --- (*4)
def select_fetchone(sql, *args):
    res = None
    with get_connection() as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(sql,*args)
            res = cur.fetchone()
    return res

