#coding=utf8

class Operation(object):
	"""docstring for Operation"""
	def __init__(self, assetCtrl, asset = 100000):
		super(Operation, self).__init__()
		# 购买方式
		self.assetCtrl = assetCtrl
		# cash
		self.asset = asset
		# 原总资产
		self.baseAsset = self.asset
		# 股票持有数
		self.stockCount = 0
		# 股票购买总价
		self.stockCost = 0
		# 持有详细
		self.detail = []
		# 上次购买价格
		self.lastBuyPrice = None
		# 首次购买的价格
		self.firstBuyPrice = None

	def buy(self, price):
		params = {'price':price, 'money':self.asset, 'baseAsset':self.baseAsset }
		count, cost = self.assetCtrl.getBuyStockCount(params)

		if count == 0:
			print 'ERROR:Operation buy count is 0'

		self.asset = round(self.asset - cost, 3)
		self.stockCount = self.stockCount + count
		self.stockCost = self.stockCost + cost
		
		self.detail.append({'price':float(price), 'cost':float(cost), 'count':count})
		self.lastBuyPrice = float(price)
		if self.firstBuyPrice == None:
			self.firstBuyPrice = float(price)

		if hasattr(self.assetCtrl, 'buyCallBack'):
			self.assetCtrl.buyCallBack()
		
		return True, count, cost

	def sell(self, data):
		if self.stockCount == 0:
			return False, 0, 0, 0, 0, 0

		price = float(data.end)
		
		cost = self.stockCount * price
		totalDifference = cost - self.stockCost

		detail = []
		for x in self.detail:
			percent = (price/x['price']) - 1
			singleDifference = round(percent * x['cost'], 3)
			detail.append({'basePrice':x['price'], 'nowPrice':price, 'cost':x['cost'], 'difference':singleDifference, 'percent':round(percent*100, 2)})

		baseAsset = self.baseAsset
		count = self.stockCount
		self.updateInfo(price)

		if hasattr(self.assetCtrl, 'sellCallBack'):
			self.assetCtrl.sellCallBack()

		return True, baseAsset, totalDifference, detail, count, cost

	def getFirstBuyPrice(self):
		return self.firstBuyPrice

	def getLastBuyPrice(self):
		return self.lastBuyPrice

	def canBuy(self, data):
		# have cash
		if self.asset <= 0:
			return False

		# 买得起至少一手
		if self.asset < 100.0 * float(data.end):
			return False

		return True

	def canSell(self):
		# 有持仓才可以卖
		if self.stockCount > 0:
			return True

		return False

	def checkFar(self, curPrice):
		# 当前股票占已投入资金的收益
		curPrice = float(curPrice)
		return (self.stockCount * curPrice / self.stockCost) - 1

	def checkTotalFar(self, curPrice):
		# 当前股票占原有资金的总收益
		curPrice = float(curPrice)
		diff = self.stockCount * curPrice - self.stockCost

		return (diff / self.baseAsset)

	# 当前股票占原有资金的总收益,返回百分数
	def checkTotalFarP(self, curPrice):
		return self.checkTotalFar(curPrice) * 100
		

	def updateInfo(self, price):
		self.asset = self.baseAsset + self.stockCount * price - self.stockCost
		self.baseAsset = self.asset
		self.clean()

	def clean(self):
		self.firstBuyPrice = None
		self.lastBuyPrice = None
		self.stockCount = 0
		self.stockCost = 0
		self.detail = []

	# 获取股票市值
	def getCost(self, nowPrice):
		return self.stockCount * float(nowPrice)

	# 获取现金资产
	def getAsset(self):
		return self.asset

	# 获取总资产，包括现金和股票市值
	def getTotalAsset(self, nowPrice):
		return self.getAsset() + self.getCost(nowPrice)
