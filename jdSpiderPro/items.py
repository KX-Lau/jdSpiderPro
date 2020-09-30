import scrapy


class JdspiderproItem(scrapy.Item):
    goods_id = scrapy.Field()           # 商品id
    goods_name = scrapy.Field()         # 商品名
    goods_shop = scrapy.Field()         # 店铺
    comment_count = scrapy.Field()      # 评论总数
    comment_max_page = scrapy.Field()      # 评论最大页数
    comment_cur_page = scrapy.Field()      # 评论当前总数
    score1_count = scrapy.Field()       # 1星评论数
    score2_count = scrapy.Field()       # 2星评论数
    score3_count = scrapy.Field()       # 3星评论数
    score4_count = scrapy.Field()       # 4星评论数
    score5_count = scrapy.Field()       # 5星评论数


class JdcommentItem(scrapy.Item):
    user_id = scrapy.Field()            # 用户id
    user_name = scrapy.Field()          # 用户昵称
    goods_id = scrapy.Field()           # 商品id
    goods_name = scrapy.Field()         # 商品名
    goods_shop = scrapy.Field()         # 店铺
    comment_count = scrapy.Field()      # 评论总数
    comment_max_page = scrapy.Field()   # 评论最大页数
    comment_cur_page = scrapy.Field()   # 评论当前总数
    score1_count = scrapy.Field()       # 1星评论数
    score2_count = scrapy.Field()       # 2星评论数
    score3_count = scrapy.Field()       # 3星评论数
    score4_count = scrapy.Field()       # 4星评论数
    score5_count = scrapy.Field()       # 5星评论数
    score = scrapy.Field()              # 评分
    comment_time = scrapy.Field()       # 评论时间
    comment_content = scrapy.Field()    # 评论内容
    reply_count = scrapy.Field()        # 回复数
    useful_count = scrapy.Field()       # 认为有用数
    goods_color = scrapy.Field()        # 商品颜色
    goods_size = scrapy.Field()         # 商品版本
    after_comment = scrapy.Field()      # 追加评论
