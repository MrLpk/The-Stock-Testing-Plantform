#coding=utf-8
'''
Created on 2014年2月18日

@author: DY
'''
import MySQLdb

HOST        = 'localhost'
USERNAME    = 'root'
PASSWORD    = 'root'
DBNAME      = 'nba'
PORT        = 3306

class MySQLLocal(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def connect(self):
        try:
            self.conn=MySQLdb.connect(host=HOST,user=USERNAME,passwd=PASSWORD,db=DBNAME,port=PORT)
            self.c=self.conn.cursor()
            
            self.c.execute('set names utf8')

        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            
    def close(self):
        self.conn.close()
        self.c.close()
    
    def insertDB(self, sql):
        self.connect()
        try:
            print 'execute --', sql
            self.c.execute(sql.encode('utf-8'))
            self.conn.commit()
            self.close()
            
            
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
    def selectDB(self, sql):
        self.connect()
        try:
            print 'select ---', sql
            self.c.execute(sql.encode('utf-8'))
            msgs = list(self.c.fetchall())
            self.close()
        
            return msgs
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
        