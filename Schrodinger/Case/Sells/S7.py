#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

''' 双线法卖出 '''

class S7(BaseBS):
	"""docstring for S7"""
	def __init__(self, ma1 = '5', ma2 = '20'):
		super(S7, self).__init__()
		ma1 = str(ma1)
		ma2 = str(ma2)
		
		self.formulas = [
			Formula(16, options = {'ma1':ma1, 'ma2':ma2})
		]