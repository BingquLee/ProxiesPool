# -*- coding: utf-8 -*-
import base64
import hashlib
import re

import requests
from lxml import etree

from Config import conn


def crawl_proxies(country='US', proxies_type='https'):

    cursor = conn.cursor()

    url = 'http://free-proxy.cz/en/proxylist/country/{}/{}/ping/level2'.format(country, proxies_type)

    session = requests.Session()

    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
    }

    html = session.get(url=url).text
    tree = etree.HTML(html)
    tr_list = tree.xpath('//table[@id="proxy_list"]/tbody/tr')
    for tr in tr_list:
        ip_base64_raw = tr.xpath('./td[1]/script/text()')
        if not ip_base64_raw:
            continue
        ip_base64 = re.findall(r'document\.write\(Base64.decode\("(.*?)"\)\)', ip_base64_raw[0])[0]
        host = base64.b64decode(ip_base64).decode('utf-8')
        port = tr.xpath('./td[2]/span/text()')[0]
        protocol = str(tr.xpath('./td[3]/small/text()')[0]).lower()
        proxy_id = hashlib.md5('{}://{}:{}'.format(protocol, host, str(port)).encode(encoding='UTF-8')).hexdigest()
        score = 100

        sql = "INSERT IGNORE INTO {} (id, host, port, protocol, score) VALUE ('{}', '{}', {}, '{}', {})".format(country, proxy_id, host, port, protocol, score)
        print(sql)
        print(cursor.execute(sql))
        conn.commit()


if __name__ == '__main__':
    crawl_proxies()
