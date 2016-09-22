#coding=utf8
from CaseFrame import CaseFrame
from Elephant import Elephant
from StockEdit import StockEdit
from Wolf import Wolf
import MathTool as MT
import math

''' 定投测试 '''
class Fi(object):
	"""docstring for Fi"""
	def __init__(self, code = None):
		super(Fi, self).__init__()
		if code == None:
			# index = 'SZ159915' # 创业板ETF
			# index = 'SH510300' # 300ETF
			# index = 'SH510050' # 50ETF
			# index = 'SZ159902' # 中小板
			# index = 'SZ159901' # 深100ETF
			# index = 'SZ150153' # 创业板分级B
			# index = 'SH600036' # 招商银行
			# index = 'SH600196' # 复星医药
			# index = 'SH600519' # 贵州茅台
			# index = 'SH600547' # 山东黄金
			# code = 'SH000016' #上证50
			code = 'SZ399006' # 创业板指

		self.stock = StockEdit(code)
		self.assetCtrl = Wolf(base=1000)

	def test(self):
		usingMoney = 0
		totalValue = 0
		maxMoney = 0
		asset = 0
		rate = 0
		for index, data in enumerate(self.stock.getDatas()):
			price = float(data.end)
			_rate, _cost, totalValue = self.assetCtrl.getBuyStockCount(price, rate, totalValue, usingMoney)

			rate = rate + _rate
			usingMoney = usingMoney + _cost

			if usingMoney > maxMoney:
				maxMoney = usingMoney
			# print index+1, price, _cost, usingMoney, totalValue

			print '-'*50
			print index+1, data.getDate()#, price, _cost, totalValue, usingMoney, round(((totalValue/usingMoney)-1)*100, 2)
			print 'price :', price
			print 'cost :', _cost
			print 'totalValue :', totalValue
			print 'usingMoney :', usingMoney

			if usingMoney < 0:
				# raise TypeError('aaa')
				asset = totalValue - usingMoney
				base = math.floor(asset / maxMoney * self.assetCtrl.getBase())
				self.assetCtrl.setBase(base)
				usingMoney = 0
				totalValue = 0
				maxMoney = 0
				rate = 0
			if index == 9:
				# break
				pass
		print 'asset', asset
		beginData = self.stock.getDatas()[1]
		endData = self.stock.getDatas()[-1]
		year = int(endData.getYear()) - int(beginData.getYear()) + 1
		print '-'*50
		print 'time : %s %s' %(beginData.getDate(), endData.getDate())
		print 'Year :', year
		print 'max :', maxMoney
		print 'totalValue :', totalValue - usingMoney + asset
		print 'CAGR : %s%%' %(MT.CAGR(totalValue - usingMoney + asset, maxMoney, year))

	def run(self):
		frame = CaseFrame()
		frame.setFixMode(self.mode)
		frame.setIsSave(self.isSave)
		frame.outputMA = self.outputMA
		frame.setBeginIndex(20)
		frame.setBeginAsset(self.beginAsset)
		frame.setAssetController(self.asset)
		frame.setBuyController(self.buy)
		frame.setSellController(self.sell)
		frame.setBeginTime(2005, 01, 01)
		frame.setEndTime(2015, 12, 31)
		frame.setStock(self.stock, self.beginAsset)

		if self.doOutPut:
			frame.outPut()
			frame.save()
		else:
			frame.analysisResult()
			# frame.makeXLS()
		return frame.getResult()