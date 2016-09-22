#coding=utf8
# 带震荡屏蔽的均线突破，情况允许有加仓行为
from Formula import Formula
from BaseBS import BaseBS
from B2 import B2

class B3(BaseBS):
	"""docstring for B3"""
	def __init__(self, ma1 = '20', ma2 = '60', atrKey = '20', atrTimes = 0.5):
		super(B3, self).__init__()
		ma1 = str(ma1)
		ma2 = str(ma2)
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)
		
		case1 = B2(ma1, atrKey, atrTimes)
		case2 = B2(ma2, atrKey, atrTimes)
		self.formulas = [
			Formula(7, options = {'c1':case1, 'c2':case2}),
		]