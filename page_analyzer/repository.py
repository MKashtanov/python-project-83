import datetime
import psycopg2
from psycopg2.extras import NamedTupleCursor


class UrlsRepository:
    database_url = None

    def __init__(self, database_url):
        self.database_url = database_url

    def __connect(self, conn=None):
        if conn is None:
            conn = psycopg2.connect(self.database_url)
        return conn

    def __do_insert(self, query, values, conn=None):
        conn = self.__connect(conn)
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(query, values)
        conn.commit()

    def __do_select(self, query, values=None, conn=None):
        conn = self.__connect(conn)
        with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(query, values)
            result = curs.fetchall()
        return result

    def add_url(self, url, conn=None):
        conn = self.__connect(conn)
        result = self.find_url_by_name(url, conn)
        if result:
            return result, False

        current_date = datetime.datetime.now()
        query = """INSERT INTO urls (name, created_at)
            VALUES (%s, %s);"""
        item_tuple = (url, current_date)
        self.__do_insert(query, item_tuple, conn)
        result = self.find_url_by_name(url, conn)
        return result, True

    def find_url_by_id(self, id, conn=None):
        conn = self.__connect(conn)
        query = "SELECT * from urls WHERE id=%s"
        result = self.__do_select(query, (id,), conn)
        if result:
            result = result[0]
        return result

    def find_url_by_name(self, name, conn=None):
        conn = self.__connect(conn)
        result = None
        value = str(name)
        if value:
            query = "SELECT * from urls WHERE name=%s"
            result = self.__do_select(query, (value,), conn)
        if result:
            result = result[0]
        return result

    def get_all_url(self, conn=None):
        conn = self.__connect(conn)
        query = """SELECT ur.id, ur.name, ur.created_at,
            max(uc.created_at) as last_check, uc.status_code
            FROM urls AS ur
            LEFT JOIN url_checks AS uc on uc.url_id = ur.id
            GROUP BY ur.id, ur.name, ur.created_at, uc.status_code
            ORDER BY ur.id DESC;"""
        result = self.__do_select(query, conn=conn)
        return result

    def add_check(self, url, seo_info, conn=None):
        conn = self.__connect(conn)
        url_item = self.find_url_by_name(url, conn)
        if url_item:
            url_id = url_item.id
        else:
            return False
        query = """INSERT INTO url_checks
            (url_id, status_code, h1, title, description)
            VALUES (%s, %s, %s, %s, %s);"""
        item_tuple = (url_id,
                      seo_info['status_code'],
                      seo_info['h1'],
                      seo_info['title'],
                      seo_info['description'],
                      )
        self.__do_insert(query, item_tuple, conn)
        return True

    def find_checks_by_url_id(self, id, conn=None):
        conn = self.__connect(conn)
        query = "SELECT * from url_checks WHERE url_id=%s"
        result = self.__do_select(query, (id,), conn)
        return result
