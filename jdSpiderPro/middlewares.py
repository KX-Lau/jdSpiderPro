import random
import time
from scrapy.http import HtmlResponse
from scrapy import signals
from twisted.internet.error import  TimeoutError, ConnectionRefusedError

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.2669.400 QQBrowser/9.6.10990.400',
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
]

# 需要定期更新
ip_list = [
    'http://58.220.95.86:9401',     # 403被禁
    'http://221.182.31.54:8080',
    'http://165.225.32.117:10356',
    'http://62.210.90.200:8080',
    'http://165.225.32.107:13084',
    'http://221.122.91.76:9480',
    'http://58.220.95.78:9401',     # 403
    'https://150.138.253.72:808',
    'http://58.220.95.79:10000',
    'http://165.225.84.146:8800',
    'http://221.122.91.34:80',
    'http://183.220.145.3:80',
    'http://165.225.32.106:10223',
    'http://58.220.95.54:9400',
    'http://221.122.91.64:80',
    'http://58.220.95.90:9401',     #
    'http://165.225.32.116:10223',
    'http://116.196.85.150:3128',
    'http://58.220.95.80:9401',
    'http://221.122.91.64:9401',
    'http://51.161.116.223:3128',
    'http://125.124.26.98:3128',
    'http://165.225.32.113:10223',
    'http://221.122.91.65:80',
    'http://103.47.66.42:8080',
    'http://165.225.32.109:10223',

]


class JdspiderproSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdspiderproDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # 拦截正常的请求
    def process_request(self, request, spider):
        # UA伪装
        request.headers['User-Agent'] = random.choice(user_agent_list)
        # print('正在使用的UA>>>>>>>>>>>>', request.headers['User-Agent'])

        request.meta['proxy'] = random.choice(ip_list)
        # request.meta['proxy'] = 'http://175.98.12.69:8088'

        # print('正在使用的ip>>>>>>>>>>>>', request.meta['proxy'])
        # print(spider.settings['TEST'])
        # 返会None, 表示继续处理该请求
        return None

    # 拦截所有的响应
    def process_response(self, request, response, spider):

        if request.url.startswith('https://search.jd.com/search?keyword'):
            # 拿到浏览器对象
            browser = spider.browser
            browser.get(request.url)
            # 执行下滑到底部的操作
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            # 休眠, 等待获取完全信息
            time.sleep(8)
            # 包含动态加载后30条的数据
            page_text = browser.page_source
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        else:
            return response
        # return response

    # 拦截发生异常的请求
    def process_exception(self, request, exception, spider):

        if isinstance(exception, (TimeoutError, ConnectionRefusedError)):
            # print('此时ip---{},  重新发送请求.................'.format(request.meta['proxy']))
            # request.meta['proxy'] = random.choice(ip_list)
            # print('!!!!!!!!!请求ip出错--------------', request.meta['proxy'], exception)
            return request
        else:
            print('发生异常的请求>>>>>>>>>>>>>', request, request.meta['proxy'], exception)
            return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
