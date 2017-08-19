# encoding=utf-8
import re
import os
import datetime
import requests
from lxml import etree
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Sina_spider1.items import InformationItem, TweetItem, FollowItem, RetweetItem

test = False

class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "https://weibo.cn"
    start_urls = [
        5235640836, 5676304901, 5871897095, 2139359753, 5579672076, 2517436943, 5778999829, 2159807003,
        1756807885, 3378940452, 5762793904, 1885080105, 5778836010, 5722737202, 3105589817, 5882481217, 5831264835,
        2717354573, 3637185102, 1934363217, 5336500817, 1431308884, 5818747476, 5073111647, 5398825573, 2501511785,
    ]

    if test:
        start_urls = [3378940452]

    # crawl_ID = set(start_urls)  # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):
        for uid in self.start_urls:
            if uid not in self.finish_ID:
                yield Request(url="https://weibo.cn/%s/info"%uid, callback=self.parse_info)


    def parse_info(self,response):
        """ crawl user profile """
        infoItem = InformationItem()
        selector = Selector(response)
        ID = re.findall('(\d+)/info',response.url)[0]
        self.finish_ID.add(ID)
        text = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())   # 基本信息

        
        nick = re.findall('昵称[：:]?(.*?);'.decode('utf8'),text)
        gender = re.findall('性别[：:]?(.*?);'.decode('utf8'),text)
        region = re.findall('地区[：:]?(.*?);'.decode('utf8'),text)
        intro = re.findall('简介[：:]?(.*?);'.decode('utf8'),text)
        birthday = re.findall('生日[：:]?(.*?);'.decode('utf8'),text)
        authenticity = re.findall('认证[：:]?(.*?);'.decode('utf8'),text)
        vip = re.findall('会员等级[：:]?(.*?);'.decode('utf8'), text)
        url = re.findall('互联网[：:]?(.*?);'.decode('utf8'),text)

        infoItem['_id'] = ID
        if nick and nick[0]:
            infoItem["nick"] = nick[0].replace(u"\xa0", "")
        else:
            infoItem['nick'] = 'NULL'
        if gender and gender[0]:
            infoItem["gender"] = gender[0].replace(u"\xa0", "")
        else:
            infoItem['gender'] = 'NULL'
        if region and region[0]:
            infoItem['region'] = region[0].replace(u"\xa0", "")
        else:
            infoItem['region'] = 'NULL'
        if intro and intro[0]:
            infoItem["introduction"] = intro[0].replace(u"\xa0", "")
        else:
            infoItem['introduction'] = 'NULL'
        if birthday and birthday[0]:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                infoItem["birthday"] = (birthday - datetime.timedelta(hours=8)).strftime('%Y-%m-%d')
            except Exception:
                infoItem['birthday'] = birthday[0]   # 有可能是星座，而非时间
        else:
            infoItem['birthday'] = 'NULL'
        if vip and vip[0]:
            infoItem["vip"] = vip[0].replace(u"\xa0", "")
        else:
            infoItem['vip'] = 'NULL'
        if authenticity and authenticity[0]:
            infoItem["authenticity"] = authenticity[0].replace(u"\xa0", "")
        else:
            infoItem['authenticity'] = 'NULL'
        if url and url[0]:
            infoItem["url"] = url[0]
        else:
            infoItem['url'] = 'NULL'

        
        tags = "https://weibo.cn/account/privacy/tags/?uid=%s&st=ebd927" % ID
        r = requests.get(tags, cookies=response.request.cookies, timeout=5)
        if r.status_code == 200:
            selector = etree.HTML(r.content)
            text = selector.xpath('/html/body/div[@class="c"]/a[contains(@href,"keyword=")]/text()')
            tags = ";".join(text)
            if tags:
                infoItem['tags'] = tags
            else:
                infoItem['tags'] = 'NULL'
        
        

        attgroup = "https://weibo.cn/attgroup/opening?uid=%s" % ID
        r = requests.get(attgroup, cookies=response.request.cookies, timeout=5)
        if r.status_code == 200:
            selector = etree.HTML(r.content)
            text = ";".join(selector.xpath('//body//div[@class="tip2"]/a//text()'))
            if text:
                num_tweets = re.findall('微博\[(\d+)\]'.decode('utf8'), text)
                num_follows = re.findall('关注\[(\d+)\]'.decode('utf8'), text)
                num_fans = re.findall('粉丝\[(\d+)\]'.decode('utf8'), text)
                if num_tweets:
                    infoItem['num_tweets'] = num_tweets[0]
                else:
                    infoItem['num_tweets'] = 'NULL'
                if num_follows:
                    infoItem['num_follows'] = num_follows[0]
                else:
                    infoItem['num_follows'] = 'NULL'
                if num_fans:
                    infoItem['num_fans'] = num_fans[0]
                else:
                    infoItem['num_fans'] = 'NULL'

        yield infoItem
        yield Request(url="https://weibo.cn/%s/profile?filter=1&page=1" % ID, callback=self.parse_tweets, dont_filter=True)
        yield Request(url="https://weibo.cn/%s/follow" % ID, callback=self.parse_follow, dont_filter=True)
        yield Request(url="https://weibo.cn/%s/fans" % ID, callback=self.parse_follow, dont_filter=True)


    def parse_tweets(self,response):
        selector = Selector(response)
        ID = re.findall('(\d+)/profile', response.url)[0]
        tweets = selector.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            tweetItem = TweetItem()
            tid = tweet.xpath('@id').extract_first()
            content = tweet.xpath('div/span[@class="ctt"]/text()').extract()[0]
            hash_mention = tweet.xpath('div/span[@class="ctt"]/a/text()').extract()
            images = tweet.xpath('div/span[@class="ctt"]/a[contains(text(),"组图共")]/@href'.decode('utf8')).extract()
            coordinate = tweet.xpath('div/a/@href').extract()
            likes = re.findall('赞\[(\d+)\]'.decode('utf8'), tweet.extract())
            retweets = re.findall('转发\[(\d+)\]'.decode('utf8'), tweet.extract())
            comments = re.findall('评论\[(\d+)\]'.decode('utf8'), tweet.extract())
            others = tweet.xpath('div/span[@class="ct"]/text()').extract()  # 求时间和使用工具（手机或平台）

            tweetItem['_id'] = ID + "-" + tid
            tweetItem["uid"] = ID
            if hash_mention:
                tmp = " ".join(hash_mention)
                hashtags = re.findall('#\S+#',tmp)
                if hashtags:
                    hashtag = " ".join(hashtags)
                    tweetItem['hashtag'] = hashtag
                else:
                    tweetItem['hashtag'] = 'NULL'
                mentions = re.findall('@\S+',tmp)
                mention = " ".join(mentions)
                if mention:
                    tweetItem['mention'] = mention
                else:
                    tweetItem['mention'] = 'NULL'
            else:
                tweetItem['hashtag'] = 'NULL'
                tweetItem['mention'] = 'NULL'
            if content:
                tweetItem['content'] = content
            else:
                tweetItem['content'] = 'NULL'
            if coordinate:
                coordinate = re.findall('center=([\d.,]+)', coordinate[0])
                if coordinate: 
                    tweetItem['coordinate'] = coordinate[0]
                else:
                    tweetItem['coordinate'] = 'NULL'
            if likes:
                tweetItem['likes'] = likes[0]
            else:
                tweetItem['likes'] = 'NULL'
            if retweets:
                tweetItem['retweets'] = retweets[0]
            else:
                tweetItem['retweets'] = 'NULL'
            if comments:
                tweetItem['comments'] = comments[0]
            else:
                tweetItem['comments'] = 'NULL'
            if others:
                others = others[0].split('来自'.decode('utf8'))
                raw_time = others[0].replace(u"\xa0","")
                post_time = process_time(raw_time)
                tweetItem['post_time'] = post_time
                if len(others) == 2:
                    tweetItem['platform'] = others[1].replace(u"\xa0", "")
                else:
                    tweetItem['platform'] = 'NULL'
            else:
                tweetItem['post_time'] = 'NULL'
                tweetItem['platform'] = 'NULL'
            tweetItem['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield tweetItem
            if retweets > 0:
                # get retweet url
                retweet_url = re.findall(u'https://weibo.cn/repost/[^\"]*',tweet.extract())[0]
                yield Request(url=retweet_url, callback=self.parse_retweets, dont_filter=True)
        # next page
        next_page = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').extract_first()
        if next_page:
            next_url = self.host + next_page
            yield Request(url=next_url, callback=self.parse_tweets, dont_filter=True)


    def parse_follow(self,response):
        selector = Selector(response)
        if "/follow" in response.url:
            ID = re.findall('(\d+)/follow', response.url)[0]
            flag = True
        else:
            ID = re.findall('(\d+)/fans', response.url)[0]
            flag = False
        urls = selector.xpath('//a[text()="关注他" or text()="关注她"]/@href'.decode('utf')).extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        for uid in uids:
            followItem = FollowItem()
            followItem['follower'] = ID if flag else uid
            followItem['followee'] = uid if flag else ID
            yield followItem
            if uid not in self.finish_ID:
                yield Request(url="https://weibo.cn/%s/info" % uid, callback=self.parse_info, dont_filter=True)

        next_page = selector.xpath('//a[text()="下页"]/@href'.decode('utf8')).extract()
        if next_page:
            next_url = self.host + next_page[0]
            yield Request(url=next_url, callback=self.parse_follow, dont_filter=True)


    def parse_retweets(self,response):
        selector = Selector(response)
        retweets = selector.xpath('body/div[@class="c"]')
        ids = os.path.split(response.url)[1]
        origin_id = re.findall('\S+\?',ids)[0]      # 原微博id
        origin_id = origin_id[:-1]
        origin_uid = re.findall('uid=\d+',ids)[0]   # 原用户id
        origin_uid = origin_uid[4:]
        for retweet in retweets:
            retweet_uid_ = retweet.xpath('a/@href').extract_first()
            retweet_uid = re.findall(u'/u/[\d]+',str(retweet_uid_))
            if len(retweet_uid) == 0:
                retweet_uid = re.findall(u'/[\S]+',str(retweet_uid_))
                if len(retweet_uid) == 0:
                    continue
                else:
                    # uid is a string of characters e.g. '/SJTU'
                    retweet_uid = retweet_uid[0]
                    retweet_uid = retweet_uid[1:]
            else:
                # uid is a string of digits e.g. 'u12345'
                retweet_uid = retweet_uid[0]
                retweet_uid = retweet_uid[3:]

            content = retweet.xpath('./text()').extract_first()
            content = content[:-1] if content[-1]==' ' else content
            retweeters = retweet.xpath('a/text()').extract()
            retweet_cascade_len = len(retweeters)

            likes = re.findall(u'\u8d5e\[(\d+)\]', retweet.extract())
            likes = likes[0] 

            others = retweet.xpath('span[@class="ct"]/text()').extract_first()  # post time and platform
            if others:
                others = others.split(u"\u6765\u81ea")
                post_time = others[0]
                post_time = post_time[1:]
                post_time = process_time(post_time)
                if len(others) == 2:
                    platform = others[1]
                else: 
                    platform = None
            else:
                post_time = None
                platform = None

            retweetItem = RetweetItem()
            origin_tweet_id = origin_uid + '-' + 'M_' + origin_id
            retweetItem['origin_tid'] = origin_tweet_id
            retweetItem['uid'] = retweet_uid
            if post_time:
                retweetItem['post_time'] = post_time
            else:
                retweetItem['post_time'] = 'NULL'
            retweetItem['crawl_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            retweetItem['likes'] = likes
            if content:
                retweetItem['content'] = content
            else:
                retweetItem['content'] = 'NULL'
            retweetItem['cascade_length'] = str(retweet_cascade_len)
            if platform:
                retweetItem['platform'] = platform
            else:
                retweetItem['platform'] = 'NULL'

            yield retweetItem

        # get next page
        next_page = selector.xpath('//*[@id="pagelist"]/form/div/a/@href').extract_first()
        if next_page:
            next_url = self.host + next_page
            yield Request(url=next_url, callback=self.parse_retweets, dont_filter=True)


def process_time(raw_time):
    post_time = ''
    if "前".decode('utf8') in raw_time:
        minutes = int(re.findall('\d+',raw_time)[0])
        post_time = (datetime.datetime.now() - datetime.timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M')
    elif "月".decode('utf8') in raw_time and "日".decode('utf8') in raw_time:
        tmp = re.findall('\d+',raw_time)
        [m,d,H,M] = tmp
        post_time = datetime.datetime.now().strftime('%Y-') + '%s-%s'%(m,d) + ' ' + '%s:%s'%(H,M)
    elif "今天".decode('utf8') in raw_time:
        time = re.findall('\d+:\d+',raw_time)[0]
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        post_time = date + ' ' + time
    else:
        post_time = raw_time
    return post_time
