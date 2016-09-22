#coding=utf8
import StateDefine as SD
import MathTool
import math

class StockAllLowData(object):
	"""docstring for StockAllLowData"""
	def __init__(self):
		super(StockAllLowData, self).__init__()
		# 低于均线后最低收盘价
		self.lowestPrice = None
		# 低于均线当天的数据
		self.downData = None
		# 所有低于均线数据{'date':'','diff':'','point':'','lowest':''}
		self.allLowData = []
		# 所有低于均线时的最大跌幅(跌幅为0的数据不录入)
		# self.downMaLowestDiff = []
		self.point = None

	# 记录低于均线时跌幅
	def recordDownMa(self, curState, data):
		if curState == SD.STOCK_SELL:
			# 记录跌破均线后当天的价格
			self.downData = data
			self.lowestPrice = float(self.downData.end)
		elif curState == SD.STOCK_NOTHING:
			# 低于均线的日子检查是否出现更低价格
			if (not self.lowestPrice is None) and self.lowestPrice > float(data.end):
				self.lowestPrice = float(data.end)
		elif curState == SD.STOCK_BUY:
			if not self.downData is None:
				diff = MathTool.increase(self.downData.end, self.lowestPrice, True)
				diffWin = MathTool.increase(self.lowestPrice, data.end, True)
				self.allLowData.append({
					'date':self.downData.getDate(), 
					'endDate':data.getDate(),
					'diff':diff,
					'point':self.downData.end, # 低于均线当天的数据
					'lowest':self.lowestPrice,
					'end':data.end, # 突破均线当天的数据
					'diffWin':diffWin # 最低点反弹幅度
					})
				# if diff < 0:
				# 	self.downMaLowestDiff.append(diff)
				result = self.analyse(self.allLowData)
				self.point = result['point']
				self.downData = None
				self.lowestPrice = None

	# 分析得到的抵御均线最大跌幅的数据
	def analyse(self, allLowData):
		dAndDWinList = [] #最大跌幅和反弹幅度
		diffList = [] #最大跌幅
		if len(allLowData) < 3:
			return {'list':allLowData, 'point':0}
		for _item in allLowData:
			if _item['diff'] < 0:
				dAndDWinList.append([_item['diff'], _item['diffWin']])
				diffList.append(_item['diff'])
		diffList.sort(reverse = True)
		dAndDWinList.sort(key = lambda x:x[0], reverse = True)
		maxNum = diffList[0]
		minNum = diffList[-1]
		diff = maxNum - minNum
		ground = math.ceil(math.sqrt(len(diffList)))
		length = diff / ground
		percent = 0	
		point = -length
		for _index, _item in enumerate(diffList):
			if _item < point:
				percent = (_index + 1) / float(len(diffList))
				if percent > 0.7:
					break
				else:
					point = point - length
			# print _item, point, percent
		# print 'diff', diff
		# print 'ground', ground
		# print 'length', length
		# print 'percent', percent
		# print 'point', point
		return {'list':dAndDWinList, 'point':point}

	def getAllLowData(self):
		return self.allLowData

	def getPoint(self):
		return self.point

