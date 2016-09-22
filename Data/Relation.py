#coding=utf8
relation = {
	'SZ399006':[{'code':'150153', 'name':u'创业板B'}, {'code':'150244', 'name':u'创业B'}, {'code':'159915', 'name':u'创业板ETF'}],
	'SH000016':[{'code':'510050', 'name':u'50ETF'}],
	'SZ399395':[{'code':'150197', 'name':u'有色B'}],
	'SZ399970':[{'code':'150195', 'name':u'互联网B'}],
	'SZ399975':[{'code':'502012', 'name':u'证券B'}, {'code':'150201', 'name':u'券商B'}, {'code':'150224', 'name':u'证券B级'}, {'code':'150236', 'name':u'券商B级'}],
	'SZ399973':[{'code':'150206', 'name':u'国防B'}],
	'SZ399991':[{'code':'150276', 'name':u'一带一B'}],
	'SZ399997':[{'code':'150270', 'name':u'白酒B'}],
	'SZ399976':[{'code':'150212', 'name':u'新能车B'}],
	'SZ399958':[{'code':'150214', 'name':u'成长B级'}],
	'SZ399959':[{'code':'150222', 'name':u'中航军B'}],
	'SZ399393':[{'code':'150118', 'name':u'房地产B'}],
	'SZ399440':[{'code':'150288', 'name':u'钢铁B'}],
	'SH000998':[{'code':'150174', 'name':u'TMT中证B'}],
	'SZ399967':[{'code':'150182', 'name':u'军工B'}, {'code':'150187', 'name':u'军工B级'}, {'code':'502005', 'name':u'军工B'}],
	'SZ399707':[{'code':'150172', 'name':u'证券B'}],
	'SZ399394':[{'code':'150131', 'name':u'医药B'}],
	'SZ399989':[{'code':'150262', 'name':u'医疗B'}],
	'SZ399412':[{'code':'150218', 'name':u'新能源B'}],
	'SZ399986':[{'code':'150228', 'name':u'银行B'}],
	'SZ399673':[{'code':'150304', 'name':u'创业股B'}, {'code':'159949', 'name':u'创业板50'}],
	'SZ399974':[{'code':'150210', 'name':u'国企改B'}, {'code':'502008', 'name':u'国企改B'}],
	'SZ399396':[{'code':'150199', 'name':u'食品B'}],
	'sz399983':[{'code':'150208', 'name':u'地产B端'}],
	# '':[{'code':'', 'name':u''}],
}

# ignore = [
# 	'SZ399997',
# 	'SZ399396',
# ]

def getRelation(code):
	result = []
	if code in relation:
		result = relation[code]

	return result

def isIgnore(code):
	if code in ignore:
		return True

	return False