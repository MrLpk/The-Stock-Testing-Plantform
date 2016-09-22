#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

class B2(BaseBS):
	"""docstring for B2"""
	def __init__(self, ma = '20', atrKey = '20', atrTimes = 0.5):
		super(B2, self).__init__()
		ma = str(ma)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		# self.introduce = '''B2参数:%s日均价，%s日ATR，%s倍ATR；\nB2策略：突破均价则买入，突破%sATR则加仓''' %(self.ma, self.atrKey, self.atrTimes, self.atrTimes)
		self.formulas = [
			# Formula(0),
			Formula(3, options = {'ma':ma}),
			Formula(2, options = {'atrTimes':atrTimes, 'atrKey':atrKey}),
		]