#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 跌破均线买入 '''
class B10(BaseBS):
	"""docstring for B10"""
	def __init__(self):
		super(B10, self).__init__()
		
		self.formulas = [
			Formula(21),
		]