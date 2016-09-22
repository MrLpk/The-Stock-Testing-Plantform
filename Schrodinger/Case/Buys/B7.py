#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

''' 双线法买入 '''

class B7(BaseBS):
	"""docstring for B7"""
	def __init__(self, ma1 = '5', ma2 = '20'):
		super(B7, self).__init__()
		ma1 = str(ma1)
		ma2 = str(ma2)
		
		self.formulas = [
			Formula(15, options = {'ma1':ma1, 'ma2':ma2})
		]