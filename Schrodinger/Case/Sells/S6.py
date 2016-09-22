#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 均值回归卖出 '''

class S6(BaseBS):
	"""docstring for S6"""
	def __init__(self, ma = '20'):
		super(S6, self).__init__()
		ma = str(ma)

		self.formulas = [
			Formula(14, options = {'ma':ma})
		]
