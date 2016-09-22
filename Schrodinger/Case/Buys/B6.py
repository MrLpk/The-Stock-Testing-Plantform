#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

''' 均值回归买入 '''

class B6(BaseBS):
	"""docstring for B6"""
	def __init__(self, std = '20', ma = '20', stdTimes = 2):
		super(B6, self).__init__()
		std = str(std)
		ma = str(ma)
		stdTimes = float(stdTimes)

		self.formulas = [
			Formula(13, options = {'std':std, 'ma':ma, 'stdTimes':stdTimes}),
		]