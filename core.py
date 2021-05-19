import os
import random

import requests
import json
import re
import time
import threading
import subprocess
from Utils import ReadConfig
import command
regex_ip = re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
regex_site = re.compile(r'^[0-9a-zA-Z\-]{1,16}\.[0-9a-zA-Z\-]{1,16}\.[0-9a-zA-Z\-]{2,10}$')


def async_run(f, *args, **kwargs):
    td = threading.Thread(target=f, args=(*args, *kwargs,))
    td.start()

def get_nodes():

    url = 'https://chia.woele.cc/chia/'
    headers = {
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.{random.randint(1000, 9999)}.212 Safari/537.36',
        'Cookie': f'guardret=b1GroZYUgZ33{random.randint(10000,99999)}VIyXw=='

    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.encoding = 'utf-8'
    # print(resp.text)
    result = re.findall(r'<tbody class="table-hover">(.*?)</tbody>',resp.text,re.S)[0]
    # print(result)
    nodes = re.findall(r'<td class="text-left">(.*?)</td>', result)
    nodes = [i for i in nodes if len(regex_site.findall(i)) > 0 or len(regex_ip.findall(i)) > 0]

    with open('nodes.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(nodes))

def connect_nodes(dir, ListWidgetSignal, ):
    try:
        filename = 'nodes.json'
        with open(filename, encoding='utf-8') as f:
            nodes = json.loads(f.read())
        print(nodes)
        ListWidgetSignal(f'共有节点数据{len(nodes)}条')
        def f(cmd, ):
            # print(command)
            # ListWidgetSignal(command)
            print(cmd)
            subprocess.call(cmd,shell=True)

            # print(res)

        for i in nodes:
            command = f'{dir}\\resources\\app.asar.unpacked\\daemon\\chia.exe show -a {i}:8444'

            async_run(f, command)
            ListWidgetSignal(f'正在同步节点->{i}')
            time.sleep(1)
    except Exception as e:
        ListWidgetSignal(f'{e}')

if __name__=='__main__':
    config = ReadConfig('node.ini')
    print(config)
    while True:
        try:
            get_nodes()
        except Exception as e:
            print(f'Failed to get node list,use old list ErrorDetail-->{e}')
        connect_nodes(config['chia_path'])
        time.sleep(int(config['time_interval'])*60)