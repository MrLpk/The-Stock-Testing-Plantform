#coding=utf8

from BaseCase import BaseCase
from Stock import Stock
import NameList as NL
from BaseData import BaseData
from OperationMgr import OperationMgr
from Turtle import Turtle
from Elephant import Elephant
from Operation import Operation

class Case1(BaseCase):
	"""docstring for Case1"""
	def __init__(self):
		super(Case1, self).__init__()
		# key
		# self.index = 'SZ159915' # 创业板ETF
		# self.index = 'SH510300' # 300ETF
		self.index = 'SH510050' # 50ETF
		# self.index = 'SZ159902' # 中小板
		# self.index = 'SZ159901' # 深100ETF
		# self.index = 'SZ150153' # 创业板分级B

		self.beginAsset = 100000

		# tutle
		self.assetCtrl = Turtle()
		# self.assetCtrl = Elephant()
		self.assetCtrl.original = self.beginAsset
		self.assetCtrl.all = self.beginAsset
		self.assetCtrl.nKey = '20'
		self.inputLock = False
		self.mmax = '10'
		self.mmin = '20'
		self.ma = '20'

		self.beginIndex = 20

	def introduce(self):
		self.fileName = 'Case1'
		self.l.log('Case1...')

	def initStock(self):
		self.stock = Stock(atr = [int(self.assetCtrl.nKey)], ma = [self.ma], max = [self.mmax], min = [self.mmin])
		self.stock.create(self.index)
		self.l.log('data count : ' + str(len(self.stock.stockDatas)))
		
		self.outputMMAX = True
		self.outputMMIN = True
		self.outputATR = True
		self.outputMA = True
		self.outputAssetRecord = True
		self.outputFR = True
		# self.outputMMIN = True

		self.opMgr.regStock(self.index, self.assetCtrl)
		self.m.isSave = False #不输出
		# self.inputLock = True # 控制分步执行
		self.setBeginTime(2000, 1, 1)
		self.setEndTime(2015, 6, 26)
		self.highestPrice = 0 # 最高购入点

		self.inject(self.stock)
		

	def update(self, index, data):
		if index <= 1:
			return

		lastData = self.stock.stockDatas[index-1]
		beforelast = self.stock.stockDatas[index-2]

		result, volume = self.checkBuy(data, lastData, beforelast)
		if result:
			self.updateHighestPrice(data.end, True)
			return

		result, volume = self.checkSell(data, lastData)
		if result:
			self.l.log('-'*70)
			if self.inputLock:
				raw_input()
					
		# if data.y == '1994' and data.m == '08' and data.d == '10':
		# 	 	raw_input()
		self.updateHighestPrice(data.end)
			
	def updateHighestPrice(self, price, replace = False):
		if replace:
			self.highestPrice = float(price)
			# print 'update replace', price
			return

		if float(price) > self.highestPrice:
			self.highestPrice = float(price)
			# print 'update', price
	def checkBuy(self, data, lastData, beforelast):
		# 昨日突破20日最高点

		diff = (float(data.end) / float(lastData.end) - 1) * 100
		if diff >= 9.5:
			# print data.date
			# print 'diff :', diff
			# raw_input()
			return False, 0

		if self.tradeState == self.NOTHING:
			if float(lastData.end) >= lastData.mmax[self.mmax]:
				infos = ['\tClose Price : %s is higher than MMAX-%s : %.3f' %(lastData.end, self.mmax, lastData.mmax[self.mmax])]
			# if float(lastData.end) >= lastData.ma[self.ma]:
			# 	infos = ['\tClose Price : %s is higher than MA-%s : %.3f' %(lastData.end, self.ma, lastData.ma[self.ma])]
				result, num = self.buy(data, infos)

				return result, num
		
		if self.tradeState == self.BUY:
			# 昨日突破0.5ATR
			buyPoint = self.lastBuyPoint + lastData.atr[self.assetCtrl.nKey]*0.5
			if float(lastData.end) > buyPoint:
				infos = ['\tClose Price : %s is over 0.5ATR : %.3f' %(lastData.end, buyPoint),
						 '\tATR-%s : %s' %(self.assetCtrl.nKey, lastData.atr[self.assetCtrl.nKey])]
				result, num = self.buy(data, infos)

				return result, num

		return False, 0

	def checkSell(self, data, lastData):
		diff = (float(data.end) / float(lastData.end) - 1) * 100
		if diff <= -9.5:
			# print data.date
			# print 'diff :', diff
			# raw_input()
			return False, 0
		# 昨日向下突破3个ATR
		sellPoint = self.highestPrice - lastData.atr[self.assetCtrl.nKey]*2
		if float(lastData.end) < sellPoint:
			infos = ['\tClose Price : %s is lower than sellPoint : %.3f' %(lastData.end, sellPoint)]

		# 10日低点突破
		# if float(lastData.end) <= lastData.mmin[self.mmin]:
		# 	infos = ['\tClose Price : %s is lower than MMIN-%s : %.3f' %(lastData.end, self.mmin, lastData.mmin[self.mmin])]
			result, num = self.sell(data, infos)
			
			return result, num

		return False, 0
		
if __name__ == '__main__':
	c = Case1()
	c.run()
