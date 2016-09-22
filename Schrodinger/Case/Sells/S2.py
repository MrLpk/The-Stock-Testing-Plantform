#coding=utf8
from Formula import Formula
from BaseBS import BaseBS

class S2(BaseBS):
	"""docstring for S2"""
	def __init__(self, ma = '20'):
		super(S2, self).__init__()
		ma = str(ma)
		# self.introduce = '''S2参数:%s日MA；\nS2策略：昨日向下突破%s日MA卖出''' %(ma, ma)
		self.formulas = [
			# Formula(6),
			Formula(5, options = {'ma':ma})
		]