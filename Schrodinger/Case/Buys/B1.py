#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

class B1(BaseBS):
	"""docstring for B1"""
	def __init__(self, mmax = '10', atrKey = '20', atrTimes = 0.5):
		super(B1, self).__init__()
		mmax = str(mmax)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		# self.introduce = '''B1参数:%s日最大收盘价，%s日ATR，%s倍ATR；\nB1策略：突破最大值则买入，突破%sATR则加仓''' %(self.mmax, self.atrKey, self.atrTimes, self.atrTimes)

		self.formulas = [
			# Formula(0),
			Formula(1, options = {'mmax':mmax}),
			Formula(2, options = {'atrTimes':atrTimes, 'atrKey':atrKey}),
		]