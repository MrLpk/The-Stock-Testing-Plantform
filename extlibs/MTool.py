#-*- coding: utf-8 -*-
'''
Created on 2013-8-27

@author: liaopengkai
'''
import urllib2
import os
import json
import re
import time
from datetime import datetime

class MTool(object):
    def __init__(self):
        super(MTool, self).__init__()
        self.isSave = True

    def isNum(self, tempStr):
        """判断字符串是否为数字，整型和浮点型皆适用"""
        try:
            float(tempStr)
            return True
        except Exception:
            return False
        
    def save(self, filename, contents, reNew = True, path = '', path2 = ''):
        '''保存文件，参数:文件名、内容、是否覆盖更新、路径'''
        # if not self.isSave:
        #     return

        if not path == '':
            if not os.path.isdir(path):
                os.mkdir(path)
            if not os.path.isdir(path + path2):
                os.mkdir(path + path2)
            filename = path + path2 + filename
        if os.path.exists(filename):
            if not reNew:
                print 'You already have ' + filename
                return
        fh = open(filename, 'w') 
        fh.write(contents) 
        fh.close() 
#         print filename
        print 'Save '+filename+' success...'
        
    def download(self, url, path = '', reNew = True):
        '''下载并保存'''
        
        temp = url.split('/')
        name = temp[len(temp)-1]
        
        if path != '':
            filename = path + name
        if os.path.exists(filename):
            if not reNew:
                print 'You already have ' + filename
                return
            
        result = urllib2.urlopen(url).read()
        self.save(name, result, reNew, path)

    # 将一个时间戳转换成一个UTC时区(0时区)的struct_time
    def gmtime(self, _t):
        return time.gmtime(_t)
    # 将一个时间戳转换成一个当前时区的struct_time
    def localtime(self, _t):
        return time.localtime(_t)

    def getTime(self, _str = '%Y-%m-%d %H:%M:%S', _t = time.localtime()):
        t = time.strftime(_str, _t)
        return t

    def sumTime(self, _hour = 0, _min = 0, _sec = 0, _times = 0, needDt = False):
        t = _times
        if _times == 0:
            t = time.time()

        t += (3600*_hour + 60*_min + _sec)
        if needDt:
            return t
        else:
            return time.localtime(t)

    def subTime(self, _hour = 0, _min = 0, _sec = 0, _times = 0, needDt = False):
        t = _times
        if _times == 0:
            t = time.time()

        t -= (3600*_hour + 60*_min + _sec)
        if needDt:
            return t
        else:
            return time.localtime(t)

    def makeTime(self, _year, _month, _day, _hour = 0, _min = 0, _sec = 0, needPrint = False):
        ''' 返回时间戳形式 '''
        _times = datetime.today()
        _times = _times.replace(int(_year), int(_month), int(_day), int(_hour), int(_min), int(_sec))
        if needPrint:
            print _times
        _times = time.mktime(_times.timetuple())
        if needPrint:
            print _times
        return _times

    def getToday(self):
        ''' 返回时间戳形式 '''
        _times = datetime.today()
        _times = time.mktime(_times.timetuple())
        
        return _times
    
    def int2Str(self, _num):
        ''' 如果数字小于10，会返回0X样式字符串 '''
        if _num < 10:
            _num = '0%d' %_num
    
        return str(_num)

if __name__ == '__main__':
    m = MTool()
    m.makeTime(1990, 3, 3)

    
    
    
    
    
    