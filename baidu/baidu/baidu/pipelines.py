# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi

from scrapy import log

import MySQLdb.cursors


class BaiduPipeline(object):
    
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                        host='127.0.0.1', 
                        db = 'baidu_tieba',
                        user = 'root',
                        passwd = '',
                        cursorclass = MySQLdb.cursors.DictCursor,
                        charset = 'utf8',
                        use_unicode = False
                )
                
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        return item
        
    def _conditional_insert(self, tx, item):
        tx.execute('insert into post_info (postName, postAuthor, lastReplyTime) values (%s, %s, %s)', (item['post_name'], item['post_author'], item['last_repy_time']))
    
    #def handle_error(self, e):
    #        log.err(e)