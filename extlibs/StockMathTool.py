#coding=utf8

# 判断当前收盘价是否大于加权均线
def compareWeigthMa(curData, baseData):
	point = baseData.getWMa()
	return float(curData.end) > point, point

def compareMaBuy(curData, baseData):
	point = getMaPlusATR(baseData)
	# print point
	return float(curData.end) > point, point

def compareMaSell(curData, baseData, price = None):
	point = getMaOrPrice(baseData, price)
	return float(curData.end) < point, point

def getMaPlusATR(data, maKey = '20', atrKey = '20'):
	# 20日均线 + 1倍ATR
	return data.ma[maKey] + (1*data.atr[atrKey])

def getMa(data, maKey = '20'):
	return data.ma[maKey]
	
# 获取20日均线和价格减ATR中较高的一个值，用于退出趋势计算
def getMaOrPrice(data, price = None, maKey = '20', atrKey = '20'):
	# 20日均线
	point = float(data.ma[maKey])
	# 买入价减去ATR
	if not (price == None or price == ''):
		price = float(price) - data.atr[atrKey]
		if price > point:
			point = price
	return point