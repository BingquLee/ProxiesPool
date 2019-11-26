# -*- coding: utf-8 -*-
from pymysql.cursors import DictCursor

from Config import conn


def get_proxy(country):
    cursor = conn.cursor(DictCursor)

    sql = "SELECT * FROM {} ORDER BY score DESC LIMIT 1,1".format(country)
    cursor.execute(sql)
    proxy = cursor.fetchall()[0]
    print(proxy)
    return proxy


if __name__ == '__main__':
    proxy = get_proxy('US')
