import datetime
import psycopg2
from psycopg2.extras import NamedTupleCursor


class UrlsRepository:
    database_url = None

    def __init__(self, database_url):
        self.database_url = database_url

    def __connect(self):
        try:
            conn = psycopg2.connect(self.database_url)
            print('Connection to database is OK')
            return conn
        except psycopg2.OperationalError as e:
            print(f'Unable to connect!\n{e}')

    def __get_next_id(self, table):
        select_query = f'SELECT MAX(id) FROM {table};'
        conn = self.__connect()
        with conn.cursor() as curs:
            curs.execute(select_query)
            record = curs.fetchone()
        id = record[0]
        result = 1 if id is None else id + 1
        return result

    def add_url(self, url):
        new_id = self.__get_next_id('urls')
        current_date = datetime.datetime.now()
        insert_query = """INSERT INTO urls (id, name, created_at)
            VALUES (%s, %s, %s);"""
        item_tuple = (new_id, url, current_date)

        conn = self.__connect()
        with conn.cursor() as curs:
            curs.execute(insert_query, item_tuple)
        conn.commit()
        print(f'1 запись успешно вставлена. id={new_id}')
        result = self.find_one_url(name=url)
        return result

    def find_urls(self, id=None, name=None):
        result = None
        key, value = None, None
        if id:
            key, value = 'id', str(id)
        elif name:
            key, value = 'name', str(name)
        if key:
            conn = self.__connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(f"SELECT * from urls WHERE {key}=%s", (value,))
                result = curs.fetchall()
        return result

    def find_one_url(self, id=None, name=None):
        result = self.find_urls(id, name)
        if result:
            result = result[0]
        return result

    def get_all_url(self):
        conn = self.__connect()
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            query = """SELECT ur.id, ur.name, ur.created_at,
                max(uc.created_at) as last_check, uc.status_code
                FROM urls AS ur
                LEFT JOIN url_checks AS uc on uc.url_id = ur.id
                GROUP BY ur.id, ur.name, ur.created_at, uc.status_code
                ORDER BY ur.id DESC;"""
            curs.execute(query)
            result = curs.fetchall()
        return result

    def add_check(self, url, result_check):
        new_id = self.__get_next_id('url_checks')
        current_date = datetime.datetime.now()
        url_id = self.find_one_url(name=url).id
        status_code = result_check['status_code']
        h1 = result_check['h1']
        title = result_check['title'][:110]
        description = result_check['description'] \
            if len(result_check['description']) <= 160 \
            else f"{result_check['description'][:157]}..."
        insert_query = """INSERT INTO url_checks
            (id, url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        item_tuple = (new_id, url_id, status_code,
                      h1, title, description, current_date)

        conn = self.__connect()
        with conn.cursor() as curs:
            curs.execute(insert_query, item_tuple)
        conn.commit()
        return True

    def find_checks(self, id=None, url=None):
        result, value = None, None
        if id:
            value = str(id)
        elif url:
            url_item = self.find_one_url(name=url)
            if url_item:
                value = url_item.id
        if value:
            conn = self.__connect()
            with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                request = "SELECT * from url_checks WHERE url_id=%s"
                curs.execute(request, (value,))
                result = curs.fetchall()
        return result
