#coding=utf8

from BaseCase import BaseCase
from Stock import Stock
import StateDefine as SD

class CaseFrame(BaseCase):
	"""docstring for CaseFrame"""
	def __init__(self):
		super(CaseFrame, self).__init__()
		self.dataObj = {}
		self.dataObj['stock'] = None
		self.dataObj['index'] = None
		self.dataObj['data'] = None
		self.dataObj['tradeState'] = None
		self.dataObj['atrKey'] = None # ATR的均线日

		# self.beginAsset = 0


	def setBeginAsset(self, asset):
		self.beginAsset = asset

	def setBeginIndex(self, index):
		self.beginIndex = index

	def setAssetController(self, ctrl):
		self.assetCtrl = ctrl

	def setBuyController(self, ctrl):
		self.buyCtrl = ctrl

	def setSellController(self, ctrl):
		self.sellCtrl = ctrl

	def setIsSave(self, isSave):
		self.m.isSave = isSave

	def setStock(self, stock, baseAsset, inject = True):
		self.stock = stock
		self.index = self.stock.getCode()
		# self.opMgr.regStock(self.index, self.assetCtrl, baseAsset)
		self.makeOperation(self.assetCtrl, baseAsset)
		self.dataObj['stock'] = self.stock
		self.introduce()
		
		if inject:
			self.inject(self.stock)

	def introduce(self):
		self.fileName = 'CaseFrame'
		self.l.log('CaseFrame...')
		self.l.log(self.assetCtrl.getIntroduce())
		self.l.log(self.buyCtrl.getIntroduce())
		self.l.log(self.sellCtrl.getIntroduce())
		# self.l.log(self.stock.getIntroduce())

	# 改模式
	# 1:持有第五天卖出，第10天如果仍可买再重新买入，其他不变
	def setFixMode(self, mode):
		self.mode = mode

	def update(self, index, data):
		if index <= 1:
			return

		self.dataObj['index'] = index
		self.dataObj['data'] = data
		self.dataObj['tradeState'] = self.tradeState
		self.dataObj['lastBuyPoint'] = self.lastBuyPoint
		self.dataObj['highestPrice'] = self.highestClosePrice
		self.dataObj['isLastTimeWin'] = self.isLastTimeWin
		self.dataObj['lastSellIndex'] = self.lastSellIndex
		self.dataObj['beginPrice'] = self.beginTradeData.end if not self.beginTradeData is None else 0
		self.dataObj['assetCtrl'] = self.assetCtrl
		self.dataObj['operation'] = self.op

		if self.mode == 1:
			# if (not self.mode1Cache['isActive']) and self.tradeState == SD.BUY:
			# 	if self.curIndex - self.lastBuyIndex == 4:
			# 		self.tempSell(data)
			# elif self.mode1Cache['isActive']:
			# 	if self.curIndex - self.lastBuyIndex == 9:
			# 		checkResult = self.sellCtrl.check(self.dataObj)
			# 		if not checkResult['r']:
			# 			self.continueBuy(data)
			pass
			# 预计废弃的代码

		if self.checkBuy(index, data):
			checkResult = self.buyCtrl.check(self.dataObj)
			if checkResult['r']:
				result, num = self.buy(data, checkResult['m'])
				# if result:
				# 	self.updateHighestPrice(data.end, True)
				# 	return
				return

		if self.checkSell(index, data):
			checkResult = self.sellCtrl.check(self.dataObj)
			if checkResult['r']:
				result, num = self.sell(data, checkResult['m'])

		# self.updateHighestPrice(data.end)
		



	




