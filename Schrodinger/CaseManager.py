#coding=utf8

from CaseFrame import CaseFrame
from Turtle import Turtle
from Elephant import Elephant
from Segment import Segment
from B1 import B1
from B2 import B2
from B3 import B3
from B4 import B4
from B5 import B5
from B6 import B6
from B7 import B7
from B8 import B8
from B9 import B9
from S1 import S1
from S2 import S2
from S3 import S3
from S4 import S4
from S5 import S5
from S6 import S6
from S7 import S7
from S8 import S8
from S9 import S9
from Stock import Stock
from GlobalConfig import GlobalConfig

class CaseManager(object):
	"""docstring for CaseManager"""
	def __init__(self, index = None, maNum = None, doOutPut = True):
		super(CaseManager, self).__init__()
		GlobalConfig().set('mode', 'Smaug')
		if index == None:
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
			# index = 'SH000016' #上证50
			# index = 'SZ399006' # 创业板指
			# index = 'SZ399976' # CS新能车
			# index = 'SZ399997' # 中证白酒
			# index = 'SZ399975' # 证券公司
			# index = 'SZ399707' # CSSW证券
			index = 'SH000300' # 沪深300
		atrKey = '20'
		mmax = ['10']
		mmin = ['20']
		# ma = ['5', '10', '20', '40', '60']
		ma = ['5', '20']
		self.beginAsset = 10000000

		if maNum == None:
			maNum = 20

		if not str(maNum) in ma:
			ma.append(str(maNum))


		# action = {
		# 	'buy':B2(maNum), # 均线突破开仓，N倍ATR加仓
		# 	'sell':S2(maNum), # 向下突破均线清仓
		# 	'asset':Elephant(tax = 0), # 莽撞法
		# 	'stock':Stock(atr = [atrKey], max = mmax, min = mmin, ma = ma, index = index)
		# }

		# action = {
		# 	'buy':B8(maNum), # 下跌补仓
		# 	'sell':S8(maNum), # 均线上卖出
		# 	'asset':Segment(totalCount = 5, tax = 0), # 分段
		# 	'stock':Stock(atr = [atrKey], max = mmax, min = mmin, ma = ma, index = index)
		# }


		# action = {
		# 	'buy':B9(), # 加权均线突破买入
		# 	'sell':S9(), # 加权均线突破卖出
		# 	'asset':Elephant(tax = 0), # 莽撞法
		# 	'stock':Stock(atr = [atrKey], max = mmax, min = mmin, ma = ma, index = index)
		# }

		action = {
			'buy':B2(maNum), # 均线突破开仓，N倍ATR加仓
			'sell':S2(maNum), # 向下突破均线清仓
			'asset':Segment(totalCount = 5, tax = 0), # 分段
			'stock':Stock(atr = [atrKey], max = mmax, min = mmin, ma = ma, index = index)
		}
		

		# assets = [
		# 	# Turtle(atrKey = atrKey, tax = 0), # 海龟法
		# 	# Elephant(tax = 0), # 莽撞法
		# 	Segment(totalCount = 5, tax = 0) # 分段
		# ]

		# buys = [
		# 	# B1(), #最大值突破开仓，N倍ATR加仓
		# 	# B2(maNum), #均线突破开仓，N倍ATR加仓
		# 	# B3(maNum, 60), #带震荡屏蔽掉均线突破
		# 	# B4(), # 突破均价则买入,但是根据波动率自动调整均线
		# 	# B5(maNum), # 有保底的均线突破买入
		# 	# B6(std = '20', ma = '20', stdTimes = 2), # 均值回归
		# 	# B7('5', '20'), # 双线法买入
		# 	B8(maNum), #下跌补仓
		# ]

		# sells = [
		# 	# S1(), #向下突破ATR清仓
		# 	# S2(maNum), #向下突破均线清仓
		# 	# S3(ma = 20, atrKey = '20', atrTimes = 2) # 开仓位跌到ATR时清仓；开仓位之上跌破均线清仓
		# 	# S4(ma = 20, atrKey = '20', atrTimes = 2) # 开仓位跌到ATR或跌破均线清仓
		# 	# S5(maNum), # 有保底的均线突破卖出
		# 	# S6(ma = '20'), # 均值回归
		# 	# S7('5', '20') # 双线法卖出
		# 	S8(maNum), #均线上卖出
		# ]

		# stocks = [
		# 	Stock(atr = [atrKey], max = mmax, min = mmin, ma = ma, index = index)
		# ]

		self.asset = action['asset']
		self.buy = action['buy']
		self.sell = action['sell']
		self.stock = action['stock']


		self.doOutPut = doOutPut
		self.mode = 0 # 改模式


		self.isSave = False #不输出

	def run(self):
		frame = CaseFrame()
		frame.setFixMode(self.mode)
		frame.setIsSave(self.isSave)
		frame.setBeginIndex(20)
		frame.setBeginAsset(self.beginAsset)
		frame.setAssetController(self.asset)
		frame.setBuyController(self.buy)
		frame.setSellController(self.sell)
		frame.setBeginTime(2005, 01, 01)
		# frame.setEndTime(2015, 12, 31)
		frame.setStock(self.stock, self.beginAsset)

		if self.doOutPut:
			frame.outPut()
			frame.save()
		else:
			frame.analysisResult()
			# frame.makeXLS()
		return frame.getResult()