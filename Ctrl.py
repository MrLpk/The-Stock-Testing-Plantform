#coding=utf8

import Path
from CaseManager import CaseManager
class Ctrl(object):
	"""docstring for Ctrl"""
	def __init__(self):
		super(Ctrl, self).__init__()
		pass

	def start(self):
		cm = CaseManager()
		cm.run()



if __name__ == '__main__':
	ctrl = Ctrl()
	ctrl.start()
