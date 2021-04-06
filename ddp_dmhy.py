#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://pastebin.ubuntu.com/p/mGP7JRpBtd
https://c.tieba.baidu.com/p/7192130039
"""
import getopt
import logging
import os
import sys
from typing import Optional

import arrow
import requests
import uvicorn
from bs4 import BeautifulSoup
from fastapi import FastAPI

logger = logging.getLogger("ddp_dmhy")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
formatter = logging.Formatter('%(levelname)-5s %(asctime)5s %(name)-5s > %(message)s')
ch.setFormatter(formatter)
ch.close()
logger.setLevel(logging.DEBUG)

run_host = "0.0.0.0"
# run_host = "127.0.0.1"
run_port = 8000
http_proxy = ""
# http_proxy = "http://127.0.0.1:1081"

app = FastAPI()
dmhy_base_uri = "https://share.dmhy.org"
dmhy_type_and_subgroup_uri = f"{dmhy_base_uri}/topics/advanced-search?team_id=0&sort_id=0&orderby="
dmhy_list_uri = f"{dmhy_base_uri}/topics/list/page/1?keyword={{0}}&sort_id={{1}}&team_id={{2}}&order=date-desc"
unknown_subgroup_id = -1
unknown_subgroup_name = "未知字幕组"


def get_proxies():
    if http_proxy:
        return {'http': http_proxy, 'https': http_proxy}


def parse_list_tr(tr):
    td0 = tr.select("td")[0]
    td1 = tr.select("td")[1]
    td2 = tr.select("td")[2]
    td3 = tr.select("td")[3]
    td4 = tr.select("td")[4]
    c1 = len(td2.select("a"))
    td1_a0 = td1.select("a")[0]
    td2_a0 = td2.select("a")[0]
    td2_a_last = td2.select("a")[-1]
    td3_a0 = td3.select("a")[0]

    return {
        "Title": td2_a_last.text.strip(),
        "TypeId": int(td1_a0["href"].replace("/topics/list/sort_id/", "")),
        "TypeName": td1_a0.text.strip(),
        "SubgroupId": unknown_subgroup_id if c1 != 2 else int(td2_a0["href"].replace("/topics/list/team_id/", "")),
        "SubgroupName": unknown_subgroup_name if c1 != 2 else td2_a0.text.strip(),
        "Magnet": td3_a0["href"],
        "PageUrl": dmhy_base_uri + td2_a_last["href"],
        "FileSize": td4.text.strip(),
        "PublishDate": arrow.get(td0.select("span")[0].text.strip()).format("YYYY-MM-DD HH:mm:ss")
    }


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/subgroup")
def subgroup():
    res = requests.get(dmhy_type_and_subgroup_uri, proxies=get_proxies())
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    options = soup.select("select#AdvSearchTeam option")
    subgroups = [{"Id": int(o["value"]), "Name": o.text} for o in options]
    subgroups.append({"Id": unknown_subgroup_id, "Name": unknown_subgroup_name})
    return {"Subgroups": subgroups}


@app.get("/type")
def type():
    res = requests.get(dmhy_type_and_subgroup_uri, proxies=get_proxies())
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    options = soup.select("select#AdvSearchSort option")
    return {"Types": [{"Id": int(o["value"]), "Name": o.text} for o in options]}


@app.get("/list")
def list(keyword: str, subgroup: Optional[int] = 0, type: Optional[int] = 0, r: Optional[str] = None):
    res = requests.get(dmhy_list_uri.format(keyword, type, subgroup), proxies=get_proxies())
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.select("table#topic_list tbody tr")
    has_more = True if soup.select("div.nav_title > a:contains('下一頁')") else False

    return {"HasMore": has_more, "Resources": [parse_list_tr(tr) for tr in trs]}


if __name__ == "__main__":
    log_level = "info"

    # https://stackoverflow.com/questions/49770999/docker-env-for-python-variables/49771684
    run_host = os.getenv('DDP_HOST', run_host)
    run_port = os.getenv('DDP_PORT', run_port)
    http_proxy = os.getenv('DDP_HTTP_PROXY', http_proxy)

    # https://www.knowledgehut.com/blog/programming/sys-argv-python-examples
    options, args = getopt.getopt(sys.argv[1:], "h:p:x:l:", ["host=", "port=", "http_proxy=", "log-level=", "help"])
    for name, value in options:
        if name in ['-h', '--host']:
            run_host = value
        elif name in ['-p', '--port']:
            run_port = int(value)
        elif name in ['-x', '--http_proxy']:
            http_proxy = value
        elif name in ['-l', '--log-level']:
            log_level = value
        elif name in ['--help']:
            print("Usage: [OPTIONS]")
            print("Options:")
            print("-h(--host) TEXT     API服务的域名或ip  [default:0.0.0.0]")
            print("-p(--port) INTEGER      API服务的端口  [default: 8000]")
            print("-x(--http_proxy) TEXT      API服务的http代理  [default: ]")
            print("-l(--log-level) [critical|error|warning|info|debug|trace] Log level. [default: info]")
            sys.exit()

    logger.info("host=%s port=%s http_proxy=%s log_level=%s" % (run_host, run_port, http_proxy, log_level))
    uvicorn.run(app, host=run_host, port=run_port, log_level=log_level)
