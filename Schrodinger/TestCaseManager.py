#coding=utf8

from CaseFrame import CaseFrame
from Turtle import Turtle
from Elephant import Elephant
from B1 import B1
from B2 import B2
from B3 import B3
from S1 import S1
from S2 import S2
from S3 import S3
from Stock import Stock
import StateDefine as SD
import NameList
from CaseManager import CaseManager
import StockMathTool as SMT
import MathTool

class TCMctrl(object):
	"""docstring for TCMctrl"""
	def __init__(self):
		super(TCMctrl, self).__init__()
		# self.start()
		# self.outPutStockData('SZ399006') #创业板指
		# self.outPutStockData('SH000016') #上证50
		# self.outPutStockData('SZ399986') #中证银行
		# self.outPutStockData('SZ399997') #中证白酒
		# self.outPutStockData('SH600036') #招商银行
		self.outPutStockData('SH000300') #沪深300
		
		# self.outPutStockmeanFR()

	# 输出股票数据
	def outPutStockData(self, code):
		s = Stock(atr = ['20'], ma = ['20'], index = code)


		# s = Stock(atr = ['20'], ma = ['20'])
		# s.setCode(code)
		# s.setFunc({'func':self.sss, 'funcName':'sss'})
		# s.create()

		s.outPutXML()

	def sss(self, parmas):
		datas = parmas['datas']
		obj = parmas['obj']
		# 最后一个数据
		data = datas[-1]
		curState = obj.getCurState()
		if curState == SD.STOCK_NOTHING or curState == SD.STOCK_SELL:
			result, _ = SMT.compareMaBuy(data, data)

			if hasattr(obj, 'lowestPrice'):
				if (not obj.lowestPrice is None) and obj.lowestPrice > float(data.end):
					obj.lowestPrice = float(data.end)
			if result:
				# 当天符合条件的标记为购买
				obj.setCurState(SD.STOCK_BUY)
				# 记录跌破均线以来的最大跌幅
				if hasattr(obj, 'point'):
					if (not obj.point is None):
						diff = MathTool.increase(obj.point, obj.lowestPrice, True)
						if hasattr(obj, ''):
							pass


				obj.point = None
				obj.lowestPrice = None
			else:
				# 卖出第二天没有重新购买的标记为NOTHING
				obj.setCurState(SD.STOCK_NOTHING)
		elif curState == SD.STOCK_BUY or curState == SD.STOCK_HOLD:
			result, point = SMT.compareMaSell(data, data)
			if result:
				# 当天符合条件的标记为卖出
				obj.setCurState(SD.STOCK_SELL)
				# 记录跌破均线后当天的价格
				obj.point = point
				obj.lowestPrice = point
			else:
				# 购买第二天没有卖出的标记为持有
				obj.setCurState(SD.STOCK_HOLD)

	def outPutStockmeanFR(self):
		# 波动幅度排序
		indexs = NameList.getList()

		array = []
		for _item in indexs:
			_key = _item.keys()[0]
			s = Stock(atr = ['20'], ma = ['20'], index = _key)
			array.append({'code':_key, 'mfr':s.getMeanFR(20)})

		array.sort(key = lambda x:x['mfr'], reverse = True)

		for _item in array:
			print _item['code'], NameList.getName(_item['code']), _item['mfr']


	def start(self):
		# indexs = [
		# 	{'SZ159915':u'创业板ETF'},
		# 	{'SH510300':u'300ETF'},
		# 	{'SH510050':u'50ETF'},
		# 	{'SZ159902':u'中小板'},
		# 	{'SZ159901':u'深100ETF'},
		# 	{'SZ150153':u'创业板分级B'},
		# ]

		indexs = NameList.getList()
		# indexs = [NameList.getItem('SH510050')]
		# indexs = [NameList.getItem('SH600036')]
		mas = ['5', '10', '20', '60']
		# mas = ['20']
		record = []

		for _index, _item in enumerate(indexs):
			record.append([])
			for _ma in mas:
				tcm = CaseManager(_item.keys()[0], _ma, False)
				result = tcm.run()
				result['ma'] = _ma
				result['name'] = _item.values()[0]
				record[_index].append(result)
			record[_index].sort(key = lambda result:result['cagr'], reverse = True)
			# break
		record.sort(key = lambda x:x[0]['avgFluctuateRange'], reverse = True)

		for x in record:
			for y in x:
				lll = ''
				for key in y.keys():
					lll = lll + ' %s : %s' %(key, y[key])
				print lll
			print '\n\n'
		