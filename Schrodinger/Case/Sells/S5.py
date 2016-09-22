#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

''' 有保底的均线突破卖出 '''
''' 估计只能和B5配套 '''
class S5(BaseBS):
	"""docstring for S5"""
	def __init__(self, ma = '20'):
		super(S5, self).__init__()
		ma = str(ma)
		
		self.formulas = [
			Formula(12, options = {'ma':ma})
		]