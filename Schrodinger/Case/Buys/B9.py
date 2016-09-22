#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 加权均线突破买入 '''
class B9(BaseBS):
	"""docstring for B9"""
	def __init__(self):
		super(B9, self).__init__()
		
		self.formulas = [
			Formula(19),
		]