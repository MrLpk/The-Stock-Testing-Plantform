#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

''' 均线上卖出 '''
''' 配合B8 '''

class S8(BaseBS):
	"""docstring for S8"""
	def __init__(self, ma = '20'):
		super(S8, self).__init__()
		ma = str(ma)
		
		self.formulas = [
			Formula(18, options = {'ma':ma})
		]