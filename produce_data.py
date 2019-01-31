'''
    训练数据不是那么好处理，监督学习最麻烦的就是准备这些数据了。。
    这里爬取豆瓣的电影影评.后期可以出一个评论一些，你的评分就出来了
'''
from bs4 import BeautifulSoup
from urllib import request
import time

# 20一页，0,20,40...
url_xxjzw = r'https://movie.douban.com/subject/4840388/reviews?sort=time&start='
url_fkwxr = r'https://movie.douban.com/subject/25986662/reviews?sort=time&start='


# 获取页面
def get_html(url):
    head = {}
    head[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    target_req = request.Request(url=url, headers=head)
    target_response = request.urlopen(target_req)
    target_html = target_response.read().decode('utf-8', 'ignore')
    # 创建BeautifulSoup对象
    listmain_soup = BeautifulSoup(target_html, 'lxml')
    return listmain_soup


# 解析豆瓣评论并存到文件中
def resolu_soup(soup_page):
    reviews = soup_page.find_all('div', class_='main review-item')
    for each_review in reviews:
        # 评分是1-5星，用class不同来表示的。allstar40 main-title-rating,h2里面是主评，<div class="short-content">是详评
        score = 0 #未知的评分
        for i in range(1, 6):
            class_name='allstar'+str(i*10)+' main-title-rating'
            score_maybe=each_review.find_all('span', class_=class_name)
            if(len(score_maybe)>0):
                score = i
        print("这个人的评分是"+str(score))
        short_review = each_review.find('h2').text.replace(' ','') #短评
        with open("../doc/data_fkwxr.txt", "a",encoding='utf-8') as f: #写到样本库用于--学习可能有没有分的
            f.write(short_review+" "+str(score)+'\n')
        long_review = each_review.find('div', class_='short-content').text.replace(' ','').replace('(展开)','')

        with open("../doc/fkwxr.txt", "a",encoding='utf-8') as f: #写在用于分析电影评价的文本里
            f.write(short_review+" "+long_review+'\n')

if __name__ == '__main__':
    # 预先得知一下评论数量（也可以现请求一次获取）
    for i in range(3):  # 6页
        resolu_soup(get_html(url_fkwxr + str(i * 20)))
        time.sleep(1)
