# -*- coding: utf-8 -*-
from dataapiclient import Client
if __name__ == "__main__":
    try:
        client = Client()
        client.init('b6a5eded39d16731278aa4646ec96128304f0ccab0850bbdacebcdcada4dbb7f')
        # url = '/api/market/getMktEqud.json?field=&beginDate=20050101&endDate=&secID=&ticker=000333&isOpen=1'
        # url = '/api/market/getMktFundd.json?field=&beginDate=20150501&endDate=20150616&secID=&ticker=510050&tradeDate='
        # url = '/api/market/getMktIdxd.json?field=&beginDate=20160101&endDate=20160110&indexID=&ticker=399970&tradeDate='
        url = '/api/market/getMktIdxd.json?field=&beginDate=20050101&endDate=&indexID=&ticker=399967&tradeDate='
        code, result = client.getData(url)
        if code==200:
            print result
        else:
            print code
            print result
    except Exception, e:
        raise e