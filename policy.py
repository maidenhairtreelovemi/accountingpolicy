from requests import get
import re

class Spider(object):
    def __init__(self):
        print('开始爬取内容...')


    #用于获取网页的源代码
    def getsource(self,url):
        html = get(url)
        html.encoding = 'utf-8'
        return html.text
    #改变连接中的页码数
    def changepage(self,url,tatal_page):
        now_page = int(re.search('index_831221_(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,tatal_page + 1):
            link = re.sub('index_831221_\d+','index_831221_%s'%i,url,re.S)
            page_group.append(link)
        return page_group


    #抓取每篇文章的信息
    def geteveryarticle(self,source):
        everyarticle = re.findall('(<a.*?</a>)',source,re.S)
        return everyarticle


    #从每篇文章中抓取我们想要的信息
    def getinfo(self,eacharticle):
        info = {}
        info['title'] = str(re.search('</span>(.*?)</a>',eacharticle,re.S).group(1))#没有加括号不要随便group，会报错
        info['date'] = str(re.search('<span>.*?</span>',eacharticle,re.S))#注意这里没有str会出错
        info['url'] = str(re.search('../(.*?)"',eacharticle,re.S))
        return info


     #存储为文本文件
    def saveinfo(self,articleinfo):
        f = open('info.text','a',encoding = 'utf-8')
        for each in articleinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('date:' + each['date'] + '\n')
            f.writelines('url:' + each['url'] + '\n\n')
        f.close()




if __name__ == '__main__':
    articleinfo = []
    url = 'http://www.chinatax.gov.cn/n810341/n810760/index_831221_1.html'
    policyspider = Spider()
    all_links = policyspider.changepage(url,21)
    print(all_links)
    for link in all_links:
        print('正在处理页面:' + link)
        html = policyspider.getsource(link)
        everyarticle = policyspider.geteveryarticle(html)
        for each in everyarticle:
            info = policyspider.getinfo(each)
            articleinfo.append(info)
        policyspider.saveinfo(articleinfo)









