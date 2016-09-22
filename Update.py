#coding=utf-8

import Path
from Download import Download
import NameList as NL

download = Download()

def updateHistory():
	print 'Updateing history ...'
	array = NL.getCodes()
	download.downHistory(array)
	print 'Update history success ...'
	raw_input()

if __name__ == '__main__':
	updateHistory()