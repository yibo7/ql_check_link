import os


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print('开始检测Url')
    urls = os.getenv("check_urls")
    print(urls)


