# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time


class JdspiderproPipeline(object):
    goods_fp = None
    comment_fp = None
    comment_writer = None
    goods_writer = None

    goods_col = ['goods_id', 'goods_shop', 'goods_name', 'comment_count', 'score1_count', 'score2_count',
                 'score3_count', 'score4_count', 'score5_count', 'comment_cur_page', 'comment_max_page']

    comment_col = ['user_id', 'user_name', 'goods_id', 'goods_name', 'goods_shop', 'comment_count', 'score1_count',
                   'score2_count', 'score3_count', 'score4_count', 'score5_count', 'comment_time', 'score',
                   'comment_content', 'reply_count', 'useful_count', 'goods_color', 'goods_size', 'after_comment',
                   'comment_cur_page', 'comment_max_page']

    # comment_col = ['user_id', 'user_name', 'goods_id', 'goods_name', 'score', 'comment_time',
    #                'comment_content', 'reply_count', 'useful_count', 'goods_color', 'goods_size', 'after_comment', ]

    start_time = 0
    end_time = 0

    def open_spider(self, spider):
        """在爬虫开始时执行一次"""

        print('开始爬取>>>>>>>>>>>>>>>>>>>>>')
        self.start_time = time.time()
        # self.goods_fp = open('./jdSpiderPro/data/dell/goods_info.csv', 'w', newline='', encoding='utf-8')
        # self.goods_writer = csv.DictWriter(self.goods_fp, fieldnames=self.goods_col)
        # self.goods_writer.writeheader()

        self.comment_fp = open('./jdSpiderPro/data/dell/comments_info.csv', 'w', newline='', encoding='utf-8')
        self.comment_writer = csv.DictWriter(self.comment_fp, fieldnames=self.comment_col)
        self.comment_writer.writeheader()

    def process_item(self, item, spider):
        # print('item', item)

        # if item.__class__.__name__ == 'JdcommentItem':
        #     # print('评论的item-------------', item['goods_id'])
        #     # comment_col = list(item.keys())   # 获取到商品评论的列名
        #
        #     self.comment_writer.writerow(item)
        #     # print('商品{}评论写入成功!'.format(item['goods_id']))
        # else:
        #     # print('商品的item>>>>>>>>>>>>>', item['goods_id'])
        #     # goods_col = list(item.keys())     # 获取到商品信息的列名
        #
        #     self.goods_writer.writerow(item)
        #     # print('商品{}信息写入成功!'.format(item['goods_id']))

        self.comment_writer.writerow(item)
        return item

    def close_spider(self, spider):
        """在爬虫结束时执行一次"""

        print('爬取结束>>>>>>>>>>>>>>>>>>>>>')

        # self.goods_fp.close()
        self.comment_fp.close()
        self.end_time = time.time()
        print('耗时: ', (self.end_time - self.start_time))
