#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

# 开仓位跌到ATR时清仓；开仓位之上跌破均线清仓
class S3(BaseBS):
	"""docstring for S3"""
	def __init__(self, ma = '20', atrKey = '20', atrTimes = 2):
		super(S3, self).__init__()
		ma = str(ma)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		
		self.formulas = [
			# Formula(6),
			Formula(8, options = {'ma':ma, 'atrTimes':atrTimes, 'atrKey':atrKey})
		]