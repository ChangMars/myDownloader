# -*- coding: utf-8 -*-
import base64
import random
import re
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.exceptions import ProxyError

proxies_data = []


def get_random_proxies():
    if len(proxies_data) > 0:
        index = random.randint(0, len(proxies_data) - 1)
        proxy = proxies_data[index]
        return proxy
    else:
        return {}


def load_proxies_list_by_free_proxy_cz(proxies):
    proxyData = []
    offset = 1
    while offset < 5:
        if offset == 1:
            url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/all'
        else:
            url = 'http://free-proxy.cz/en/proxylist/country/all/http/ping/all/%s' % offset
        try:
            response = requests.get(url,
                                    headers={
                                        'Host': 'free-proxy.cz',
                                        'User-Agent': UserAgent().random,
                                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                        'Accept-Encoding': 'gzip, deflate, sdch',
                                        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                                    },
                                    proxies=get_random_proxies(),
                                    timeout=10
                                    )
            bs = BeautifulSoup(response.content, "lxml")
            table = bs.find('table', {'id': 'proxy_list'})
            if table is None:
                print('proxy_list is None')
                continue
            tr = table.findAll('tr')
            for r in tr:
                td = r.findAll('td')
                if len(td) == 0:
                    continue
                pattern = re.compile(r'(document\.write\(Base64\.decode\(")(.*)("\)\))')
                sc = td[0].findAll('script', {'type': 'text/javascript'})
                if len(sc) == 0:
                    continue
                match = pattern.match(sc[0].text)
                result = bytes.decode(base64.b64decode(match.group(2)))
                if 'HTTPS' == td[2].text:
                    proxy = {'https': 'https://%s' % result}
                else:
                    proxy = {'http': 'http://%s' % result}
                print(proxy)
                proxyData.append(proxy)
            print('free-proxy.cz 已取得%s個proxy' % len(proxyData))
            return proxyData
        except ProxyError:
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            pass
        offset += 1
        time.sleep(2)


def load_proxies_list_by_proxydb():
    proxyData = []
    url = 'http://proxydb.net/?protocol=http&country_='
    error = 0
    while error < 10:
        try:
            response = requests.get(url,
                                    headers={
                                        'Host': 'proxydb.net',
                                        'User-Agent': UserAgent().random,
                                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                        'Accept-Encoding': 'gzip, deflate, sdch',
                                        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                                    },
                                    proxies=get_random_proxies(),
                                    timeout=10
                                    )
            bs = BeautifulSoup(response.content, "lxml")
            table = bs.find_all('table', {'class': 'table table-sm table-hover'})
            if table is None:
                print('proxydb is None')
                continue
            tr = table[0].find_all('tr')
            for index in range(1, len(tr)):
                td = tr[index]
                td = td.findAll('td')
                if len(td) == 0:
                    continue
                ip = td[0].text.replace('\n', '')
                proxy = {'http': 'http://%s' % ip}
                print(proxy)
                proxyData.append(proxy)
            print('proxydb 已取得%s個proxy' % len(proxyData))
            return proxyData
        except ProxyError:
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(e)
            error += 1
    print('proxydb 已取得%s個proxy' % len(proxyData))
    return proxyData


def load_proxies_list_by_free_proxy_lists_net(proxies):
    proxyData = []
    url = 'http://www.freeproxylists.net/zh/?c=&pt=&pr=HTTP&a[]=0&a[]=1&a[]=2&u=50'
    error = 0
    while error < 10:
        try:
            response = requests.get(url,
                                    headers={
                                        'Host': 'freeproxylists.net',
                                        'User-Agent': UserAgent().random,
                                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                        'Accept-Encoding': 'gzip, deflate, sdch',
                                        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                                    },
                                    proxies=get_random_proxies(),
                                    timeout=10
                                    )
            bs = BeautifulSoup(response.content, "lxml")
            table = bs.find('table', {'class': 'DataGrid'})
            if table is None:
                print('DataGrid is None')
                continue
            tr = table.findAll('tr')
            for index in range(1, len(tr)):
                td = tr[index]
                td = td.findAll('td')
                if len(td) == 0:
                    continue
                sc = td[0].findAll('script', {'type': 'text/javascript'})
                if len(sc) == 0:
                    continue
                port = td[1].text
                data = re.findall(r'IPDecode\(\"(.*)\"\)', sc[0].string)
                ip = urllib.parse.unquote(data[0])
                bs = BeautifulSoup(ip, "lxml")
                result = bs.find('a')
                ip = result.text
                if 'HTTPS' == td[2].text:
                    proxy = {'https': 'https://%s:%s' % (ip, port)}
                else:
                    proxy = {'http': 'http://%s:%s' % (ip, port)}
                print(proxy)
                proxyData.append(proxy)
        except ProxyError:
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(e)
            error += 1
    print('freeproxylists.net 已取得%s個proxy' % len(proxyData))
    return proxyData


def load_proxies_list():
    global proxies_data
    if len(proxies_data) > 0:
        return proxies_data
    try:
        proxies_data += load_proxies_list_by_httptunnel()
    except Exception as e:
        print('load_proxies_list_by_httptunnel():', e)
    try:
        proxies_data += load_proxies_list_by_proxydb()
    except Exception as e:
        print('load_proxies_list_by_proxydb():', e)
    # try:
    #     result += load_proxies_list_by_free_proxy_lists_net(result)
    # except Exception as e:
    #     print('load_proxies_list_by_free_proxy_lists_net():', e)
    # if len(result) < 30:
    #     try:
    #         result += load_proxies_list_by_free_proxy_cz(result)
    #     except Exception as e:
    #         print('load_proxies_list_by_free_proxy_cz():', e)
    print('all proxies: %s' % str(len(proxies_data)))
    if len(proxies_data) == 0:
        load_proxies_list()
    return proxies_data


def load_proxies_list_by_httptunnel():
    proxyData = []
    error = 0
    while error < 10:
        try:
            response = requests.get('http://www.httptunnel.ge/ProxyListForFree.aspx',
                                    headers={'Host': 'www.httptunnel.ge',
                                             'Connection': 'keep-alive',
                                             'Cache-Control': 'max-age=0',
                                             'Upgrade-Insecure-Requests': '1',
                                             'User-Agent': UserAgent().random,
                                             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                             'Accept-Encoding': 'gzip, deflate, sdch',
                                             'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                                             'Referer': 'http://www.httptunnel.ge/ProxyListForFree.aspx'},
                                    timeout=10
                                    )
            bs = BeautifulSoup(response.content, "lxml")
            table = bs.find('table', {'id': 'ctl00_ContentPlaceHolder1_GridViewNEW'})
            a = table.findAll('a')
            for ip in a:
                proxy = {'http': 'http://%s' % ip.string}
                print(proxy)
                proxyData.append(proxy)
            print('httptunnel 已取得%s個proxy' % len(proxyData))
            return proxyData
        except ProxyError:
            continue
        except requests.exceptions.Timeout:
            continue
        except Exception as e:
            print(e)
            error += 1
    print('httptunnel 已取得%s個proxy' % len(proxyData))
    return proxyData
