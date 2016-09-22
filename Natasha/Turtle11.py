#coding=utf8

from BaseData import BaseData
import math
''' Turtle '''

class Turtle(object):
	"""docstring for Turtle"""
	def __init__(self, original = 0, all = 0, nKey = '0'):
		super(Turtle, self).__init__()
		self.maxUnit = 5 # 最大仓位
		self.unitCount = 0 #当前仓位
		self.original = original # 总量
		self.all = all
		self.nKey = nKey # atr key
		self.stockCount = 0 # 购买数量

	def getIntroduce(self):
		return '海龟买法'

	# 计算当前需要买多少手
	def getBuyStockCount(self, data):
		n = data.atr[self.nKey]
		count = self.original * 0.01 / n
		count = self.fixStockCount(count)

		return count

	''' You must use self.check(data) before getVolume '''
	def getVolume(self, data):
		if self.nKey == None:
			print 'error : you have not init nKey'

		self.unitCount = self.unitCount + 1
		price = float(data.end)
		self.stockCount = self.getBuyStockCount(data)
		num = round(self.stockCount * price, 3)

		if self.stockCount == 0:
			return 1, 2, 3

		# print '-'*40
		# print self.original
		# print n
		# print price
		# print num

		# 资金不足时，计算最少可以买多少手
		if self.all < num:
			count = self.all / price
			self.stockCount = self.fixStockCount(count)
			num = round(self.stockCount * price, 3)

		self.all = self.all - num
		return num

	# 把数字修正为100的倍数，不足100返回100
	def fixStockCount(self, stockCount):
		stockCount = int(math.floor(stockCount))

		if stockCount <= 100:
			return 100

		num = stockCount % 100

		if num == 0:
			return stockCount
		else:
			return stockCount - num

	def inCome(self, num):
		self.clean()
		self.all = self.original + num
		self.original = self.all

	def check(self, data):
		''' 仓位已满 '''
		if self.unitCount >= self.maxUnit:
			return False

		''' not cash '''
		if self.all <= 0:
			return False

		''' 太贵一手都买不起 '''
		if 100.0 * float(data.end) > self.all:
			return False

		if self.getBuyStockCount(data) == 0:
			print data.end
			print self.all
			return 1,2,3

			# return False

		return True

	def clean(self):
		self.unitCount = 0
		self.stockCount = 0