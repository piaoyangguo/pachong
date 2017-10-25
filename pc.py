# coding: utf-8
import urllib2
from lxml.html import soupparser
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class lxmlxpathpaser():
    def __init__(self):
        self.opener = urllib2.build_opener()
        self.setRequestHeaders()

    def setRequestHeaders(self, headers=[('User-agent', 'Mozilla/5.0')]):
        self.opener.addheaders = headers

    def getPageContent(self, url, encoding=None):
        u'获取html串'
        try:
            htmlAll = self.opener.open(url, timeout=15).read()
        except:
            htmlAll = ''
        if encoding:
            return htmlAll.decode(encoding, "ignore")
        else:
            return htmlAll

    def diglink(self, node):
        u'挖掘页面链接'
        linklist = []
        htmlstr = self.getPageContent(node.url, node.encoding)
        if htmlstr:
            dom = soupparser.fromstring(htmlstr)
            nodes = dom.xpath(node.link)
            for n in nodes:
                if n.split("/")[:3] == node.url.split("/")[:3]:
                    linklist.append(n)
            for l in linklist:
                nw = webnode(node)
                nw.url = l
                if nw not in node.linklist:
                    node.linklist.append(nw)

    def getchildhtml(self, node):
        nodeclass = " class='%s'" % node.get("class") if node.get("class") else ""
        allstr = "<%s%s>" % (node.tag, nodeclass)
        if node.getchildren():
            for i in node.getchildren():
                if i.getchildren():
                    allstr += self.getchildhtml(i)
                else:
                    if i.text:
                        iclass = "class='%s'" % i.get("class") if i.get("class") else ""
                        allstr += "<%s%s>" % (i.tag, iclass)
                        allstr += i.text
                        allstr += "</%s>" % i.tag
        else:
            allstr += node.text
        allstr += "</%s>" % node.tag
        return allstr

    def dig(self, anode):
        self.diglink(anode)
        f = open("text.txt", "w")
        if anode.needlink:
            for i in anode.linklist:
                print '%s digging url: %s' % (i, i.url)
                htmlstr = self.getPageContent(i.url, i.encoding)
                dom = soupparser.fromstring(htmlstr)
                nodes = dom.xpath(i.content)
                for n in nodes:
                    if anode.html:
                        content = self.getchildhtml(n)
                    else:
                        content = n.text_content()
                    f.write(content)
                    f.write("\n\n\n")
        else:
            print 'digging url: %s' % anode.url
            htmlstr = self.getPageContent(anode.url, anode.encoding)
            dom = soupparser.fromstring(htmlstr)
            nodes = dom.xpath(anode.content)
            for n in nodes:
                if anode.html:
                    content = self.getchildhtml(n)
                else:
                    content = n.text_content()
                f.write(content)
                f.write("\n\n\n")
        f.close()


class webnode():
    def __init__(self, node=None):
        self.url = node.url if node else ""
        self.encoding = node.encoding if node else None  # 字符编码
        self.html = node.html if node else False  # 标签和样式
        self.content = node.content if node else None  # contentxpath
        self.link = node.link if node else None  # linkxpath
        self.needlink = node.needlink if node else False  # needlink
        self.linklist = None if node else []  # 多页
        if self.linklist == []:
            self.linklist.append(self)


def collect():
    newwebxpath = lxmlxpathpaser()
    newwebnode = webnode()
    newwebnode.url = u"http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%s&kw=python+web&sm=0&p=5" % u"北京"
    newwebnode.encoding = "utf-8"
    # newwebnode.content = "//tr[@class='newlist_tr_detail']//ul"
    newwebnode.html = False
    newwebnode.content = "//tr/td"
    newwebnode.link = "//div[@class='pagesDown']//a/@href"
    newwebxpath.dig(newwebnode)


collect()
