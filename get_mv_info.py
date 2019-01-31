#-*- coding:utf-8 -*-

import sys
import requests
import urllib
import json
import re

"""
[{"episode":"","img":"https://img1.doubanio.com\/view\/photo\/s_ratio_poster\/public\/p2365823697.jpg","title":"冰川时代5：星际碰撞","url":"https:\/\/movie.douban.com\/subject\/25797778\/?suggest=%E5%86%B0%E5%B7%9D%E6%97%B6%E4%BB%A35","type":"movie","year":"2016","sub_title":"Ice Age: Collision Course","id":"25797778"}]

根据名称获取对应的豆瓣ID->返回一个列表,默认取第一个
"""
def get_id(keyword=None):
    keyword = keyword.encode('utf-8') if isinstance(keyword,unicode) else keyword
    q_word = urllib.quote(keyword)
    url = 'https://movie.douban.com/j/subject_suggest?q={0}'.format(q_word)
    #url = 'https://movie.douban.com/j/subject_suggest?q=%E5%86%B0%E5%B7%9D%E6%97%B6%E4%BB%A35'

    resp = requests.get(url)
    code = resp.status_code
    if code != 200:
        print 'get ID error'
        return False
    result = json.loads(resp.text)
    #print json.dumps(result,ensure_ascii=False)
    if result:
        return result[0].get('id')
    return None

"""
响应体json序列化
"""
def get_detail_json(content=None):
    key =  '<script type="application/ld+json">'
    cursor = content.find(key)
    if not cursor:
        return None
    buf = content[cursor+len(key):]
    key =  '</script>'
    cursor = buf.find(key)

    buf = buf[:cursor].strip().replace('\n','')
    try:
        j = json.loads(buf)
    except:
        j = eval(buf)
    return j
    
    

"""
    获取名称
"""
def get_name(info={}):
    return info.get('name')
    
"""
    获取豆瓣链接
"""
def get_douban_url(info={}):
    url = 'https://movie.douban.com/{0}'.format(info.get("url"))
    return url
 
"""
    获取图片链接
"""
def get_image_url(info={}):
    return info.get('image')
 
"""
    获取导演
"""
def get_directors(info={}):
    L = info.get('directors') or []
    names = [i.get('name') for i in L]
    return names
 
"""
    获取编剧
"""
def get_authors(info={}):
    L = info.get('author') or []
    names = [i.get('name') for i in L]
    return names
 

"""
    获取主演
"""
def get_actors(info={}):
    L = info.get('actor') or []
    names = [i.get('name') for i in L]
    return names
 
"""
    获取上映日期
"""
def get_publish_date(info={}):
    return info.get("datePublished")

"""
    获取影片类型
  "genre": ["\u559c\u5267", "\u52a8\u753b", "\u5192\u9669"],
"""
def get_movie_type(info={}):
    v = info.get("genre")
    return v
 
"""
    描述
  "description": "影片讲述松鼠奎特（克里斯·韦奇 Chris Wedge 配音）为了追松果，偶然引发了宇宙事件，改变并威胁着冰川时代的世界。为了拯救自己，话唠树懒希德（约翰·雷吉扎莫 John Leguizamo 配音...",
"""
def get_description(info={}):
    return info.get("description")
 
"""
评分
"""
def get_score(info={}):
    return info.get("aggregateRating",{}).get("ratingValue")


def get_info(info={}):
    D = dict(
        name = get_name(info),
        image_url= get_image_url(info),
        douban_url= get_douban_url(info),
        directors= get_directors(info),
        authors= get_authors(info),
        actors= get_actors(info),
        description= get_description(info),
        publish_date= get_publish_date(info),
        score= get_score(info),
        types= get_movie_type(info),
    )

    return D
 
 
def get_detail(id=None):
    url = 'https://movie.douban.com/subject/{0}/'.format(id)
    resp = requests.get(url)
    code = resp.status_code
    if code != 200:
        print 'get detail error'
        return False
    
    with open('./content.log', 'wb') as fp:
        fp.write(resp.content)
    info = get_detail_json(resp.text)
    return get_info(info)
    
    
if __name__ == '__main__':
    #1-根据名称获取 ID
    id = get_id(sys.argv[1])

    #2-根据ID获取影片内容
    resp=get_detail(id)
    for i in resp:
        print i, json.dumps(resp[i],ensure_ascii=False)
