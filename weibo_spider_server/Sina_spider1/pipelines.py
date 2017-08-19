# encoding=utf-8
from items import InformationItem, TweetItem, FollowItem, RetweetItem
import MySQLdb
import datetime

test = False

DBNAME = 'weibo0807'
PASSWD = 'Admin4747!'

class MySQLPipeline(object):
    def __init__(self):
        if test:
            time = datetime.datetime.now().strftime('%m-%d %H-%M')
            self.user_test_log = open('./testlog/%s sql user test log.txt'%time,'w')
            self.tweet_test_log = open('./testlog/%s sql tweet test log.txt'%time,'w')
            self.retweet_test_log = open('./testlog/%s sql retweet test log.txt'%time,'w')
            self.follow_test_log = open('./testlog/%s sql follow test log.txt'%time,'w')
        self.count = 0
        self.test_count = 0
        self.conn = MySQLdb.connect(host='localhost',
                                    port=3306,
                                    user='root',
                                    passwd=PASSWD,
                                    db=DBNAME,
                                    charset='utf8',)
        self.cur = self.conn.cursor()

    def __del__(self):
        if test:
            self.user_test_log.close()
            self.tweet_test_log.close()
            self.retweet_test_log.close()
            self.follow_test_log.close()

    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            # assemble sql command
            sql_cmd = ''
            sql_cmd += str('INSERT INTO users values(')
            sql_cmd += str('\'%s\','%item['_id'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['nick'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['gender'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['region'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['birthday'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['introduction'].encode('utf8').replace('\'','\\\''))
            sql_cmd += str('\'%s\','%item['authenticity'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['vip'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['tags'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['num_tweets'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['num_follows'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['num_fans'].encode('utf8'))
            sql_cmd += str('\'%s\');'%item['url'].encode('utf8'))
            if test:
                self.user_test_log.write(sql_cmd+'\n')

        elif isinstance(item, TweetItem):
            # assemble sql command
            sql_cmd = ''
            sql_cmd += str('INSERT INTO tweets values(')
            sql_cmd += str('\'%s\','%item['_id'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['uid'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['hashtag'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['mention'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['content'].encode('utf8').replace('\'','\\\''))
            sql_cmd += str('\'%s\','%item['post_time'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['crawl_time'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['coordinate'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['platform'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['likes'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['comments'].encode('utf8'))
            sql_cmd += str('\'%s\');'%item['retweets'].encode('utf8'))
            if test:
                self.tweet_test_log.write(sql_cmd+'\n')

        elif isinstance(item, RetweetItem):
            # assemble sql command
            sql_cmd = ''
            sql_cmd += str('INSERT INTO retweets values(')
            sql_cmd += str('\'%s\','%item['origin_tid'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['uid'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['content'].encode('utf8').replace('\'','\\\''))
            sql_cmd += str('\'%s\','%item['post_time'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['crawl_time'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['platform'].encode('utf8'))
            sql_cmd += str('\'%s\','%item['likes'].encode('utf8'))
            sql_cmd += str('\'%s\');'%item['cascade_length'].encode('utf8'))
            if test:
                self.retweet_test_log.write(sql_cmd+'\n')

        elif isinstance(item, FollowItem):
            # assemble sql comand
            sql_cmd = ''
            sql_cmd += str('INSERT INTO follows values(')
            sql_cmd += str('\'%s\','%item['follower'].encode('utf8'))
            sql_cmd += str('\'%s\');'%item['followee'].encode('utf8'))
            if test:
                self.follow_test_log.write(sql_cmd+'\n')
        
        if not test:
            try:
                self.cur.execute(sql_cmd)
                self.conn.commit()
                self.count += 1
            except Exception, e:
                print repr(e)

        else:
            self.test_count += 1

        # 在Java开发中，Dao连接会对内存溢出，需要定时断开重连，这里不清楚是否需要，先加上了
        if self.count > 1000:
            self.reconnect()

        return item

    def reconnect(self):
        self.count = 0
        self.cur.close()
        self.conn.close()
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd=PASSWD,
            db=DBNAME,
            charset='utf8',)
        self.cur = self.conn.cursor()






"""
class MongoDBPipleline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Follows = db["Follows"]
        self.Fans = db["Fans"]

    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, FollowsItem):
            followsItems = dict(item)
            follows = followsItems.pop("follows")
            for i in range(len(follows)):
                followsItems[str(i + 1)] = follows[i]
            try:
                self.Follows.insert(followsItems)
            except Exception:
                pass
        elif isinstance(item, FansItem):
            fansItems = dict(item)
            fans = fansItems.pop("fans")
            for i in range(len(fans)):
                fansItems[str(i + 1)] = fans[i]
            try:
                self.Fans.insert(fansItems)
            except Exception:
                pass
        return item
"""