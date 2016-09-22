#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 突破均线卖出 '''
class S10(BaseBS):
	"""docstring for S10"""
	def __init__(self):
		super(S10, self).__init__()
		
		self.formulas = [
			Formula(22),
		]