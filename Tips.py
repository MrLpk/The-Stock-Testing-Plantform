#coding=utf8
import Path
import NameList
from Stock import Stock
import Relation as RLN
from StockConfig import StockConfig
from GlobalConfig import GlobalConfig
from XlsHelper import XlsHelper
import StockMathTool as SMT
import StateDefine as SD
import MathTool

class Tips(object):
	"""docstring for Tips"""
	def __init__(self):
		super(Tips, self).__init__()
		GlobalConfig().set('mode', 'Hobbit')

	def run(self):
		# 获取列表
		# indexs = [{'SZ399006':u'创业板指'}]
		indexs = NameList.getList()
		# 计算结果
		suggest = self.result(indexs)
		# 输出到xls
		self.outPutXls(suggest)
		# self.cfg.save()

	def result(self, indexs):
		record = self.getRecordData()

		holdSuggest = []
		buySuggest = []
		sellSuggest = []
		watchSuggest = []
		other = []
		for _item in indexs:
			_key = _item.keys()[0]
			stock = Stock(atr = ['20'], ma = ['20'], index = _key)
			data = stock.stockDatas[-1]
			if _key in record:
				# 已持有部分
				isSell, suggestDict = self.getSellSuggest(data, _key, stock, record[_key])
				if isSell:
					sellSuggest.append(suggestDict)
				else:
					holdSuggest.append(suggestDict)
			else:
				isBuy, suggestDict = self.getBuySuggest(data, _key, stock)
				# if _key == 'SZ000333':
				# 	print 'isbuy',isBuy
				if isBuy:
					if stock.getCurState() == SD.STOCK_BUY:
						buySuggest.append(suggestDict)
					else:
						watchSuggest.append(suggestDict)
				else:
					other.append(suggestDict)

		sellSuggest.sort(key = lambda x:x['percent'], reverse = True)
		holdSuggest.sort(key = lambda x:x['percent'], reverse = True)
		buySuggest.sort(key = lambda x:x['wir'], reverse = True)
		watchSuggest.sort(key = lambda x:x['wir'], reverse = True)
		other.sort(key = lambda x:x['percent'], reverse = True)

		suggest = [
			{'title':'Sell', 'array':sellSuggest, 'relation':False},
			{'title':'Buy', 'array':buySuggest, 'relation':True},
			{'title':'Hold', 'array':holdSuggest, 'relation':False},
			{'title':'Watch', 'array':watchSuggest, 'relation':True},
			{'title':'other', 'array':other, 'relation':False},
		]

		return suggest
		

	def getSellSuggest(self, data, _key, stock, price = None):
		result, point = SMT.compareMaSell(data, data, price)
		percent = MathTool.increase(point, data.end, True)
		suggestDict = self.makeDict(data, _key, stock, point, percent)
		return result, suggestDict

	def getBuySuggest(self, data, _key, stock):
		result, point = None, None
		if stock.getCurState() == SD.STOCK_BUY or stock.getCurState() == SD.STOCK_HOLD:
			result = True
			point = SMT.getMa(data)
		else:
			result, point = SMT.compareMaBuy(data, data)
		# if _key == 'SZ000333':
		# 	print stock.getCurState()
		# 	print result, data.end, point
		# 	raw_input()
		percent = MathTool.increase(point, data.end, True)
		suggestDict = self.makeDict(data, _key, stock, point, percent)
		return result, suggestDict

	def getSuggest(self, data, _key, stock, point):
		percent = MathTool.increase(point, data.end, True)
		suggestDict = self.makeDict(data, _key, stock, point, percent)
		
		return float(data.end) > point, suggestDict

	def makeDict(self, data, code, stock, point, percent):
		dictionary = {
			'date':data.getDate(), 		# 日期
			'code':code, 				# 代码
			'mfr':stock.getMeanFR(60), 	# 60日波幅
			'price':float(data.end),	# 当前收盘价
			'operatePrice':point,		# 操作价
			'percent':percent,			# 距离操作价百分比
			'atr':data.atr['20'],		# ATR
			'ir':data.getIRP(20),  		# X日价格增长率
			'wir':data.getWIRP(),		# 20、40日加权价格增长率
		}
		return dictionary

	def outPutXls(self, suggests):
		tables = []
		datas = []
		for _suggest in suggests:
			datas.append([_suggest['title']])

			for _item in _suggest['array']:
				datas.append([_item['date'], _item['code'], NameList.getName(_item['code']), _item['wir'], _item['price'], _item['operatePrice'], str(_item['percent'])+'%'])

				if _suggest['relation']:
					funds = RLN.getRelation(_item['code'])
					for _fund in funds:
						datas.append(['', _fund['code'], _fund['name']])

			datas.append([''])

		tables.append({'name':'Stock', 'data':datas})
		XlsHelper('result.xls').create(tables)


	def getRecordData(self):
		result = {}
		try:
			table = XlsHelper('record.xlsx').read(index = 0)
			for i in range(table.nrows):
				row = table.row_values(i)
				code = row[0]
				price = None
				if len(row) >= 2:
					price = row[1]
				if code in result:
					print 'The Same code :', code
				else:
					result[code] = price
		except Exception, e:
			print e
		finally:
			return result

if __name__ == '__main__':
	t = Tips()
	t.run()

