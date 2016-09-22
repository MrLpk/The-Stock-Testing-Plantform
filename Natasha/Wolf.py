#coding=utf8
import math

class Wolf(object):
	"""docstring for Wolf"""
	def __init__(self, base = 1000, gain = 0.02, tax = 0):
		super(Wolf, self).__init__()
		self.tax = tax
		self.base = base #定投基础
		self.gain = gain #定投增长

	def getIntroduce(self):
		return '定增买法'

	def setBase(self, base):
		self.base = base

	def getBase(self):
		return self.base

	# 计算当前需要买多少手
	def getBuyStockCount(self, price, rate, totalValue, usingMoney):
		if not isinstance(price, float):
			price = float(price.end)
		if price <= 0:
			raise TypeError('Price <= 0')

		# 当前回合需要达到的总价值
		totalValue = round(totalValue * (1 + self.gain) + self.base, 2)
		# 需操作的金额
		cost = totalValue - price * rate
		rate = (cost / price)

		return rate, round(cost, 2), totalValue

	# def getBuyStockCount(self, price, rate, totalValue, usingMoney):
	# 	if not isinstance(price, float):
	# 		price = float(price.end)
	# 	if price <= 0:
	# 		raise TypeError('Price <= 0')

	# 	# 当前回合需要达到的总价值
	# 	totalValue = round(totalValue * (1 + self.gain) + self.base, 2)
	# 	# 需操作的金额
	# 	# print 'aaa', totalValue, rate
	# 	cost = totalValue - price * rate
	# 	rate = (cost / price)
	# 	# print cost, usingMoney
	# 	# 转换为数量
	# 	count = 0#self.fixStockCount(abs(cost / price))

	# 	# if cost < 0:
	# 	# 	count = count * -1.0

	# 	# print totalValue, count, cost, price
	# 	# return count, count * price * (1 + self.tax), totalValue
	# 	# print totalValue, cost, price

	# 	return rate, round(cost, 2), totalValue

	# 把数字修正为100的倍数，不足100返回100,
	# 向上取
	def fixStockCount(self, stockCount):
		stockCount = int(math.floor(stockCount))

		if stockCount < 100:
			return 100

		num = stockCount % 100

		if num == 0:
			return stockCount
		else:
			return stockCount - num + 100

if __name__ == '__main__':
		# 3.747,
		# 4.441,

		# 10000  2600

		# 10000*1.01+10000=20100-11546.6
		# 10000*1.01
	w = Wolf(base=1000)
	datas = [
		9.19,
		9.68,
		10.25,
		9.42,
		10.64,
		11.81,
		11.37,
		10.29,
		10.99,
		10.08,
		9.12,
		8.46,
		8.45,
		9.13,
		9.21,
		7.91,
		8.52,
		8.38,
		7.29,
		6.48,
		7.35,
		6.78,
		6.85,
		7.34,
		7.26,
	]


	# datas =[
	# 	3.747,
	# 	4.441,
	# 	4.611,
	# 	4.277,
	# 	3.663,
	# 	3.205,
	# 	3.052,
	# 	3.382,
	# 	3.445,
	# 	3.539,
	# 	2.737,
	# 	2.687,
	# 	3.003,
	# 	]
	holdCount = 0

	usingMoney = 0
	totalValue = 0
	for index, price in enumerate(datas):
		_count, _cost, totalValue = w.getBuyStockCount(holdCount, price, totalValue)

		holdCount = holdCount + _count
		usingMoney = usingMoney + _cost
		nowCost = round(holdCount * price, 2)
		# print index+1, price, _count, _cost, usingMoney, totalValue
		print index+1, price, totalValue, usingMoney, nowCost, round(((nowCost/usingMoney)-1)*100, 2)
		if index == 16:
			# break
			pass


		