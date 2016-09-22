#coding=utf8

import StateDefine as SD
import StockMathTool as SMathTool

class Formula(object):
	"""docstring for Formula"""
	def __init__(self, findex = 0, options = {}):
		super(Formula, self).__init__()
		self.findex = findex

		self.reLine = None # 补仓先(虽然止损，可能还没跌出趋势，这时候在这个点补仓)
		self.keepLine = None # 止损线

		self.result = {'buyPoint':0, 'sellPoint':0}

		self.mmax = options['mmax'] if 'mmax' in options else ''
		self.ma = options['ma'] if 'ma' in options else ''
		self.atrKey = options['atrKey'] if 'atrKey' in options else ''
		self.atrTimes = options['atrTimes'] if 'atrTimes' in options else ''
		self.formula1 = options['f1'] if 'f1' in options else []
		self.formula2 = options['f2'] if 'f2' in options else []
		self.case1 = options['c1'] if 'c1' in options else ''
		self.case2 = options['c2'] if 'c2' in options else ''
		self.std = options['std'] if 'std' in options else ''
		self.stdTimes = options['stdTimes'] if 'stdTimes' in options else ''
		self.ma1 = options['ma1'] if 'ma1' in options else ''
		self.ma2 = options['ma2'] if 'ma2' in options else ''

		f1Info = self.addMsg(self.formula1)
		f2Info = self.addMsg(self.formula2)

		c1Info = self.case1.getIntroduce() if not self.case1 == '' else ''
		c2Info = self.case2.getIntroduce() if not self.case2 == '' else ''

		self.funcs = [
			self.c1,  # 0 涨停
			self.b1,  # 1 突破最大值开仓
			self.b2,  # 2 N倍ATR加仓
			self.b3,  # 3 突破均线开仓
			self.s1,  # 4 最高点突破ATR清仓
			self.s2,  # 5 向下突破均线清仓
			self.c2,  # 6 跌停
			self.c3,  # 7 震荡屏蔽功能
			self.s3,  # 8 开仓位跌到ATR时清仓；开仓位之上跌破均线清仓
			self.s4,  # 9 开仓位突破ATR清仓
			self.b4,  # 10 均线突破，但是根据波动率自动调整均线
			self.b5,  # 11 有保底的均线突破
			self.s5,  # 12 有保底的均线突破
			self.b6,  # 13 均值回归
			self.s6,  # 14 均值回归
			self.b7,  # 15 双线法
			self.s7,  # 16 双线法
			self.b8,  # 17 下跌补仓
			self.s8,  # 18 下跌补仓配套卖出计划
			self.b9,  # 19 加权均线突破买入
			self.s9,  # 20 加权均线突破卖出
			self.b10, # 21 跌破均线买入
			self.s10, # 22 突破均线卖出
		]

		self.msgs = [
			u'检查是否涨停',  # 0
			u'参数:%s日最大收盘价;策略：突破最大值则买入' %(self.mmax),  # 1
			u'参数:%s倍ATR，%s日ATR;策略：突破%sATR则加仓' %(self.atrTimes, self.atrKey, self.atrTimes),  # 2
			u'参数:%s日均价;策略：突破均价则买入' %(self.ma),  # 3
			u'参数:%s日ATR，%s倍ATR;策略：最高点向下突破%s个ATR卖出' %(self.atrKey, self.atrTimes, self.atrTimes),  # 4
			u'参数:%s日MA;策略：昨日向下突破%s日MA卖出' %(self.ma, self.ma),  # 5
			u'检查是否跌停',  # 6
			u'策略：震荡屏蔽\n组合1:%s;组合2:%s' %(c1Info, c2Info),  # 7
			u'参数:%s倍ATR，%s日ATR,%s日均价;策略：向下突破%s个ATR卖出,开仓位之上，向下突破%s日MA卖出' %(self.atrTimes, self.atrKey, self.ma, self.atrTimes, self.ma), # 8
			u'参数:%s倍ATR，%s日ATR;策略：买入点向下突破%s个ATR卖出 ' %(self.atrTimes, self.atrKey, self.atrTimes), # 9
			u'策略：突破均价则买入,但是根据波动率自动调整均线', # 10
			u'策略：有保底的均线突破买入, MA : %s' %(self.ma), # 11
			u'策略：有保底的均线突破卖出, MA : %s' %(self.ma), # 12
			u'策略：均值回归-买入', # 13
			u'策略：均值回归-卖出', # 14
			u'策略：双线法-买入, MA1 : %s, MA2 : %s' %(self.ma1, self.ma2), # 15
			u'策略：双线法-卖出, MA1 : %s, MA2 : %s' %(self.ma1, self.ma2), # 16
			u'策略：下跌补仓', # 17
			u'策略：下跌补仓配套卖出计划', # 18
			u'策略：加权均线突破买入', # 19
			u'策略：加权均线突破卖出', # 20
		]

	def analyseObj(self, obj):
		self.obj = obj
		self.data = obj['data'] if 'data' in obj else ''
		self.tradeState = obj['tradeState'] if 'tradeState' in obj else ''
		self.index = obj['index'] if 'index' in obj else ''
		self.lastData = obj['stock'].stockDatas[self.index-1] if 'stock' in obj else ''
		self.lastBuyPoint = obj['lastBuyPoint'] if 'lastBuyPoint' in obj else ''
		self.highestPrice = obj['highestPrice'] if 'highestPrice' in obj else ''
		self.isLastTimeWin = obj['isLastTimeWin'] if 'isLastTimeWin' in obj else ''
		self.lastSellIndex = obj['lastSellIndex'] if 'lastSellIndex' in obj else ''
		self.beginPrice	= float(obj['beginPrice']) if 'beginPrice' in obj else ''
		self.cost = float(obj['cost']) if 'cost' in obj else ''
		self.assetCtrl = obj['assetCtrl'] if 'assetCtrl' in obj else ''
		self.operation = obj['operation'] if 'operation' in obj else ''

		# print 'findex', self.findex, self.ma
		# print 'ma', self.lastData.ma, self.lastData.atr
		if self.findex in [3, 5, 8, 10, 11, 12]:
			self.maBuyPoint = self.lastData.ma[self.ma] + (1*self.lastData.atr['20'])
			self.maSellPoint = float(self.lastData.ma[self.ma])

		else:
			self.maBuyPoint = None
			self.maSellPoint = None


	#--------------------------------------------------
	#---------------------------CHECK
	def c1(self):
		# 检查是否涨停 
		# 0
		pass

	def c2(self):
		# 检查是否跌停
		# 6
		pass
		
	def c3(self):
		#震荡屏蔽
		# 7
		# 旧的不用了
		pass



	#--------------------------------------------------
	#---------------------------BUY
	def b1(self):
		# 最大值突破
		# 1
		if self.tradeState == SD.NOTHING:
			if float(self.lastData.end) >= self.lastData.mmax[self.mmax]:
				infos = ['\tClose Price : %s is higher than MMAX-%s : %.3f' %(self.lastData.end, self.mmax, self.lastData.mmax[self.mmax])]
				return {'r':True, 'm':infos}

		return {'r':False}

	def b2(self):
		# 突破ATR加仓
		# 2
		if self.tradeState == SD.BUY:
			buyPoint = self.lastBuyPoint + self.lastData.atr[self.atrKey] * self.atrTimes
			if float(self.lastData.end) > buyPoint:
				infos = ['\tClose Price : %s is over 0.5ATR : %.3f' %(self.lastData.end, buyPoint),
						 '\tATR-%s : %s' %(self.atrKey, self.lastData.atr[self.atrKey])]
				return {'r':True, 'm':infos}
		return {'r':False}

	def b3(self):
		# 均线突破
		# 3
		atrTimes = 1
		# if (self.index-1) - self.lastSellIndex <= 20 and (not self.isLastTimeWin):
		# 	# 震荡
		# 	atrTimes = 1
		# else:
		# 	# 没震荡
		# 	atrTimes = 1

		usedData = self.data
		# usedData = self.lastData
		if self.tradeState == SD.NOTHING:
			buyPoint = usedData.ma[self.ma] + (atrTimes*usedData.atr['20'])
			if float(usedData.end) >= buyPoint:
				infos = ['\tClose Price : %s is higher than buyPoint MA-%s : %.3f' %(self.data.end, self.ma, buyPoint)]
				return {'r':True, 'm':infos}
		return {'r':False}

	def b4(self):
		# 突破均价则买入,但是根据波动率自动调整均线
		# 10	
		fr = self.lastData.fluctuateRange['20']
		if fr > 2.0 and fr < 3.0:
			self.ma = '60'
			return self.b3()
		else:
			return {'r':False}

	def b5(self):
		# 有保底的均线突破
		# 11

		self.result['buyPoint'] = self.maBuyPoint

		if self.tradeState == SD.NOTHING:
			# print self.maBuyPoint
			if float(self.lastData.end) >= self.maBuyPoint: 
				infos = ['\tClose Price : %s is higher than buyPoint MA-%s : %.3f' %(self.lastData.end, self.ma, self.maBuyPoint)]
				return {'r':True, 'm':infos}


		return {'r':False}

	def b6(self):
		# 均值回归
		# 13
		# buyPoint = self.lastData.std[self.std] * self.stdTimes
		# difference = self.lastData.ma[self.ma] - float(self.lastData.end)
		buyPoint = self.data.std[self.std] * self.stdTimes
		difference = self.data.ma[self.ma] - float(self.data.end)
		if difference > buyPoint:
			infos = ['\\tdifference : %s is higher than buyPoint %s std-%s : %.3f' %(difference, self.stdTimes, self.std, buyPoint)]
			return {'r':True, 'm':infos}

		return {'r':False}

	def b7(self):
		# 双线法
		# 15
		point1 = self.data.ma[self.ma1]
		point2 = self.data.ma[self.ma2]

		if point1 > point2:
			infos = ['\\MA1 : %s is higher than MA2 %s' %(point1, point2)]
			return {'r':True, 'm':infos}

		return {'r':False} 


	def b8(self):
		# 17 下跌补仓
		# 均线以下
		ratio = [0.95, 0.9025, 0.8573, 0.814]
		# 均线以下
		if float(self.lastData.end) < self.lastData.ma[self.ma]:
			# 仓位未满
			if not self.assetCtrl.isFullCount():
				curCount = self.assetCtrl.getCurCount()
				if curCount == 0:
					bias = self.lastData.bias[self.ma]
					if bias < 0 and abs(bias) > self.lastData.meanFR['20']:
						return {'r':True, 'm':[]}
				else:
					diff = self.operation.checkTotalFar(self.lastData.end)
					if diff < -0.09:
						return {'r':False}

					# if ratio[curCount-1] * self.operation.getFirstBuyPrice() < float(self.data.end) :
					# if ratio[curCount-1] * self.operation.getFirstBuyPrice() > float(self.lastData.end) :
					if 0.95 * self.operation.getLastBuyPrice() > float(self.lastData.end) :
						# print ratio[curCount-1] * self.operation.getFirstBuyPrice(), float(self.data.end)
						return {'r':True, 'm':[]}

		return {'r':False}

	def b9(self):
		# 19 加权均线突破买入
		result, weightMaBuyPoint = SMathTool.compareWeigthMa(self.lastData, self.lastData)
		if self.tradeState == SD.NOTHING:
			if result: 
				infos = ['\tClose Price : %s is higher than buyPoint WeightMa : %.3f' %(self.lastData.end, weightMaBuyPoint)]
				return {'r':True, 'm':infos}

		return {'r':False}

	# 21 跌破均线买入
	def b10(self):
		tradeState = self.getTradeState()
		# 如果没有仓位了
		if self.assetCtrl.isFullCount():
			return {'r':False}
		if tradeState == SD.STOCK_SELL:
			# 跌破当天购买
			return {'r':True, 'm':[]}
		elif tradeState == SD.STOCK_NOTHING:
			return {'r':True, 'm':[]}
		return {'r':False}
		


	#--------------------------------------------------------------------------------------------------------------------------------------
	#---------------------------SELL
	def s1(self):
		# 最高点向下突破ATR
		# 4
		sellPoint = self.highestPrice - self.lastData.atr[self.atrKey]*self.atrTimes
		if float(self.lastData.end) < sellPoint:
			infos = ['\tClose Price : %s is lower than sellPoint : %.3f' %(self.lastData.end, sellPoint)]
			return {'r':True, 'm':infos}
		return {'r':False}

	def s2(self):
		# 向下突破均线
		# 5
		# if float(self.data.end) >= self.lastData.ma[self.ma]:
		# 	return {'r':False}

		if float(self.lastData.end) < float(self.lastData.ma[self.ma]):
			infos = ['\tClose Price : %s is lower than MA-%s : %.3f' %(self.lastData.end, self.ma, self.lastData.ma[self.ma])]
			return {'r':True, 'm':infos}
		return {'r':False}

	def s3(self):
		# 开仓位跌到ATR时清仓；开仓位之上跌破均线清仓
		# 8
		sellPoint = self.lastBuyPoint - self.lastData.atr[self.atrKey] * self.atrTimes
		if float(self.lastData.end) < sellPoint:
			infos = ['\tClose Price : %s is lower than sellPoint : %.3f' %(self.lastData.end, sellPoint)]
			return {'r':True, 'm':infos}
		elif float(self.lastData.end) > self.lastBuyPoint:
			return self.s2()
		return {'r':False}

	def s4(self):
		# 买入点向下跌破ATR清仓
		# 9
		sellPoint = self.lastBuyPoint - self.lastData.atr[self.atrKey] * self.atrTimes
		if float(self.lastData.end) < sellPoint:
			infos = ['\tClose Price : %s is lower than sellPoint : %.3f' %(self.lastData.end, sellPoint)]
			return {'r':True, 'm':infos}

		return {'r':False}

	def s5(self):
		# 有保底的均线突破
		# 12

		self.result['sellPoint'] = self.maSellPoint
		
		if float(self.lastData.end) < self.maSellPoint:
			infos = ['\tClose Price : %s is lower than MA-%s : %.3f' %(self.lastData.end, self.ma, self.maSellPoint)]
			return {'r':True, 'm':infos}
		return {'r':False}


		# return self.s2()

	def s6(self):
		# 均值回归
		# 14
		sellPoint = self.data.ma[self.ma]
		self.result['sellPoint'] = sellPoint
		if float(self.data.end) > sellPoint:
			infos = ['\tClose Price : %s is higher than sellPoint MA-%s : %.3f' %(self.data.end, self.ma, sellPoint)]
			return {'r':True, 'm':infos}

		if float(self.data.end) < self.lastBuyPoint - self.data.atr['20']:
			return {'r':True, 'm':[]}

		return {'r':False}

	def s7(self):
		# 双线法
		# 16
		point1 = self.data.ma[self.ma1]
		point2 = self.data.ma[self.ma2]

		if point1 < point2:
			infos = ['\\MA1 : %s is lower than MA2 %s' %(point1, point2)]
			return {'r':True, 'm':infos}

		return {'r':False} 

	def s8(self):
		# 18 下跌补仓配套卖出计划
		if float(self.data.end) > self.lastData.ma[self.ma]:
			return {'r':True, 'm':[]}

		# 浮亏9个点以上退出
		diff = self.operation.checkTotalFar(self.data.end)
		if diff < -0.09:
			return {'r':True, 'm':[]}

		# diff = self.operation.checkTotalFarP(self.data.end)
		# if diff < 0 and abs(diff) > self.data.meanFR['20']:
		# 	return {'r':True, 'm':[]}

		return {'r':False}

	def s9(self):
		# 20 加权均线突破卖出
		result, weightMaSellPoint = SMathTool.compareWeigthMa(self.lastData, self.lastData)
		if not result: 
			infos = ['\tClose Price : %s is lower than buyPoint WeightMa : %.3f' %(self.lastData.end, weightMaSellPoint)]
			return {'r':True, 'm':infos}

		return {'r':False}

	def s10(self):
		# 22 突破均线卖出
		pass



	def addMsg(self, formulas):
		# 叠加其他公式的介绍
		result = ''
		for f in formulas:
			result = result + f.getMsg() + '\n'

		return result

	def getIndex(self):
		return self.findex

	def getMsg(self):
		return self.msgs[self.getIndex()]

	def check(self, obj):
		self.analyseObj(obj)
		fun = self.funcs[self.getIndex()]
		return fun()

	def getResult(self):
		return self.result

	def getBuyPoint(self):
		return self.getResult()['buyPoint']

	def getSellPoint(self):
		return self.getResult()['sellPoint']

if __name__ == '__main__':
	f = Formula(options = {'mmax':20, 'atrKey':20})
	f.check('a')