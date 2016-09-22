#coding=utf8

from BaseCase import BaseCase
from Stock import Stock
import NameList as NL
from BaseData import BaseData
from OperationMgr import OperationMgr
from Turtle import Turtle
from Operation import Operation

class Case2(BaseCase):
	"""docstring for Case2"""
	def __init__(self):
		super(Case2, self).__init__()
		# key
		self.index = 'sh001'

		# tutle
		self.tutle = Turtle()
		self.tutle.original = 100000
		self.tutle.all = 100000
		self.tutle.nKey = '20'
		self.inputLock = False

	def introduce(self):
		self.fileName = 'Case2'
		self.l.log('Case2...')

	def initStock(self):
		self.sh = Stock(atr = [int(self.tutle.nKey)], tomax = [20], tomin = [20])
		self.sh.create('SH000001')
		self.l.log('data count : ' + str(len(self.sh.stockDatas)))

	def analysis(self):
		self.opMgr.regStock(self.index, self.tutle)
		# self.inputLock = True # 控制分步执行
		self.setBeginTime(1991, 1, 1)
		self.highestPrice = 0 # 最高购入点
		self.lastBuyPoint = 0
		# self.aaa = 0
		for index, data in enumerate(self.sh.stockDatas):
			if index == 0:
				continue

			if not self.checkTime(data.timestamp):
				continue

			lastData = self.sh.stockDatas[index-1]

			result, volume = self.buy(data, lastData)
			if result:
				self.recordBuy(data, volume)
				# print 'before', self.highestPrice
				self.updateHighestPrice(data.end, True)
				# print 'after', self.highestPrice
				if self.inputLock:
					raw_input()
				continue

			result, volume = self.sell(data, lastData)
			if result:
				if volume >= 0:
					self.recordSellWin(data, self.opMgr.payWayCache[self.index].all)
				else:
					self.recordSellLose(data, self.opMgr.payWayCache[self.index].all)

				if self.inputLock:
					raw_input()
					

			self.updateHighestPrice(data.end)

			if data.y == '1994' and data.m == '08' and data.d == '10':
				raw_input()

		self.l.log( 'Programe Finish...')
		self.l.log( 'Left Money:%s' %self.opMgr.payWayCache[self.index].all)
			
	def updateHighestPrice(self, price, replace = False):
		if replace:
			self.highestPrice = float(price)
			# print 'update replace', price
			return

		if float(price) > self.highestPrice:
			self.highestPrice = float(price)
			# print 'update', price
	def buy(self, data, lastData):
		flag = False
		num = 0

		if self.lastBuyPoint == 0:
			# 昨日成交额低于20日最大成交额1/10
			if float(lastData.turnover) <= lastData.tomax['20']*0.1:
				result, num = self.opMgr.buy(self.index, data)
				if result:
					flag = True
					self.l.log('%s-%s-%s' %(data.y, data.m, data.d))
					self.l.log('turnover : %s is lower than 1/10 TOMax : %.3f' %(lastData.turnover, lastData.tomax['20']*0.1))
		# else:
			# 暂不考虑加仓
			# buyPoint = self.lastBuyPoint + lastData.atr[self.tutle.nKey]*0.5
			# if float(lastData.end) > buyPoint:
			# 	result, num = self.opMgr.buy(self.index, data)
			# 	if result:
			# 		flag = True
			# 		self.l.log('%s-%s-%s' %(data.y, data.m, data.d))
			# 		self.l.log('CP : %s is over 0.5ATR : %.3f' %(lastData.end, buyPoint))

		if flag:
				self.lastBuyPoint = round(float(data.end), 3)

				self.l.log('Buy %s %s' %(self.index, num))
				self.l.log('Stock count : %s, price : %s' %(self.tutle.stockCount, data.end))
				self.l.log('Left money : %s' %self.opMgr.payWayCache[self.index].all)
				self.l.log('-'*45)
				return True, num

		return False, 0

	def sell(self, data, lastData):
		# 昨日向下突破两个ATR
		sellPoint = self.highestPrice - lastData.atr[self.tutle.nKey]*2
		if float(lastData.end) < sellPoint:
			result, original, final, detail = self.opMgr.sell(self.index, data)
			if result:
				self.lastBuyPoint = 0

				self.l.log( '%s-%s-%s, CP : %s is lower than sellPoint : %.3f' %(data.y, data.m, data.d, lastData.end, sellPoint))
				self.l.log( 'Sell %s' %self.index)

				self.addAllTimes()
				num = round(final/original*100, 2)
				if final > 0:
					self.l.log( 'InCome : %s' %final)
					self.l.log( 'Left money : %s, precent:%s' %(self.opMgr.payWayCache[self.index].all, num))
					self.addWinTimes()
					self.logDetail(detail)
				elif final < 0:
					self.l.log( 'lose : %s' %final)
					self.l.log( 'Left money : %s, precent:%s' %(self.opMgr.payWayCache[self.index].all, num))
					self.addLoseTimes()
					self.logDetail(detail)
				else:
					self.l.log( 'Not Win Not Loss...')
					return False, 0

				return True, final

		return False, 0

	def outPut(self):
		self.outputMMAX = True
		self.outputATR = True
		# self.outputMMIN = True
		self.addOHLC(self.sh.stockDatas, 'SH')
		