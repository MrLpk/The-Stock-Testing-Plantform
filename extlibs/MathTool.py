#coding=utf8

# 等差数列求和，num的值不进行计算
def AP(num):
	result = 0
	for x in xrange(1, num):
		result = result + x

	return result

def AP4(num):
	return AP(num) * 4

yearCache = []
def addCAGRYear(year):
	year = int(year)
	if not year in yearCache:
		yearCache.append(year)

# 年复合增长率
def CAGR(now, base, years = []):
	year = 0
	if isinstance(years, int):
		year = years
	else:
		if len(years) == 0:
			years = yearCache

		year = int(max(years)) - int(min(years)) + 1

	now = float(now)
	base = float(base)
	
	# print now, base, years
	result = (now/base)**(1.0/year)-1
	return round(result*100, 2)

# 计算增长
# base:原始值
# now:当前值
# isPercent:是否返回百分数
# num:小数点后保留位数
def increase(base, now, isPercent = False, num = 2):
	base = float(base)
	now = float(now)
	result = (now / base) - 1

	if isPercent:
		result = result * 100

	return round(result, num)


if __name__ == '__main__':
	# num = AP(8)

	# num = AP4(5)

	# num = CAGR(1300000, 80000, [2003,2015])

	num = increase(100, 190, num= 3)
	print num