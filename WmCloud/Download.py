#coding=utf8
from dataapiclient import Client
import StateDefine as SD
from StockConfig import StockConfig

class Download(object):
	"""docstring for Download"""
	def __init__(self):
		super(Download, self).__init__()
		token = 'b6a5eded39d16731278aa4646ec96128304f0ccab0850bbdacebcdcada4dbb7f'
		self.client = Client()
		self.client.init(token)
		self.cfg = StockConfig()
		# self.name = 'Smaug'
		self.name = 'Hobbit'

	# 下载历史数据

	# eg:stocks = [600519, ..., 159915]
	def downHistory(self, stocks, stockType = 0):
		date = '20151201'
		if self.name == 'Smaug':
			date = '20050101'
			
		urls = [
				# '/api/market/getMktEqud.json?field=&beginDate=20050101&endDate=&secID=&ticker=%s&isOpen=1',
				# '/api/market/getMktFundd.json?field=&beginDate=20050101&endDate=&secID=&ticker=%s&tradeDate=',
				# '/api/market/getMktIdxd.json?field=&beginDate=20050101&endDate=&indexID=&ticker=%s&tradeDate=',
				'/api/market/getMktEqud.json?field=&beginDate=%s&endDate=&secID=&ticker=%s&isOpen=1',
				'/api/market/getMktFundd.json?field=&beginDate=%s&endDate=&secID=&ticker=%s&tradeDate=',
				'/api/market/getMktIdxd.json?field=&beginDate=%s&endDate=&indexID=&ticker=%s&tradeDate=',
		]
		newStockTypes = []
		
		for _stock in stocks:
			stockType = self.getTypeByCode(_stock)
			url = urls[stockType] %(date, self.initCode(_stock))
			# print url
			result = self.down(url)
			if result['retCode'] == -1:
				for x in xrange(1,len(urls)):
					stockType = x
					url = urls[stockType] %(date, self.initCode(_stock))
					result = self.down(url)
					if result['retCode'] == 1:
						newStockTypes.append({_stock:stockType})
						break
			# print result['data']
			# print result
			content = ''
			if stockType == SD.IDX:
				content = self.handleIdxAsStock(result['data'])
			else:
				content = self.handleAsStock(result['data'])

			# if _stock == 'SH600036':
			# 	print content
			# 	return
			
			self.save('%s/%s.txt' %(self.name, _stock), content)
		self.updateType(newStockTypes)

	# 序列化股票代码
	# SH6000000 --> 6000000
	def initCode(self, code):
		code = str(code)
		if len(code) == 8:
			return code[2:]
		elif len(code) == 6:
			return code
		raise 'Change Code Error : ' + code

	# 根据证券代码返回股票类型
	# -1:无记录;0:股票;1:基金;2:指数
	def getTypeByCode(self, code):
		result = self.cfg.getTypeByCode(code)
		return result if not result == -1 else 0 

	def updateType(self, array):
		self.cfg.update(array)

	# 根据url下载内容 
	def down(self, url):
		self.url = url
		# print url
		code, result = self.client.getData(url)
		if code == 200:
			return eval(result)
		else:
			print code
			print result

	# 将数据处理成股票数据格式
	# 前复权
	def handleAsStock(self, data):
		result = ''
		for _data in data:
			# print _data
			accumAdjFactor = _data['accumAdjFactor'] # 前复权因子
			date = self.formatDate(_data['tradeDate'])
			openPrice = round(_data['openPrice'] * accumAdjFactor, 3)
			highestPrice = round(_data['highestPrice'] * accumAdjFactor, 3)
			lowestPrice = round(_data['lowestPrice'] * accumAdjFactor, 3)
			closePrice = round(_data['closePrice'] * accumAdjFactor, 3)
			turnoverVol = round(_data['turnoverVol'], 2) # 成交量
			turnoverValue = round(_data['turnoverValue'], 2) # 成交金额
			
			result = result + '%s,%s,%s,%s,%s,%s,%s\n' %(date, openPrice, highestPrice, lowestPrice, closePrice, turnoverVol, turnoverValue)

		return result

	# 将指数的数据处理成股票数据格式
	def handleIdxAsStock(self, data):
		result = ''
		for _data in data:
			try:
				date = self.formatDate(_data['tradeDate'])
				openPrice = round(_data['openIndex'], 3)
				highestPrice = round(_data['highestIndex'], 3)
				lowestPrice = round(_data['lowestIndex'], 3)
				closePrice = round(_data['closeIndex'], 3)
				turnoverVol = round(_data['turnoverVol'], 2) # 成交量
				turnoverValue = round(_data['turnoverValue'], 2) # 成交金额
				
				result = result + '%s,%s,%s,%s,%s,%s,%s\n' %(date, openPrice, highestPrice, lowestPrice, closePrice, turnoverVol, turnoverValue)
			except Exception, e:
				print self.url
				print _data
				raise e
			

		return result
	# YYYY-MM-DD --> YYYY/MM/DD
	def formatDate(self, date):
		date = date.split('-')
		return '%s/%s/%s' %(date[0], date[1], date[2])

	def save(self, path, content):
		fh = open(path, 'w') 
		fh.write(content) 
		fh.close() 

		print 'Save %s success...' %path

