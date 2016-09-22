#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

# 开仓位跌到ATR或跌破均线清仓
class S4(BaseBS):
	"""docstring for S4"""
	def __init__(self, ma = '20', atrKey = '20', atrTimes = 2):
		super(S4, self).__init__()
		ma = str(ma)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		
		self.formulas = [
			# Formula(6),
			Formula(9, options = {'atrTimes':atrTimes, 'atrKey':atrKey}),
			Formula(5, options = {'ma':ma})
		]