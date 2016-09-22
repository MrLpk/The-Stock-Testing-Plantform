#coding=utf8

from Stock import Stock
import random
from GlobalConfig import GlobalConfig

blackList = []

whiteList = {'510050.SS':'50ETF', '510180.SS':'180ETF'}

indexsBackup = [
			# {'SH000001':u'上证指数'},
			# {'SZ399001':u'深圳成指'},
			{'SH000300':u'沪深300'},
			{'SZ399005':u'中小板指'},
			{'SZ399006':u'创业板指'},
			{'SH000016':u'上证50'},
			{'SH000010':u'上证180'},
			{'SZ399395':u'国证有色'},
			{'SZ399970':u'移动互联'},
			{'SZ399975':u'证券公司'},
			{'SZ399973':u'中证国防'},
			{'SZ399991':u'一带一路'},
			{'SZ399997':u'中证白酒'},
			{'SZ399976':u'CS新能车'},
			{'SZ399958':u'创业成长'},
			{'SZ399959':u'军工指数'},
			{'SZ399393':u'国证地产'},
			{'SZ399440':u'国证钢铁'},
			{'SZ399004':u'深圳100R'}, #150019
			# {'SZ399805':u'互联金融'},
			{'SH000998':u'中证TMT'},
			{'SZ399967':u'中证军工'},
			{'SZ399707':u'CSSW证券'},
			{'SZ399394':u'国证医药'},
			{'SZ399989':u'中证医疗'},
			{'SZ399412':u'国证新能'},
			{'SZ399986':u'中证银行'},
			{'SZ399673':u'创业50'},
			{'SZ399974':u'国企改革'},
			{'SZ399396':u'国证食品'},
			
			# {'SH510300':u'300ETF'},
			# {'SZ159902':u'中小板'},
			# {'SZ159901':u'深100ETF'},
			# {'SZ159915':u'创业板ETF'},
			# {'SH510050':u'50ETF'},
			# {'SZ150153':u'创业板分级B'},
			# {'SZ150244':u'创业B'},
			{'SH600000':u'浦发银行'},
			{'SH600016':u'民生银行'},
			{'SH600036':u'招商银行'},
			{'SH600196':u'复星医药'},
			{'SH600519':u'贵州茅台'},
			{'SH600547':u'山东黄金'},
			{'SH601788':u'光大证券'},
			{'SZ000333':u'美的集团'},
			{'SZ000568':u'泸州老窖'},
			{'SZ000623':u'吉林敖东'},
			{'SZ000776':u'广发证券'},
			{'SZ000858':u'五粮液'},
			{'SZ002038':u'双鹭药业'},
			{'SZ300059':u'东方财富'},
			{'SZ300104':u'乐视网'},
			{'SZ300315':u'掌趣科技'},
			{'SZ000596':u'古井贡酒'},
			{'SH600436':u'片仔癀'},
			{'SZ000623':u'吉林敖东'},
			{'SH603567':u'珍宝岛'},
			{'SH603328':u'依顿电子'},
			# {'':u''},
		]

# 获取indexs里所有代码 
def getCodes():
	codes = []
	for _indexs in getList():
		codes.append(_indexs.keys()[0])
	return codes

def getName(index):
	for _indexs in getList():
		if index in _indexs:
			return _indexs[index]

	print '''NameList getName Error : Can't find %s''' %index
	return None

def getItem(index):
	for _indexs in getList():
		if index in _indexs:
			return _indexs

	print '''NameList getItem Error : Can't find %s''' %index
	return None

def getList():
	cfg = GlobalConfig()
	result = cfg.get('indexs')

	if result is None:
		try:
			result = []
			from XlsHelper import XlsHelper
			table = XlsHelper('NameList.xls').read(index = 0)
			for i in range(table.nrows):
				row = table.row_values(i)
				code = row[0]
				name = row[1]
				result.append({code:name})
			cfg.set('indexs', result)
		except Exception, e:
			print e
			result = indexsBackup
		# finally:
			# result = indexsBackup

	return result


def randomWhite():
	random.randint(0,99)
	pass


