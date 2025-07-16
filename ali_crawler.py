# coding: utf-8
import re
import urllib.request

url = 'http://mysql.taobao.org/monthly/'
# 打开网址
response = urllib.request.urlopen(url)
# 读取源代码并转为unicode
content = response.read().decode('utf-8')
# print(content)

# 网页主题的正则表达式
re_topic = re.compile(r'<!-- <title>(.*?)</title> -->', re.S)
# 获取网页主题
topic = re.findall(re_topic, content)[0]

# 文章标题和对应链接的正则表达式
re_month_blog_address = re.compile(r'<a target="_top" class="main" href="/monthly/(.*?)">', re.S)
# 文章标题和对应链接
month_blog_list = re.findall(re_month_blog_address, content)

# 写入主题，并重置目标文件
with open(file='阿里数据库内核月报.md', mode='w') as f:
    # 写入主题
    f.write(f'## {topic}\n')

# 写入月报的月份和每篇文章的标题和对应链接（用 markdown 格式）
for month_blog in month_blog_list:
    # 月份，例如 2016/07
    child_title = month_blog
    # 阿里内核月报 url + 月份，得到每个月报的地址
    month_blog_url = url + month_blog
    # 打开网址
    response = urllib.request.urlopen(month_blog_url)
    # 读取源代码并转为unicode
    content = response.read().decode('utf-8')
    # 每月月报的文章标题和链接地址的正则表达式
    re_article_title_link = re.compile(r'class="main" href="/monthly/(.*?)">(.*?)</a></h3></li>', re.S)
    # 获取每月月报的文章标题和链接地址
    article_title_link_list = re.findall(re_article_title_link, content)

    with open(file='阿里数据库内核月报.md', mode='a') as f:
        # 写三级标题：月份
        f.write('### {child_title}\n')
        f.write('---\n')
        f.write('\n')
        for article_title_link in article_title_link_list:
            # 获取文章链接
            article_link = url + article_title_link[0]
            # 获取文章标题
            article_title = article_title_link[1]
            # 以 markdown 格式组织文章标题和链接
            title_md_fmt = f"[{article_title}]({article_link})"
            # 将文章标题和链接写入文件中
            f.write(f'{title_md_fmt}\n')