# -*- coding: utf-8 -*-
import requests
from pymysql.cursors import DictCursor

from Config import conn


def check_proxies():
    cursor = conn.cursor(DictCursor)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    sql_db_list = "SELECT table_name FROM information_schema.tables WHERE table_schema='proxies_pool' AND table_type='base table';"
    cursor.execute(sql_db_list)
    db_list = cursor.fetchall()
    for i in db_list:
        country = i['table_name']
        sql_proxies = "SELECT * FROM {} WHERE protocol='https'".format(country)
        cursor.execute(sql_proxies)
        proxies_list = cursor.fetchall()
        for proxy in proxies_list:
            host = proxy['host']
            port = proxy['port']
            proxy_id = proxy['id']
            score = proxy['score']
            try:
                print(requests.get(url='https://www.baidu.com', proxies={"https": "{}:{}".format(host, port)}, headers=headers, timeout=10).text)
                score = 100
            except Exception as e:
                score -= 1
            if score != 0:
                sql_update = "UPDATE {} SET score={} WHERE id='{}'".format(country, score, proxy_id)
                cursor.execute(sql_update)
            else:
                sql_delete = "DELETE FROM {} WHERE id='{}'".format(country, proxy_id)
                cursor.execute(sql_delete)
            conn.commit()


if __name__ == '__main__':
    check_proxies()
