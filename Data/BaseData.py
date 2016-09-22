#coding=utf8

from MTool import MTool as M

class BaseData(object):
	"""docstring for BaseData"""
	def __init__(self, id, date, begin, maxPrice, minPrice, end, money, count):
		super(BaseData, self).__init__()
		self.id = id
		self.date = date #日期
		self.begin = begin #开盘价
		self.max = maxPrice #最高价
		self.min = minPrice #最低价
		self.end = end #收盘价
		self.count = count #成交量
		self.turnover = money #成交额
		self.y = ''
		self.m = ''
		self.d = ''
		self.timestamp = self.str2timestamp(date) #时间
		self.ma = {} #均线
		self.mmax = {} #X日内收盘价最高值
		self.mmin = {} #X日内收盘价最小值
		self.tr = 0 #真实波幅
		self.atr = {} #平均真实波幅
		self.tomax = {} # N日内交易额最高值
		self.tomin = {} # N日内交易额最小值
		self.fr = {} # fluctuate rate 波动率
		self.afr = {} # 准备弃用
		self.fluctuateRange = {} #atr / ma 波动幅度，衡量波动占价格的幅度
		self.frSum = {} # 波动率累加，带有方向性
		self.frLimit = {} # 限定时间内波动强度
		self.frl = {}
		self.meanFR = {} # 60日波幅
		self.std = {} # 标准差
		self.pastDayMa = {} # 过去某天的均价，用来计算增长率
		self.bias = {} # 偏离率
		self.tradeState = None #交易状态 STOCK_BUY、STOCK_HOLD、STOCK_SELL、STOCK_NOTHING
		self.maMean = None #均线下最大跌幅平均数
		self.maMeanUp = None #maMean+标准差
		self.maMeanDown = None #maMean-标准差

		self.maPosition = 0


	def getTradeState(self):
		return self.tradeState

	# 获取X天股价增长率
	def getIncrease(self, key = '20'):
		key = str(key)
		rate = (float(self.end) / self.pastDayMa[key]) - 1
		return rate

	# 获取股价加权增长率，以20、40日计算
	def getWeightIncrease(self):
		i20 = self.getIncrease('20')
		i40 = self.getIncrease('40')
		return i20 * 0.6 + i40 * 0.4

	# 获取X天股价增长率,返回百分比形式
	# increase rate percent
	def getIRP(self, key = '20'):
		rate = round(self.getIncrease(key) * 100, 2)
		return rate

	# 获取股价加权增长率,返回百分比形式
	def getWIRP(self):
		return round(self.getWeightIncrease() * 100, 2)

	# 获取加权均线
	def getWMa(self, wm1 = {'key':'20', 'wight':0.6}, wm2 = {'key':'40', 'wight':0.4}):
		ma1 = self.ma[wm1['key']] * wm1['wight']
		ma2 = self.ma[wm2['key']] * wm2['wight']
		return round(ma1 + ma2, 2)

	def str2timestamp(self, string):
		dates = string.split('/')
		m = M()
		self.y = dates[0]
		self.m = dates[1]
		self.d = dates[2]
		timestamp = m.makeTime(dates[0], dates[1], dates[2])
		return timestamp

	def getDate(self):
		return '%s-%s-%s' %(self.y, self.m, self.d)

	# return Year & Month
	def getYM(self):
		return '%s%s' %(self.y, self.m)

	def getYear(self):
		return self.y

	def getSQL(self):
		# sql = '''insert into m_stock (date, tt, begin, max, min, end, count, money) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' %(self.date, self.timestamp, self.begin, self.max, self.min, self.end, self.count, self.turnover)
		sql = '''insert into m_stock values (%d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' %(self.id, self.date, self.timestamp, self.begin, self.max, self.min, self.end, self.count, self.turnover)
		return sql
		