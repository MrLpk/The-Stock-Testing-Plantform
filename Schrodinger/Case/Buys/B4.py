#coding=utf8

from Formula import Formula
from BaseBS import BaseBS

class B4(BaseBS):
	"""docstring for B4"""
	def __init__(self, atrKey = '20', atrTimes = 0.5):
		super(B4, self).__init__()
		atrKey = str(atrKey)
		atrTimes = float(atrTimes)

		'''突破均价则买入,但是根据波动率自动调整均线'''
		self.formulas = [
			Formula(10),
			Formula(2, options = {'atrTimes':atrTimes, 'atrKey':atrKey}),
		]