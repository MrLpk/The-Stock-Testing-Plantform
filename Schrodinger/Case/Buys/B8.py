#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

''' 下跌补仓 '''

class B8(BaseBS):
	"""docstring for B8"""
	def __init__(self, ma = '20'):
		super(B8, self).__init__()
		ma = str(ma)

		
		self.formulas = [
			Formula(17, options = {'ma':ma})
		]