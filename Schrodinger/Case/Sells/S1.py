#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

class S1(BaseBS):
	"""docstring for S1"""
	def __init__(self, atrKey = '20', atrTimes = 2):
		super(S1, self).__init__()
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		# self.introduce = '''S1参数:%s日ATR，%s倍ATR；\nS1策略：昨日向下突破%s个ATR卖出''' %(self.atrKey, self.atrTimes, self.atrTimes)
		self.formulas = [
			# Formula(6),
			Formula(4, options = {'atrTimes':atrTimes, 'atrKey':atrKey})
		]