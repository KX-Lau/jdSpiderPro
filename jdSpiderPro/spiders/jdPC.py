import json

import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from jdSpiderPro.items import JdcommentItem

chrome_options = Options()
chrome_options.add_argument('--headless')               # 浏览器不提供可视化界面, 即无头模式
chrome_options.add_argument('--disable-gpu')            # 官方文档建议, 避免bug
chrome_path = r'./jdSpiderPro/utils/chromedriver.exe'               # 指定浏览器位置


class JdpcSpider(scrapy.Spider):
    name = 'jdPC'

    # 起始url
    # start_urls = ['https://httpbin.org/get']
    start_urls = ['https://search.jd.com/search?keyword=电脑&ev=exbrand_戴尔（Dell）']

    # 搜索页url
    url = 'https://search.jd.com/search?keyword=电脑&ev=exbrand_戴尔（Dell）&page=%d'

    # 商品评论url
    comment_url = 'https://club.jd.com/comment/productPageComments.action?productId=%s&score=0&sortType=5&page=%d&pageSize=10'

    # 搜索页的页码
    page = 1

    # 实例一个浏览器对象
    browser = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)

    def parse(self, response):
        """解析搜索页, 获取商品id和店铺, 并过滤, 再对过滤后的商品详情页发请求"""

        # print(response.text)
        print('正在爬取商品的第{}页.........................'.format((self.page + 1) // 2), end=' ')

        li_list = response.xpath('//*[@id="J_goodsList"]/ul/li')
        print(len(li_list))

        if len(li_list) == 60:
            for li in li_list:

                # 爬取到商品id
                goods_id = li.xpath('@data-sku').extract_first()
                shop = li.xpath('./div/div[5]/span/a/text()')
                shop = shop.extract_first() if shop else '无'
                # print(goods_id, shop)

                # 过滤掉官方,自营和二手店家的商品
                if not ('自营' in shop or '二手' in shop or '官方' in shop):
                    # print(goods_id, shop)

                    citem = JdcommentItem()
                    citem['goods_id'] = goods_id
                    citem['goods_shop'] = shop
                    citem['comment_cur_page'] = 0

                    print('正在爬取商品{}评论的第1页.........................'.format(goods_id))

                    # 根据商品id, 补全商品评论的url
                    new_comment_url = format(self.comment_url % (goods_id, 0))
                    # print(gitem, new_comment_url)

                    # 发送请求, 并传递参数
                    yield Request(url=new_comment_url, callback=self.parse_comment,
                                  meta={'citem': citem})

            # 下一页搜索页
            if self.page < 3:
                self.page += 2
                new_url = format(self.url % self.page)
                # print(new_url)

                # 发送爬取每页商品页的请求
                yield Request(url=new_url, callback=self.parse, dont_filter=True)

            # 最后一页搜索页, 退出浏览器
            if self.page == 3:
                self.browser.quit()

        # 每页的商品没有全部加载时, 重新发送请求
        else:
            print(response.url)
            yield Request(url=response.url, callback=self.parse, dont_filter=True)

    def parse_comment(self, response):
        """解析商品评论"""

        citem = response.meta['citem']

        if response.text:
            comment_info = json.loads(response.text)
            # print(comment_info)

            citem['comment_count'] = comment_info['productCommentSummary']['commentCount']
            citem['score1_count'] = comment_info['productCommentSummary']['score1Count']
            citem['score2_count'] = comment_info['productCommentSummary']['score2Count']
            citem['score3_count'] = comment_info['productCommentSummary']['score3Count']
            citem['score4_count'] = comment_info['productCommentSummary']['score4Count']
            citem['score5_count'] = comment_info['productCommentSummary']['score5Count']

            # 评论的最大页数
            citem['comment_max_page'] = comment_info['maxPage']

            print('{}评论的最大页数{}............'.format(citem['goods_id'], citem['comment_max_page']))

            # 评论列表
            comment_list = comment_info['comments']
            # print("comment_list>>>>>>>>>>", comment_list)
            if comment_list:
                for comment in comment_list:
                    # print("comment>>>>>>>>>>>>>>>>>>>>")
                    citem['user_id'] = comment['id']
                    citem['user_name'] = comment['nickname']
                    citem['goods_name'] = comment['referenceName']
                    citem['score'] = comment['score']
                    citem['comment_time'] = comment['creationTime']
                    citem['comment_content'] = comment['content'].replace('\n', ' ')
                    citem['reply_count'] = comment['replyCount']
                    citem['useful_count'] = comment['usefulVoteCount']
                    if comment.__contains__('productColor'):
                        citem['goods_color'] = comment['productColor']
                    else:
                        citem['goods_color'] = '无'

                    if comment.__contains__('productSize'):
                        citem['goods_size'] = comment['productSize']
                    else:
                        citem['goods_size'] = '无'

                    if comment.__contains__('afterUserComment'):
                        citem['after_comment'] = comment['afterUserComment']['content']
                    else:
                        citem['after_comment'] = '无'

                    yield citem
                    # print('citem', citem)

        if citem['comment_cur_page'] < 1:        # 控制爬取的评论页数
            citem['comment_cur_page'] += 1
            # print(response.url)
            print('正在爬取商品{}评论的第{}页.........................'.format(citem['goods_id'], citem['comment_cur_page'] + 1))

            # 根据商品id, 补全商品评论的url
            new_comment_url = format(self.comment_url % (citem['goods_id'], citem['comment_cur_page']))
            # print(new_comment_url)

            # 发送爬取每个商品评论请求, 并传递参数
            yield Request(url=new_comment_url, callback=self.parse_comment,
                          meta={'citem': citem}, dont_filter=True)


