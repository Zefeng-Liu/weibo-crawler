# encoding=utf-8

import scrapy

class InformationItem(scrapy.Item):
    """用户个人信息"""
    _id = scrapy.Field()    # 用户id
    nick = scrapy.Field()   # 昵称
    authenticity = scrapy.Field()   # 认证信息
    gender = scrapy.Field() # 性别
    region = scrapy.Field() # 地区
    birthday = scrapy.Field()   # 生日
    introduction = scrapy.Field()   # 简介
    vip = scrapy.Field()    # 会员等级
    tags = scrapy.Field()   # 标签
    num_tweets = scrapy.Field() # 微博数
    num_follows = scrapy.Field()    # 关注数
    num_fans = scrapy.Field()   # 粉丝数
    url = scrapy.Field()    # 首页链接


class TweetItem(scrapy.Item):
    """微博信息"""
    _id = scrapy.Field()    # 微博id
    uid = scrapy.Field()    # 用户id
    hashtag = scrapy.Field()    # 主题
    mention = scrapy.Field()    # 艾特
    content = scrapy.Field()    # 内容
    post_time = scrapy.Field()  # 发表时间
    crawl_time = scrapy.Field() # 抓取时间
    coordinate = scrapy.Field() # 定位坐标
    platform = scrapy.Field()   # 发表平台
    likes = scrapy.Field()  # 点赞数
    comments = scrapy.Field()   # 评论数
    retweets = scrapy.Field()   # 转发数

class RetweetItem(scrapy.Item):
    """转发信息"""
    origin_tid = scrapy.Field() # 原微博id
    uid = scrapy.Field()    # 转发者的id
    content = scrapy.Field()    # 转发内容
    post_time = scrapy.Field()  # 转发时间
    crawl_time = scrapy.Field() # 爬取时间
    likes = scrapy.Field()  # 转发点赞数
    cascade_length = scrapy.Field() # 转发链长度
    platform = scrapy.Field()   # 转发平台

class FollowItem(scrapy.Item):
    """
    关注关系
    follower follows followee
    """
    follower = scrapy.Field()   # 关注者
    followee = scrapy.Field()   # 被关注者
