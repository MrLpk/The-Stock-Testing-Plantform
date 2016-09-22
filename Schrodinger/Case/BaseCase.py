#coding=utf8

from Log import Log
import NameList as NL
from Stock import Stock
from MTool import MTool
from Operation import Operation
import os
from datetime import datetime
import MathTool as Math
from BaseData import BaseData
from XlsHelper import XlsHelper
import StateDefine as SD

class BaseCase(object):
	"""docstring for BaseCase"""
	def __init__(self):
		super(BaseCase, self).__init__()
		self.fileName = ''
		self.stock = None
		self.index = ''
		self.beginAsset = 0
		self.beginDate = ''
		self.endDate = ''
		self.assetCtrl = None
		self.op = None
		self.datas = []
		self.m = MTool()
		self.l = Log()
		self.l.m = self.m
		self.highestClosePrice = 0 # 持仓过程中出现的最高收盘价 
		self.lowestClosePrice = 0 # 持仓过程中出现的最低收盘价
		self.highestAsset = 0 # 持仓过程中出现的资产最高值
		self.lowestAsset = 0 # 持仓过程中出现的资产最低值
		self.isLastTimeWin = True
		self.lastBuyIndex = 0
		self.lastSellIndex = 0
		self.beginIndex = 0
		self.resultCache = {'num':[], 'data':[]} # 交易结果缓存，后续用来计算最大盈利、最大亏损等等
		self.assetsCache = {'years':[]} # 所有资产变化，按年分类
		self.classifyCache = {} # key:年份，value：[moneys];按年份分类
		self.bigCache = {'percents':[], 'datas':[], 'moneys':[]} # 百分比、数据、资产缓存
		# self.bigCache['frs'] = {} # 波动率
		# self.bigCache['afrs'] = {} # 均波动率 atr/ma
		self.allFr = {}

		# 存储最终结果
		self.result = {
			'beginDate':'', 
			'endDate':'', 
			'baseAsset':'', 
			'asset':'', 
			'cagr':'', 
			'avgFluctuateRange':'', 
			'buySellDay':[]
			}

		self.s = {}
		self.s['series'] = ['var series = [']
		self.s['ohlcs'] = ['var ohlcs = [']
		self.s['tradeRecords'] = ['var tradeRecords = [']
		self.s['atrs'] = ['var atrs = [']
		self.s['assets'] = ['var assets = ['] # 记录资产变化
		self.s['drawdowns'] = ['var drawdowns = ['] # 回撤
		# self.s['frs'] = ['var frs = ['] # 波动率
		self.s['frrs'] = ['var frrs = ['] # 波动率
		self.s['frgs'] = ['var frgs = ['] # 波动率
		self.s['frws'] = ['var frws = ['] # 波动率
		self.s['afrs'] = ['var afrs = ['] # 均波动率 atr/ma
		self.s['frls'] = ['var frls = ['] # fr level
		self.s['frps'] = ['var frps = [']

		self.outPutData = {}
		self.outPutData['tradeData'] = [{
				'date':u'日期', 
				'action':u'操作', 
				'count':u'数量',
				'price':u'价格',
				'cost':u'总价',
				'remain':u'剩余现金',
				'difference':u'盈亏',
				'percent':u'盈亏率'}]
		self.outPutData['dailyAssets'] = [[
				u'日期', 
				u'资产', 
		]] # 每日总资产 {'date':'xxx', 'asset':xx}
		self.outPutData['dailyAssetsSortByYear'] = []
		self.outPutData['buySellDay'] = [] # 记录从买入到卖出的间隔，以及该次的输赢情况、最大浮亏
		self.outPutData['closeMaPic'] = [] # 记录从买入到卖出期间的收盘价和ma，以及输赢情况
		self.closeMa = [] #closeMaPic缓存

		self.outPutData['highestGain'] = [] # 记录每次持仓过程中最大收盘价涨幅

		self.beginTradeData = None # 建仓首日数据
		self.beginTradeAsset = None # 建仓首日资产

		# self.allDiff = 0
		self.mode1Cache = {
			'beginPrice':'', 
			'sellPrice':'',
			'continuePrice':'',
			'endPrice':'',
			'isActive':False} #改1模式下的数据记录

		self.cache = {}
		self.cache['TRBuy'] = ['[']
		self.cache['TRWin'] = ['[']
		self.cache['TRLose'] = ['[']
		self.cache['assets'] = ['[']
		self.cache['drawdowns'] = ['[']


		self.ohlcCache = ['[']
		self.maCache = {}
		self.maxCache = {}
		self.minCache = {}
		self.atrCache = {}
		self.frCacheR, self.frCacheG, self.frCacheW, self.afrCacheR, self.afrCacheG, self.afrCacheW = {}, {}, {}, {}, {}, {}
		self.sss = {}
		self.frlCache = {}
		self.frpsCache = {}
		self.closePrice = {}


		self.ddTempRecord = {'y':0, 'm':0, 'd':0, 'record':[]}
		self.allTimes = 0
		self.winTimes = 0
		self.loseTimes = 0

		self.outputFR = False
		self.outputAFR = False
		self.outputOHLC = False#True
		self.outputMA = False
		self.outputMMAX = False
		self.outputMMIN = False
		self.outputATR = False
		self.outputTradeRecord = False#True
		self.outputAssetRecord = False
		self.outputDrawdownRecord = False#True

		self.beginTime = 0
		self.endTime = 0

		# 开仓位置
		self.lastBuyPoint = 0

		# 锁定收盘价
		# 在一些特殊情况，并不以当时价格结算，而是假定该次交易以锁定的价格结算
		self.lockClosePrice = None

		# self.BUY = 1
		# self.OVERWEIGHT = 2
		# self.NOTHING = 3
		self.tradeState = SD.NOTHING
		self.tradeCycle = SD.END


	def introduce(self):
		self.l.log( 'BaseCase...')

	def initStock(self):
		pass

	def analysis(self):
		pass

	def outPut(self):
		pass

	def setBeginTime(self, y, m, d):
		self.beginTime = self.m.makeTime(y, m, d)

	def setEndTime(self, y, m, d):
		self.endTime = self.m.makeTime(y, m, d)

	def inject(self, stock):
		for index, data in enumerate(stock.stockDatas):
			self._update(index, data)

	def _update(self, index, data):
		self.curIndex = index
		if index == 0:
			if self.beginTime > 0 and data.timestamp < self.beginTime:
				_date = self.m.getTime('%Y/%m/%d', self.m.localtime(self.beginTime))
				data = BaseData(0, _date, '', '', '', '', '', '')

			self.recordAssets(data, self.beginAsset)

		if index < self.beginIndex:
			return

		if not self.checkTime(data.timestamp):
			return

		if self.beginDate == '':
			self.beginDate = data.date
		self.endDate = data.date
		self.lastEffectData = data

		self.lastData = self.stock.stockDatas[index-1]

		for frKey, frValue in data.fr.items():
			if not frKey in self.allFr:
				self.allFr[frKey] = []
			self.allFr[frKey].append(frValue)

		if self.outputFR:
			if float(data.end) > float(lastData.end):
				self.addDict(self.frCacheR, data, data.fr)
				offset = 1
			elif float(data.end) < float(lastData.end):
				firstKey = data.fr.keys()[0]
				self.addDict(self.frCacheG, data, {firstKey:-data.fr[firstKey]})
				offset = -1
			else:
				self.addDict(self.frCacheW, data, data.fr)
				offset = 1
					
			for frKey, frValue in data.fr.items():
				if not frKey in self.sss:
					self.sss[frKey] = [offset * frValue]
					continue
				self.sss[frKey].append(self.sss[frKey][-1] + offset * frValue)

			self.addDict(self.frlCache, data, data.frl)
			self.addDict(self.frpsCache, data, data.frSum)

		if self.outputAFR:
			self.addDict(self.afrCache, data, data.afr)

		if self.outputOHLC:
			self.addOHLCCache(self.ohlcCache, data)

		if self.outputMA:
			self.addDict(self.maCache, data, data.ma)

		if self.outputMMAX:
			self.addDict(self.maxCache, data, data.mmax)

		if self.outputMMIN:
			self.addDict(self.minCache, data, data.mmin)

		if self.outputATR:
			self.addDict(self.atrCache, data, data.atr)
				
		self.recordDD(data, 2)

		self.outPutData['dailyAssets'].append([data.getDate(), self.op.getTotalAsset(data.end)])

		isNewYear = True
		for obj in self.outPutData['dailyAssetsSortByYear']:
			if data.getYear() in obj:
				isNewYear = False
				obj[data.getYear()].append([data.getDate(), self.op.getTotalAsset(data.end)])
		if isNewYear:
			self.outPutData['dailyAssetsSortByYear'].append({data.getYear():[[data.getDate(), self.op.getTotalAsset(data.end)]]})

		if self.tradeState == SD.BUY:
			self.closeMa.append(
				{
				'date':data.getDate(),
				'price':float(data.end),
				'ma':data.ma
				})
			self.updateHighestClosePrice(data.end)
			self.updateLowestClosePrice(data.min)
		self.update(index, data)
		

	def update(self, index, data):
		pass

	# 存储显示图表的数据
	def addBigCacheDict(self, key, dictionay, data):
		for x in dictionay:
			if not x in self.bigCache[key]:
				self.bigCache[key][x] = []

			self.bigCache[key][x].append({'y':data.y, 'm':data.m, 'd':dadta.d, 'data':dictionay[x]})

	# 按年份归类一下资产、资产变化率
	def recordAssets(self, data, money, percent = 0):
		money = round(float(money), 3)
		percent = float(percent)
		if not data.y in self.assetsCache:
			self.assetsCache[data.y] = {'m':[], 'p':[], 'd':[]}
			self.assetsCache['years'].append(data.y)

		self.assetsCache[data.y]['m'].append(money)
		self.assetsCache[data.y]['p'].append(percent)
		self.assetsCache[data.y]['d'].append(data)

		if not data.y in self.classifyCache:
			self.classifyCache[int(data.y)] = {'m':[], 'p':[], 'd':[]}

		self.classifyCache[int(data.y)]['m'].append(money)
		self.classifyCache[int(data.y)]['p'].append(percent)
		self.classifyCache[int(data.y)]['d'].append(data)

		self.bigCache['moneys'].append(money)
		self.bigCache['percents'].append(percent)
		self.bigCache['datas'].append(data)


	# 超过区间的时间返回False，区间内返回True
	def checkTime(self, time):
		if self.beginTime > 0 and time < self.beginTime:
			return False

		if self.endTime > 0 and time > self.endTime:
			return False

		return True

	# 记录回撤 
	# state:1、开始；2、中间;3、结束;
	def recordDD(self, data, state):
		if not self.outputDrawdownRecord:
			return
		if (not state == 1) and len(self.ddTempRecord['record']) == 0:
			return
		if not state in [1, 2, 3]:
			return

		self.ddTempRecord['record'].append(float(data.max))
		self.ddTempRecord['record'].append(float(data.min))

		if state == 3:
			record = self.ddTempRecord['record']
			highest = max(record)
			lowest = min(record[record.index(highest):])
			drawdown = round((highest - lowest) / highest * 100, 2)
			self.cache['drawdowns'].append('''{x:Date.UTC(%s,%d,%s), y:%.3f},
				''' %(data.y, int(data.m)-1, data.d, drawdown))

			self.ddTempRecord['record'] = []
			self.l.log('\n\tDrawDown:')
			self.l.log('\thighest : %s' %highest)
			self.l.log('\tlowest : %s' %lowest)
			self.l.log('\tMax drawdown : %s%%' %drawdown)

	# 购买时记录一下
	def recordBuy(self, data, price):
		self.recordDD(data, 1)
		if self.outputTradeRecord:
			self.cache['TRBuy'].append('''{x:Date.UTC(%s,%d,%s), y:%.3f},
				''' %(data.y, int(data.m)-1, data.d, price))

	# 出售后盈利记录，主要在显示时会标成红色
	# self.cache['assets'] 记录资产变化
	def recordSellWin(self, data, income):
		# self.recordDD(data, 3)
		record = '''{x:Date.UTC(%s,%d,%s), y:%.3f},
				''' %(data.y, int(data.m)-1, data.d, income)
		if self.outputTradeRecord:
			self.cache['TRWin'].append(record)

		if self.outputAssetRecord:
			self.cache['assets'].append(record)

	# 出售后亏损记录，主要在显示时会标成绿色
	# self.cache['assets'] 记录资产变化
	def recordSellLose(self, data, income):
		record = '''{x:Date.UTC(%s,%d,%s), y:%.3f},
				''' %(data.y, int(data.m)-1, data.d, income)
		if self.outputTradeRecord:
			self.cache['TRLose'].append(record)

		if self.outputAssetRecord:
			self.cache['assets'].append(record)

	# 添加交易记录到series
	def addTradeRecord(self):
		if self.outputTradeRecord:
			self.cache['TRBuy'].append(']')
			self.cache['TRWin'].append(']')
			self.cache['TRLose'].append(']')
			self.s['tradeRecords'].append(self.makeSerie('column', 'Buy', self.cache['TRBuy'], 2, 'black'))
			self.s['tradeRecords'].append(self.makeSerie('column', 'Win', self.cache['TRWin'], 2, 'red'))
			self.s['tradeRecords'].append(self.makeSerie('column', 'Lose', self.cache['TRLose'], 2, 'green'))

	# 添加资产变化记录到series
	def addAssetRecord(self):
		if self.outputAssetRecord:
			self.cache['assets'].append(']')
			self.s['assets'].append(self.makeSerie('column', 'Assets', self.cache['assets']))

	# 添加回撤记录到series
	def addDrawdownRecord(self):
		if self.outputDrawdownRecord:
			self.cache['drawdowns'].append(']')
			self.s['drawdowns'].append(self.makeSerie('column', 'Drawdown', self.cache['drawdowns'], 1))

	def addTradeTimes(self, num = 1):
		self.allTimes = self.allTimes + num

	def addWinTimes(self, num = 1):
		self.winTimes = self.winTimes + num

	def addLoseTimes(self, num = 1):
		self.loseTimes = self.loseTimes + num

	def makeOperation(self, assetCtrl, baseAsset):
		self.op = Operation(assetCtrl, baseAsset)

	def checkBuy(self, index, data):
		# 检查是否涨停 
		# if self.tradeState == SD.STOP_BUY:
		# 	return False

		diff = Math.increase(self.lastData.end, data.end, True) #(float(data.end) / float(self.lastData.end) - 1) * 100
		if diff >= 10.1:
			sss = 'Gain is over 10%%, %s %s' %(data.getDate(), diff)
			raise TypeError(sss)
		elif diff >= 9.5:
			return False

		return self.op.canBuy(data)

	def checkSell(self, index, data):
		# 检查是否跌停 
		diff =  Math.increase(self.lastData.end, data.end, True) #(float(data.end) / float(self.lastData.end) - 1) * 100
		if diff <= -10.1:
			raise TypeError('Gain is over -10%%, %s %s' %(data.getDate(), diff))
		elif diff <= -9.5:
			return False

		if self.tradeState == SD.NOTHING:
			return False
		if self.beginTradeData.getDate() == data.getDate():
			False

		return self.op.canSell()

	def buy(self, data, infos = [], delay = 0, price = None):
		if not delay == 0:
			pass

		if price is None:
			price = data.end
			
		result, count, num = self.op.buy(price)
		
		if result:
			action = ''
			if self.tradeState == SD.NOTHING:
				self.l.log('\n\nOperation %s' %self.index)
				self.l.log('\n\t%s' %(self.allTimes+1))
				self.l.log('\tBuy:')
				self.tradeState = SD.BUY
				self.lastBuyIndex = self.curIndex 
				action = u'买入'
				self.mode1Cache['beginPrice'] = float(price)
				self.beginTradeData = data
				self.beginTradeAsset = self.op.getTotalAsset(data.end)
				self.updateHighestClosePrice(price, True)
				self.updateLowestClosePrice(price, True)
			elif self.tradeState == SD.BUY:
				self.l.log('\n\tOverweight:')
				action = u'加仓'
			# elif self.tradeState == SD.STOP_BUY:
			# 	self.l.log('\n\nOperation %s' %self.index)
			# 	self.l.log('\tContinue Buy:')
			# 	self.tradeState = SD.BUY
			# 	action = u'续买'
				# return
			self.recordBuy(data, num)
			self.l.log('\t%s-%s-%s' %(data.y, data.m, data.d))
			self.l.logs(infos)
			self.l.log('\tStock count : %s, Price : %s, Total : %s' %(count, price, num))
			self.l.log('\tLeft money : %s' %self.op.getAsset())

			self.outPutData['tradeData'].append({
				'date':data.getDate(), 
				'action':action, 
				'count':count,
				'price':price,
				'cost':num,
				'remain':self.op.getAsset(),
				'difference':'',
				'percent':''})

			self.closeMa.append(
				{
				'date':data.getDate(),
				'price':float(price),
				'ma':data.ma
				})

			if self.lastBuyPoint == 0:
				self.lastBuyPoint = round(float(price), 3)
			# raw_input()
			return result, num

		return False, 0, 'ERROR'

	# def tempSell(self, data):
	# 	self.mode1Cache['sellPrice'] = float(data.end)
	# 	self.mode1Cache['isActive'] = True
	# 	self.outPutData['tradeData'].append({
	# 			'date':data.getDate(), 
	# 			'action':u'暂卖', 
	# 			'count':0,
	# 			'price':data.end,
	# 			'cost':'',
	# 			'remain':'',
	# 			'difference':'',
	# 			'percent':''})

	# def continueBuy(self, data):
	# 	self.mode1Cache['continuePrice'] = float(data.end)
	# 	self.outPutData['tradeData'].append({
	# 			'date':data.getDate(), 
	# 			'action':u'续回', 
	# 			'count':0,
	# 			'price':data.end,
	# 			'cost':'',
	# 			'remain':'',
	# 			'difference':'',
	# 			'percent':''})

	# def cleanMode1Cache(self):
	# 	self.mode1Cache = {
	# 		'beginPrice':'', 
	# 		'sellPrice':'',
	# 		'continuePrice':'',
	# 		'endPrice':'',
	# 		'isActive':False}

	def sell(self, data, infos = []):
		# 单次持仓最大收盘价涨幅
		gain = Math.increase(self.beginTradeData.end, self.highestClosePrice, True)  #((self.highestClosePrice / float(self.beginTradeData.end)) - 1) * 100
		gain = round(gain, 2)
		
		# 单次持仓最大收盘价亏损
		# 根据总资产变化来计算，对于单次买入或者加仓都能适用
		deficit = Math.increase(self.beginTradeAsset, self.lowestAsset, True) #((self.lowestAsset / self.beginTradeAsset) - 1) * 100
		deficit = round(deficit, 2)
		# 单次持仓最大收盘价浮盈
		# 根据总资产变化来计算，对于单次买入或者加仓都能适用
		surplus = Math.increase(self.beginTradeAsset, self.highestAsset, True) #((self.highestAsset / self.beginTradeAsset) - 1) * 100
		surplus = round(surplus, 2)

		result, baseAsset, difference, detail, count, cost = self.op.sell(data)
		
		if result:
			self.lastSellIndex = self.curIndex
			self.lastBuyPoint = 0
			

			self.l.log('\n\tSell:')
			self.l.log('\t%s-%s-%s' %(data.y, data.m, data.d))
			self.l.logs(infos)
			self.l.log('\tProfit : %s' %difference)

			self.addTradeTimes()
			num = round(difference/baseAsset*100, 2)
			self.resultCache['num'].append(num)
			self.resultCache['data'].append(data)

			self.l.log('\tTotal money : %s, Increasing rate : %s%%' %(self.op.getAsset(), num))
			self.logDetail(detail)

			if difference > 0:
				self.addWinTimes()
				self.recordSellWin(data, self.op.getAsset())
				self.isLastTimeWin = True
			elif difference < 0:
				self.addLoseTimes()
				self.recordSellLose(data, self.op.getAsset())
				self.isLastTimeWin = False
			else:
				self.l.log( 'Not Win Not Loss...')
				self.isLastTimeWin = True
				# return False, 0

			self.mode1Cache['endPrice'] = float(data.end)

			self.outPutData['buySellDay'].append(
				{
					'beginDate':self.beginTradeData.getDate(),
					'endDate':data.getDate(),
					'day':self.lastSellIndex - self.lastBuyIndex + 1, 
					'result':self.isLastTimeWin,
					'deficit':deficit,
					'surplus':surplus,
					'num':num
					}
				)
			self.outPutData['closeMaPic'].append({'data':self.closeMa, 'result':self.isLastTimeWin})
			# if not self.isLastTimeWin:
			# 	print self.closeMa
			# 	return {}
			self.closeMa = []

			self.recordAssets(data, self.op.getAsset(), num)
			self.recordDD(data, 3)
			self.tradeState = SD.NOTHING

			self.outPutData['tradeData'].append({
				'date':data.getDate(), 
				'action':u'卖出', 
				'count':count,
				'price':data.end,
				'cost':cost,
				'remain':self.op.getAsset(),
				'difference':difference,
				'percent':num,
				})

			
			# if gain < 0.1 and not self.beginTradeData.getDate() in ['2011-08-04']:
			# 	print self.beginTradeData.getDate()
			# 	raise TypeError('gain is ')
			self.beginTradeData = None
			self.beginTradeAsset = None
			self.outPutData['highestGain'].append(gain)
			# raw_input()
			return True, difference

		return False, 0

	def makeListCache(self, cache, chartType, name, addEnd = True, y = -1, color = ''):
		l = []
		for x in cache:
			if addEnd:
				cache[x].append(']')
			
			l.append(self.makeSerie(chartType, name+x, cache[x], y = y, color = color))

		return l

	def makeSerie(self, chartType, name, data, y = -1, color = ''):
		string = ''.join(data)

		seriesString = '''{
                type: '%s',
                name: '%s',
                data: %s,''' %(chartType, name, string)

		if y > 0:
			seriesString = seriesString + '''
			yAxis:%d,''' %y

		if len(color) > 0:
			seriesString = seriesString + '''
			color:'%s',''' %color

		seriesString = seriesString + '},'

		return seriesString

	def addOHLCCache(self, cache, stockData):
		cache.append('''[Date.UTC(%s,%d,%s), %s, %s, %s, %s],
				''' %(stockData.y, int(stockData.m)-1, stockData.d, stockData.begin, stockData.max, stockData.min, stockData.end))

	def addDict(self, cache, stockData, dictionay):
		for x in dictionay:
			if x not in cache:
				cache[x] = ['[']
			cache[x].append('''[Date.UTC(%s,%d,%s), %.3f],
				''' %(stockData.y, int(stockData.m)-1, stockData.d, dictionay[x]))

	def logDetail(self, details):
		self.l.log( '\n\tDetail:')
		for detail in details:
			self.l.log('\tBasePrice:%s, NowPrice:%s, Cost:%s, Difference:%s, Increasing rate : %s%%' %(detail['basePrice'], detail['nowPrice'], detail['cost'], detail['difference'], detail['percent']))

	def analysisResult(self):
		if self.outputOHLC:
			self.ohlcCache.append(']')
			self.s['series'].append(self.makeSerie('candlestick', 'name', self.ohlcCache))

		if self.outputMA:
			self.s['series'].extend(self.makeListCache(self.maCache, 'line', 'MA-'))

		if self.outputMMAX:
			self.s['series'].extend(self.makeListCache(self.maxCache, 'line', 'MAX-'))

		if self.outputMMIN:
			self.s['series'].extend(self.makeListCache(self.minCache, 'line', 'MIN-'))

		if self.outputATR:
			self.s['atrs'].extend(self.makeListCache(self.atrCache, 'column', 'ATR-', y = 1))

		if self.outputFR:
			self.s['frrs'].extend(self.makeListCache(self.frCacheR, 'column', 'FR Red-', y = 1, color = 'red'))
			self.s['frgs'].extend(self.makeListCache(self.frCacheG, 'column', 'FR Green-', y = 1, color = 'green'))
			self.s['frws'].extend(self.makeListCache(self.frCacheW, 'column', 'FR White-', y = 1, color = 'black'))

			self.s['frls'].extend(self.makeListCache(self.frlCache, 'column', 'FRL-', y = 2))
			self.s['frps'].extend(self.makeListCache(self.frpsCache, 'column', 'FRP-', y = 1))

		if self.outputAFR:
			self.s['afrs'].extend(self.makeListCache(self.afrCache, 'column', 'AFR-', y = 1))

		totalAsset = self.op.getTotalAsset(self.lastEffectData.end)
		self.l.log('Programe Finish...')
		self.l.log('%s %s' %(self.stock.getCode(), NL.getName(self.stock.getCode())))
		self.l.log('%s - %s' %(self.beginDate, self.endDate))
		self.l.log('Begin Money : %s' %self.beginAsset)
		self.l.log('Left Money  : %s' %totalAsset)

		# 输赢次数
		self.l.log( 'win:%d, lose:%d, all:%d' %(self.winTimes, self.loseTimes, self.allTimes))
		# 单次最大盈利幅度
		profitST = max(self.bigCache['percents'])
		profitSTData = self.bigCache['datas'][self.bigCache['percents'].index(profitST)]
		self.l.log('Max Profit Single Times : %s%%,  %s' %(profitST, profitSTData.date))
		# 单次最大亏损幅度
		lossST = min(self.bigCache['percents'])
		lossSTData = self.bigCache['datas'][self.bigCache['percents'].index(lossST)]
		self.l.log('Max Loss Single Times : %s%%  %s' %(lossST, lossSTData.date))

		# maxProfixDict, maxLossDict = self.maxProfixAndLoss()
		# # 最大连续盈利
		# self.l.log('maxProfix : %s  %s-%s' %(maxProfixDict['p'], maxProfixDict['begin'].date, maxProfixDict['end'].date))
		# # 最大连续亏损
		# self.l.log('maxLoss : %s  %s-%s' %(maxLossDict['p'], maxLossDict['begin'].date, maxLossDict['end'].date))

		maxWinTimes, maxLoseTimes = self.getMaxWinAndLoseTimes()
		self.l.log('Max Continuous Profit Times : %s' %maxWinTimes)
		self.l.log('Max Continuous Loss Times : %s' %maxLoseTimes)

		cagr = Math.CAGR(totalAsset, self.beginAsset, self.getYearList())
		self.l.log('CAGR : %s%s' %(cagr, '%'))

		avgOperationCount = float(self.allTimes) / len(self.getYearList())
		self.l.log('meanOperationCount : %s times/year' %round(avgOperationCount, 2))

		self.l.log('avgFluctuateRange : %s' %self.stock.getAvgFluctuateRange())

		# 结果
		self.result['beginDate'] = self.beginDate
		self.result['endDate'] = self.endDate
		self.result['baseAsset'] = self.beginAsset
		self.result['asset'] = totalAsset
		self.result['cagr'] = cagr
		self.result['avgFluctuateRange'] = self.stock.getAvgFluctuateRange()

		self.outPutData['highestGain'].sort()
		# print self.outPutData['highestGain']


	def getResult(self):
		return self.result

	# 返回参与投资的年份列表
	def getYearList(self):
		array = []
		for obj in self.outPutData['dailyAssetsSortByYear']:
			array.append(int(obj.keys()[0]))
		return array
		
	# def maxProfixAndLoss(self):
	# 	maxProfix, maxLoss, maxTemp = 0, 0, 0
	# 	maxProfixBeginData, maxProfixEndData = None, None
	# 	maxLossBeginData, maxLossEndData = None, None
	# 	lastNum = 0
	# 	mode = '-'
	# 	index = 0
	# 	lastData, tempData, beginData, endData = None, None, None, None

	# 	lastestYear = self.assetsCache['years'][-1]
	# 	lastestData = self.assetsCache[lastestYear]['d'][-1]

	# 	for year in self.assetsCache['years']:
	# 		item = self.assetsCache[year]
	# 	 	moneys = item['m']
	# 	 	datas = item['d']

	# 	 	for money in moneys:
	# 	 		data = datas[moneys.index(money)]
	# 	 		if index == 0:
	# 	 			tempData = data
	# 	 			lastData = data
	# 	 			lastNum = money
	# 	 			index = index + 1
	# 	 			continue

	# 	 		if index == 1:
	# 	 			if money > lastNum:
	# 	 				mode = '+'
	# 	 			elif money < lastNum:
	# 	 				mode = '-'
	# 	 			else:
	# 	 				self.l.log('!'*100)
	# 	 				return 'error'
	# 	 			maxTemp = lastNum

	# 	 		if id(data) == id(lastestData):
	# 	 			num = (money - maxTemp) / maxTemp * 100

	# 	 			if num > 0 and num > maxProfix:
	# 	 				maxProfix = round(num, 2)
	# 	 				maxProfixBeginData = tempData
	# 	 				maxProfixEndData = data
	# 	 			elif num < 0 and num < maxLoss:
	# 	 				maxLoss = round(num, 2)
	# 	 				maxLossBeginData = tempData
	# 	 				maxLossEndData = data
	# 	 			continue

	# 	 		if money > lastNum:
	# 	 			if mode == '-':
	# 	 				num = (lastNum - maxTemp) / maxTemp * 100
	# 	 				if num < maxLoss:
	# 	 					maxLoss = round(num, 2)
	# 	 					maxLossBeginData = tempData
	# 	 					maxLossEndData = lastData
	# 	 				maxTemp = lastNum
	# 	 				# print 'maxTemp'
	# 	 				# print tempData.date, '-', lastData.date
	# 	 				# print 'num :', num
	# 	 				# raw_input()
	# 	 				tempData = lastData
	# 	 				mode = '+'
	# 	 		elif money < lastNum:
	# 	 			if mode == '+':
	# 	 				num = (lastNum - maxTemp) / maxTemp * 100
	# 	 				if num > maxProfix:
	# 	 					maxProfix = round(num, 2)
	# 	 					maxProfixBeginData = tempData
	# 	 					maxProfixEndData = lastData
	# 	 				maxTemp = lastNum
	# 	 				# print 'maxTemp'
	# 	 				# print tempData.date, '-', lastData.date
	# 	 				# print 'num :', num
	# 	 				# raw_input()
	# 	 				tempData = lastData
	# 	 				mode = '-'
	# 	 		else:
	# 	 			self.l.log('!'*100)
	# 	 			return 'error'
	# 	 		lastData = data
	# 	 		lastNum = money
	# 	 		index = index + 1
		 	

	# 	# return maxProfix, maxProfixBeginData, maxProfixEndData, maxLoss, maxLossBeginData, maxLossEndData
	# 	return {'p':maxProfix, 'begin':maxProfixBeginData, 'end':maxProfixEndData}, {'p':maxLoss, 'begin':maxLossBeginData, 'end':maxLossEndData}


	# 记录持仓过程中最高价及资产最高值
	def updateHighestClosePrice(self, price, replace = False):
		price = float(price)
		asset = self.op.getTotalAsset(price)
		if replace:
			self.highestClosePrice = price
			self.highestAsset = asset
			return

		if price > self.highestClosePrice:
			self.highestClosePrice = price

		if asset > self.highestAsset:
			self.highestAsset = asset

	# 记录持仓过程中最低价及资产最低值
	def updateLowestClosePrice(self, price, replace = False):
		price = float(price)
		asset = self.op.getTotalAsset(price)
		if replace:
			self.lowestClosePrice = price
			self.lowestAsset = asset
			return

		if price < self.lowestClosePrice:
			self.lowestClosePrice = price

		if asset < self.lowestAsset:
			self.lowestAsset = asset

	# 连续盈利、亏损的最大交易次数
	def getMaxWinAndLoseTimes(self):
		maxWinTimes = 0 # 最大连续盈利次数
		maxLoseTimes = 0 # 最大连续亏损次数
		winTimes = 0 # 连赢次数
		loseTimes = 0 # 连亏次数
		mode = '+'
		for item in self.resultCache['num']:
			if item >= 0:
				if mode == '+':
					winTimes = winTimes + 1
				else:
					if maxLoseTimes < loseTimes:
						maxLoseTimes = loseTimes
					loseTimes = 0
					winTimes = 1
					mode = '+'
			else:
				if mode == '-':
					loseTimes = loseTimes + 1
				else:
					if maxWinTimes < winTimes:
						maxWinTimes = winTimes
					winTimes = 0
					loseTimes = 1
					mode = '-'

		return maxWinTimes, maxLoseTimes
	# 输出execle
	def makeXLS(self):
		array = []
		datas = []

		# 交易数据&资产表
		for tradeData in self.outPutData['tradeData']:
			difference = '' if tradeData['difference'] == '' else tradeData['difference']
			modeDiff = tradeData['modeDiff'] if 'modeDiff' in tradeData else ''
			percent = '' if tradeData['percent'] == '' else '%s%%' %(tradeData['percent'])
			datas.append([
				tradeData['date'],
				tradeData['action'],
				tradeData['count'],
				tradeData['price'],
				tradeData['cost'],
				tradeData['remain'],
				# difference,
				tradeData['difference'],
				percent,
				modeDiff
				])
		array.append({'name':'Test', 'data':datas})
		array.append({'name':'DailyAssets', 'data':self.outPutData['dailyAssets']})

		# 年资产变动
		datas = [[u'年份', u'年初', u'年尾', u'收益率']]
		for obj in self.outPutData['dailyAssetsSortByYear']:
			for key, value in obj.items():
				datas.append([
					int(key), 
					value[0][-1],
					value[-1][-1],
					'%.3f%s' %((value[-1][-1]/value[0][-1]-1)*100, '%')
				])
		array.append({'name':'YearAssets', 'data':datas})

		# 持仓时间
		datas = [[u'开始', u'结束', u'天数', u'最大浮亏', u'最大浮盈', u'盈亏', u'输赢']]
		for obj in self.outPutData['buySellDay']:
			datas.append([
				obj['beginDate'], 
				obj['endDate'], 
				obj['day'], 
				obj['deficit'], 
				obj['surplus'],
				obj['num'],
				obj['result']
				])
		array.append({'name':u'所有天数', 'data':datas})

		# 赢得持仓时间
		datas = [[u'开始', u'结束', u'天数', u'最大浮亏', u'最大浮盈', u'盈亏', u'输赢']]
		for obj in self.outPutData['buySellDay']:
			if obj['result']:
				datas.append([
				obj['beginDate'], 
				obj['endDate'], 
				obj['day'], 
				obj['deficit'], 
				obj['surplus'],
				obj['num'],
				obj['result']
				])
		array.append({'name':u'赢天数', 'data':datas})

		# 输的持仓时间
		datas = [[u'开始', u'结束', u'天数', u'最大浮亏', u'最大浮盈', u'盈亏', u'输赢']]
		for obj in self.outPutData['buySellDay']:
			if not obj['result']:
				datas.append([
				obj['beginDate'], 
				obj['endDate'], 
				obj['day'], 
				obj['deficit'], 
				obj['surplus'],
				obj['num'],
				obj['result']
				])
		array.append({'name':u'输天数', 'data':datas})

		# 赢的收盘和MA数据
		_title = [u'日期', u'收盘价'] + self.stock.getMas_title()
		datas = [_title]
		for obj in self.outPutData['closeMaPic']:
			if obj['result']:
				for _obj in obj['data']:
					_data = [_obj['date'], _obj['price']]
					for _ma in _obj['ma']:
						_data.append(_obj['ma'][_ma])
					datas.append(_data)
				datas.append('')
		array.append({'name':'WinCM', 'data':datas})

		# 输的收盘和MA数据
		_title = [u'日期', u'收盘价'] + self.stock.getMas_title()
		datas = [_title]
		for obj in self.outPutData['closeMaPic']:
			if not obj['result']:
				for _obj in obj['data']:
					_data = [_obj['date'], _obj['price']]
					for _ma in _obj['ma']:
						_data.append(_obj['ma'][_ma])
					datas.append(_data)
				datas.append('')
		array.append({'name':'LoseCM', 'data':datas})

		
		XlsHelper('Test.xls').create(array)


	def save(self):
		self.analysisResult()
		self.makeXLS()
		
		return
		# names = {'atrs':['Atrs.js'],
		# 		 'tradeRecords':['TradeRecords.js'],
		# 		 'assets':['Assets.js'],
		# 		 'series':['Data1.js'],
		# 		 'drawdowns':['Drawdowns.js'],
		# 		 'frrs':['Frrs.js'],
		# 		 'frgs':['Frgs.js'],
		# 		 'frws':['Frws.js'],
		# 		 'afrs':['Afrs.js'],
		# 		 'frls':['Frls.js'],
		# 		 'frps':['Frps.js']}

		# if self.m.isSave:
		# 	folder = 'Schrodinger/Case/' + self.fileName
		# 	if not os.path.exists(folder):
		# 		os.mkdir(folder)

		# 	time = datetime.today()
		# 	sndFolderName = '%s.%s.%s %s-%s-%s' %(time.year, time.month, time.day, time.hour, time.minute, time.second)
		# 	path = folder + '/' + sndFolderName
		# 	os.mkdir(path)

		# 	names['atrs'].append(path+'/Atrs.js')
		# 	names['tradeRecords'].append(path+'/TradeRecords.js')
		# 	names['assets'].append(path+'/Assets.js')
		# 	names['series'].append(path+'/Data1.js')

		# 	self.l.saveLog(path+'/Case1.txt')

		# if self.outputATR:
		# 	self.outPutContentByList('atrs', names['atrs'])

		# if self.outputTradeRecord:
		# 	self.addTradeRecord()
		# 	self.outPutContentByList('tradeRecords', names['tradeRecords'])

		# if self.outputAssetRecord:
		# 	self.addAssetRecord()
		# 	self.outPutContentByList('assets', names['assets'])

		# if self.outputDrawdownRecord:
		# 	self.addDrawdownRecord()
		# 	self.outPutContentByList('drawdowns', names['drawdowns'])

		# if self.outputFR:
		# 	self.outPutContentByList('frrs', names['frrs'])
		# 	self.outPutContentByList('frgs', names['frgs'])
		# 	self.outPutContentByList('frws', names['frws'])

		# 	self.outPutContentByList('frls', names['frls'])
		# 	self.outPutContentByList('frps', names['frps'])

		# if self.outputAFR:
		# 	self.outPutContentByList('afrs', names['atrs'])

		# self.outPutContentByList('series', names['series'])

		

	# 根据list生成需要保存的内容,并输出
	def outPutContentByList(self, key, names):
		self.s[key].append(']')
		content = ''.join(self.s[key])

		for name in names:
			self.m.save(name, content)

	def run(self):
		self.introduce()
		self.initStock()
		self.analysis()
		self.outPut()
		self.save()
