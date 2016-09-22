#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 加权均线突破卖出 '''
class S9(BaseBS):
	"""docstring for S9"""
	def __init__(self):
		super(S9, self).__init__()
		
		self.formulas = [
			Formula(20),
		]