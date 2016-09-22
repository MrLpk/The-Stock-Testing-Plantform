#coding=utf8

class XlsHelper(object):
	"""docstring for XlsHelper"""
	def __init__(self, fileName):
		super(XlsHelper, self).__init__()
		self.fileName = fileName

	def create(self, datas):
		import xlwt
		workbook = xlwt.Workbook(encoding='utf-8')

		for _datas in datas:
			sheetName = _datas['name']
			data = _datas['data']
			booksheet = workbook.add_sheet(sheetName, cell_overwrite_ok=True)

			for i, row in enumerate(data):
			    for j, col in enumerate(row):
			        booksheet.write(i, j, col)

		workbook.save(self.fileName)

		print 'Save %s success ...' %self.fileName

	def read(self, index = None, tableName = None):
		import xlrd
		data = xlrd.open_workbook(self.fileName)

		if not index is None:
			return data.sheet_by_index(0)
		
		if not tableName is None:
			return data.sheet_by_name(tableName)

		return data
		