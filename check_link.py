import os
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from notify import send

# 只为测试用
os.environ['check_urls'] = 'https://www.aitanqin.com,https://www.aitanqin.com/guitar/'


def check_dead_links(url):
    # 发送 GET 请求获取页面内容
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # 获取页面中所有的链接并去重
    links = set(link.get("href") for link in soup.find_all("a"))

    # 检查每个链接的有效性
    dead_links = []
    for href in links:
        if href and not href.startswith("#"):  # 排除锚点链接
            link_url = urljoin(url, href)  # 解析相对链接为绝对链接
            try:
                link_response = requests.head(link_url)
                # 521 是miit.gov.cn的自定义状态
                if link_response.status_code not in [200, 302, 521]:
                    dead_links.append(link_url)
            except requests.exceptions.RequestException:
                dead_links.append(link_url)

    return dead_links


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    urls = os.getenv("check_urls")
    url_list = urls.split(',')
    send_msg = ''
    if urls and len(url_list) > 0:
        bad_urls = []
        for surl in url_list:
            print(f'开始检查：{surl}')
            bad_s = check_dead_links(surl)
            if len(bad_s) > 0:
                bad_urls.append(bad_s)
                print(f'源页面：{surl}有{len(bad_s)}条死链')
                print(bad_s)
        if len(bad_urls) > 0:
            _s_bad_url = ', '.join(bad_urls)
            send_msg = f'检测到死链{len(bad_urls)}条：{_s_bad_url}'

        else:
            send_msg = '检测完成，没有发现死链！'

    else:
        send_msg = '没有配置检查地址'
    send('网站链接检查报告', send_msg)