#coding=utf8

from BaseData import BaseData
import copy
import numpy as NP
from GlobalConfig import GlobalConfig
import StateDefine as SD
import StockMathTool as SMT
import MathTool
import math
from StockAllLowData import StockAllLowData

class Stock(object):
	"""docstring for Stock"""
	def __init__(self, ma = [20], max = [20], min = [20], atr = [20], tomax = [], tomin = [], frSum = [20], frl = [20], frLimit = [20, 60, 120], index = '', increase = [20, 40]):
		super(Stock, self).__init__()

		self.stockDatas = [] # 每日数据
		self.func = None
		self.funcName = None
		self.maCache = {}
		self.maxCache = {}
		self.minCache = {}
		self.trCache = {'last':-1}
		self.atrCache = {}
		self.tomaxCache = {}
		self.tominCache = {}

		self.frSumCache = {}
		self.allFrCache = {}
		self.frLevelCache = {}
		self.frLimitCache = {}

		# 标的当前的推荐交易状态
		self.curState = {}

		# # 低于均线后最低收盘价
		# self.lowestPrice = None
		# # 低于均线当天的数据
		# self.downData = None
		# # 所有低于均线数据{'date':'','diff':'','point':'','lowest':''}
		# self.allLowData = []
		# # 所有低于均线时的最大跌幅(跌幅为0的数据不录入)
		# self.downMaLowestDiff = []
		self.stockAllLowData = StockAllLowData()

		# 5、20、40日均线是必须要的
		defaultMa = ['5', '20', '40']
		for _dMa in defaultMa:
			if not _dMa in ma:
				ma.append(_dMa)

		self.mas = ma
		self.increase = increase

		# 确保atr有的key MA也有，这样afr才能计算
		for x in atr:
			if not x in ma:
				ma.append(x)

		self.maCache = self.initCache(ma, {'all':0, 'list':[]})
		self.maxCache = self.initCache(max, {'list':[]})
		self.minCache = self.initCache(min, {'list':[]})
		self.atrCache = self.initCache(atr, {'all':0, 'list':[]})
		self.tomaxCache = self.initCache(tomax, {'list':[]})
		self.tominCache = self.initCache(tomin, {'list':[]})
		self.frSumCache = self.initCache(frSum, {'all':0, 'list':[]})
		# self.allFrCache = self.initCache()
		self.frLevelCache = self.initCache(frl, {'all':0, 'list':[]})
		self.frLimitCache = self.initCache(frLimit, {'all':0, 'list':[]})

		self.cache = {}
		#atr / ma 波动幅度，衡量波动占价格的幅度,因为计算需要ma，所有key也已ma为基准
		self.cache['fluctuateRange'] = self.initCache(ma, {'all':0, 'count':0})
		# 60个atr/ma 波动均值，上面的可能要废除，因为所有平均的话并不一定准确反馈近期波幅
		self.cache['meanFR'] = self.initCache(['20', '40', '60'], {'all':0, 'list':[]})

		self.avgFluctuateRange = {}
		self.meanFR = {} # 60日均波幅

		self.isInMaCycle = False # 是否处在20日均线的交易周期里

		if not index == '':
			self.code = index
			self.create(index)

	def getCode(self):
		return self.code

	def setCode(self, code):
		self.code = code

	def setFunc(self, params):
		func = params['func']
		funcName = params['funcName']

		self.func = func
		self.funcName = funcName

	def getCurState(self, name = 'ma'):
		if not name in self.curState:
			self.curState[name] = SD.STOCK_NOTHING

		return self.curState[name]

	def setCurState(self, state, name = 'ma'):
		self.curState[name] = state


	# 初始化缓存
	def initCache(self, list, value):
		dictionary = {}

		if len(list) == 0:
			return dictionary

		for t in list:
			dictionary[str(t)] = copy.deepcopy(value)

		return dictionary

	# 根据name生成路径
	def getPath(self, name):
		import os
		path = 'Smaug/%s.txt' %name

		mode = GlobalConfig().get('mode')
		if mode == 'Hobbit':
			path = 'Hobbit/%s.txt' %name

		if os.path.isfile(path):
			return path
		else:
			raise TypeError(path)

	def getMas(self):
		return self.mas

	# 返回MA-XX形式的list
	def getMas_title(self):
		array = []
		for _ma in self.mas:
			array.append('MA-%s' %_ma)
		return array

	def create(self, name = None):
		if name is None:
			name = self.code
		path = self.getPath(name)
		lines = open(path, 'r').readlines()
		for lineCount, line in enumerate(lines):
			# print lineCount, line[:-4]
			words = line.split(',')
			if not len(words) == 7:
				continue
			data = BaseData(0, words[0], words[1], words[2], words[3], words[4], words[5], words[6].rstrip())

			# 第一个数据没有波幅，填当天收盘价
			if self.trCache['last'] < 0:
				self.addTrCache(data.end)

			# 缓存收盘价
			self.addCache(data.end)

			# 记录均价
			for t, cache in self.maCache.items():
				# data.ma[t] = round(cache['all'] / len(cache['list']), 3)
				data.ma[t] = round(NP.mean(cache['list']), 3)
				data.std[t] = round(NP.std(cache['list']), 3)
				data.bias[t] = ((float(data.end) / data.ma[t]) - 1) * 100

			# 记录N日收盘价最大值
			for t, cache in self.maxCache.items():
				data.mmax[t] = max(cache['list'])

			# 记录N日收盘价最小值
			for t, cache in self.minCache.items():
				data.mmin[t] = min(cache['list'])

			# 记录当日波幅&当日ATR
			maxToday = float(data.max)
			minTOday = float(data.min)
			trs = [abs(maxToday - minTOday),
					abs(self.trCache['last'] - maxToday),
					abs(self.trCache['last'] - minTOday)]
			data.tr = round(max(trs), 3)
			self.addAtrCache(data.tr)

			for t, cache in self.atrCache.items():
				atr = round(cache['all'] / len(cache['list']),3)
				data.atr[t] = atr
				data.afr[t] = round(atr / float(data.ma[t]) * 100, 2)
				# 波动幅度
				data.fluctuateRange[t] = round(atr / float(data.ma[t]) * 100, 2)
				# 缓存所有波动幅度，用以计算均值
				fluctuateRangeDict = self.cache['fluctuateRange'][t]
				fluctuateRangeDict['all'] = fluctuateRangeDict['all'] + data.fluctuateRange[t]
				fluctuateRangeDict['count'] = fluctuateRangeDict['count'] + 1
				
			# 缓存60个20日波动幅度
			self.addAllListCache(self.cache['meanFR'], data.fluctuateRange['20'])
			for t, cache in self.cache['meanFR'].items():
				data.meanFR[t] = round(cache['all'] / len(cache['list']), 3)

			for frKey, frValue in data.fr.items():
				offset = 1
				if lineCount == 0:
					if float(data.begin) > float(data.end):
						offset = -1
				else:
					if self.trCache['last'] > float(data.end):
						offset = -1
				self.addSomeCache(self.frLevelCache, frValue * offset)
				self.addSomeCache(self.frLimitCache, frValue)
				self.addSomeCache(self.frSumCache, frValue * offset)

			# for frLiKey, frLiValue in self.frLimitCache.items():
			# 	data.frLimit[frLiKey] = round(frLiValue['all'] / len(frLiValue['list']), 2)

			for frSumKey, frSumValue in self.frSumCache.items():
				finalResult = 1
				for oneValue in frSumValue['list']:
					finalResult = finalResult * (1+oneValue/100.0)
				data.frSum[frSumKey] = round(finalResult-1, 5)

				# print self.frSumCache
				# print data.frSum
				# raw_input()

			# print self.frSumCache
			# raw_input()
			
			self.addTrCache(data.end)
			for t, cache in self.frLevelCache.items():
				if not t in data.fr:
					continue
				data.frl[t] = round(cache['all'] / len(cache['list']), 3)

			# 缓存交易额
			self.addToCache(data.turnover)

			# 记录N日交易额最大值
			if len(self.tomaxCache) > 0:
				for t, cache in self.tomaxCache.items():
					data.tomax[t] = max(cache['list'])

			# 记录N日交易额最小值
			if len(self.tominCache) > 0:
				for t, cache in self.tominCache.items():
					data.tomin[t] = min(cache['list'])


			for _increase in self.increase:
				data.pastDayMa[str(_increase)] = float(self.getFrontDataByIndex(_increase, data).ma['5'])
				
			self.stockDatas.append(data)

			# 生成基于均线的交易状态
			self.makeMaState()
			# 记录低于均线时跌幅
			self.stockAllLowData.recordDownMa(self.getCurState(), data)

			if not self.func is None:
				self.func(
					{
						'datas':self.stockDatas,
						'obj':self,
					}
				)

			# print 'trs:', trs
			# print 'maCache', self.maCache
			# print 'atrcache:', self.atrCache
			# print 'ma:', data.ma
			# print 'mmax:', data.mmax
			# print 'mmin:', data.mmin
			# print 'tr:', data.tr
			# print 'atr:', data.atr
			# print '-' * 60
			# if lineCount >= 50:
			# 	break

			# raw_input()
			
		
		# 统计均值
		for key, value in self.cache['fluctuateRange'].items():
			if value['count'] == 0:
				self.avgFluctuateRange[key] = 0
				continue
			self.avgFluctuateRange[key] = value['all'] / value['count']
		

	def makeMaState(self):
		# 最后一个数据
		data = self.stockDatas[-1]
		curState = self.getCurState()
		if curState == SD.STOCK_NOTHING or curState == SD.STOCK_SELL:
			result, _ = SMT.compareMaBuy(data, data)
			# 当天符合条件的标记为购买
			if result:
				data.tradeState = SD.STOCK_BUY
				self.setCurState(data.tradeState)
			else:
				data.tradeState = SD.STOCK_NOTHING
				self.setCurState(data.tradeState)
		elif curState == SD.STOCK_BUY or curState == SD.STOCK_HOLD:
			result, _ = SMT.compareMaSell(data, data)
			# 购买第二天没卖出的标记为持有，卖出的标记为nth
			if result:
				data.tradeState = SD.STOCK_SELL
				self.setCurState(data.tradeState)
			else:
				data.tradeState = SD.STOCK_HOLD
				self.setCurState(data.tradeState)

	# 记录低于均线时跌幅
	# def makeDownMaRecord(self):
	# 	curState = self.getCurState()
	# 	data = self.stockDatas[-1]
	# 	if curState == SD.STOCK_SELL:
	# 		# 记录跌破均线后当天的价格
	# 		self.downData = data
	# 		self.lowestPrice = float(self.downData.end)
	# 	elif curState == SD.STOCK_NOTHING:
	# 		# 低于均线的日子检查是否出现更低价格
	# 		if (not self.lowestPrice is None) and self.lowestPrice > float(data.end):
	# 			self.lowestPrice = float(data.end)
	# 	elif curState == SD.STOCK_BUY:
	# 		if not self.downData is None:
	# 			diff = MathTool.increase(self.downData.end, self.lowestPrice, True)
	# 			diffWin = MathTool.increase(self.lowestPrice, data.end, True)
	# 			self.allLowData.append({
	# 				'date':self.downData.getDate(), 
	# 				'endDate':data.getDate(),
	# 				'diff':diff,
	# 				'point':self.downData.end, # 低于均线当天的数据
	# 				'lowest':self.lowestPrice,
	# 				'end':data.end, # 突破均线当天的数据
	# 				'diffWin':diffWin # 最低点反弹幅度
	# 				})
	# 			if diff < 0:
	# 				self.downMaLowestDiff.append(diff)
	# 			self.downData = None
	# 			self.lowestPrice = None


	# 或许N日前的BaseData，如果没有则返回index为0的BaseData
	# append新数据之前使用
	def getFrontDataByIndex(self, frontNum, default):
		if frontNum == 0:
			print "frontNum can't not be 0"
			return 

		totalCount = len(self.stockDatas)
		if totalCount == 0:
			return default

		if totalCount >= frontNum:
			return self.stockDatas[totalCount - frontNum]
		else:
			return self.stockDatas[0]

	def addCache(self, num):
		self.addMaCache(num)
		# self.addMmCache(num)
		self.addMmCache(self.maxCache, num)
		self.addMmCache(self.minCache, num)

	# 缓存N日交易额最大最小值
	def addToCache(self, num):
		if len(self.tomaxCache) > 0:
			self.addMmCache(self.tomaxCache, num)
			
		if len(self.tominCache) > 0:
			self.addMmCache(self.tominCache, num)

	def addMaCache(self, num):
		if len(self.maCache) > 0:
			self.addAllListCache(self.maCache, num)

	# 某个N日最值缓存进行数值更新
	def addMmCache(self, mmCache, num):
		num = float(num)
		for x, cache in mmCache.items():
			if len(cache['list']) == int(x):
				cache['list'].pop(0)

			mmCache[x]['list'].append(num)

		# print self.mmCache

	# 计算TR需要上个交易日收盘价，所以存一下
	def addTrCache(self, last):
		self.trCache['last'] = float(last)

	# update some dictionary like this {'all':0, 'list':[]}
	def addAllListCache(self, cache, num):
		num = float(num)
		for k, v in cache.items():
			diff = num
			if len(v['list']) == int(k):
				diff = diff - v['list'][0]
				v['list'].pop(0)

			v['all'] = round(v['all'] + diff, 3)
			v['list'].append(num)

	def addAtrCache(self, num):
		if len(self.atrCache) > 0:
			self.addAllListCache(self.atrCache, num)

	def addSomeCache(self, cache, num):
		if len(cache) > 0:
			self.addAllListCache(cache, num)

	def getValueByIndex(self, dict, index):
		key = dict.keys()[index]
		return dict[key]

	def getAvgFluctuateRange(self):
		return round(self.avgFluctuateRange['20'], 3)

	def getMeanFR(self, key = '60'):
		key = str(key)

		return self.stockDatas[-1].meanFR[key]

	def outPutXML(self):
		array = []
		datas = [[
			u'日期', 
			u'开盘', 
			u'最高', 
			u'最低', 
			u'收盘', 
			u'tr', 
			u'atr-20', 
			u'ma-20', 
			u'ma-40',
			u'fr-20', 
			u'meanFR-20', 
			u'meanFR-60', 
			u'std-20', 
			u'inc-20', 
			u'inc-40',
			u'ir-20',
			u'ir-40',
			u'bias-20',
			u'wir',
			u'wma',
		]]
		for _item in self.stockDatas:
			datas.append([
				_item.getDate(), 
				float(_item.begin), 
				float(_item.max), 
				float(_item.min), 
				float(_item.end), 
				_item.tr,
				_item.atr['20'],
				_item.ma['20'],
				_item.ma['40'],
				_item.fluctuateRange['20'],
				_item.meanFR['20'],
				_item.meanFR['60'],
				_item.std['20'],
				_item.pastDayMa['20'],
				_item.pastDayMa['40'],
				_item.getIRP(20),
				_item.getIRP(40),
				_item.bias['20'],
				_item.getWIRP(),
				_item.getWMa(),
				])
		array.append({'name':'Stock', 'data':datas})
		# 记录低于均线数据
		datas = [[u'开始日期', u'结束日期', u'均线', u'最低', u'均线上', u'跌幅', u'涨幅']]
		allLowData = self.stockAllLowData.getAllLowData()
		for _item in allLowData:
			datas.append([
				_item['date'],
				_item['endDate'],
				_item['point'],
				_item['lowest'],
				_item['end'],
				_item['diff'],
				_item['diffWin'],
			])
		array.append({'name':'DownMa', 'data':datas})
		datas = self.stockAllLowData.analyse(allLowData)['list']
		array.append({'name':'DownMa1', 'data':datas})



		from XlsHelper import XlsHelper
		XlsHelper('Stock.xls').create(array)

	# # 分析得到的抵御均线最大跌幅的数据
	# def analyseAllLowData(self, allLowData):
	# 	dAndDWinList = [] #最大跌幅和反弹幅度
	# 	diffList = [] #最大跌幅
	# 	if len(allLowData) < 3:
	# 		return {'list':allLowData, 'point':0}
	# 	for _item in allLowData:
	# 		if _item['diff'] < 0:
	# 			dAndDWinList.append([_item['diff'], _item['diffWin']])
	# 			diffList.append(_item['diff'])
	# 	diffList.sort(reverse = True)
	# 	dAndDWinList.sort(key = lambda x:x[0], reverse = True)
	# 	maxNum = diffList[0]
	# 	minNum = diffList[-1]
	# 	diff = maxNum - minNum
	# 	ground = math.ceil(math.sqrt(len(diffList)))
	# 	length = diff / ground
	# 	percent = 0	
	# 	point = -length
	# 	for _index, _item in enumerate(diffList):
	# 		if _item < point:
	# 			percent = (_index + 1) / float(len(diffList))
	# 			if percent > 0.7:
	# 				break
	# 			else:
	# 				point = point - length
	# 		# print _item, point, percent
	# 	# print 'diff', diff
	# 	# print 'ground', ground
	# 	# print 'length', length
	# 	# print 'percent', percent
	# 	# print 'point', point
	# 	return {'list':dAndDWinList, 'point':point}
			



if __name__ == '__main__':
	# s = Stock(atr = ['20'], ma = ['20'], index = 'SZ399975')
	# 	s.outPutXML()
	pass

		

		