from kiteconnect import KiteConnect, KiteTicker
# from pandas import DataFrame
import pandas as pd
from datetime import datetime, timedelta
import talib
import icecream

if __name__=='__main__':
    api_key = open('api_key.txt','r').read()
    api_secret = open('api_secret.txt', 'r').read()

    kite = KiteConnect(api_key=api_key)
    
    # if already have the access token
    access_token = open('access_token.txt', 'r').read()

    kite.set_access_token(access_token)

    # if if opening for the first time in the day

    print(kite.login_url())
    data = kite.generate_session("", api_secret=api_secret)
    print(data['access_token'])
    kite.set_access_token(data['access_token'])

    with open('access_token.txt', 'w') as ak:
        ak.write(data['access_token'])

    from_date = datetime.strftime(datetime.now()-timedelta(100), '%y-%m-%d')
    to_date = datetime.today().strftime('%y-%m-%d')
    interval ='5minute'

    tokens= {738561 :'RELIANCE'}
    
    while True:
        if (datetime.now().second == 0) and (datetime.now().minute % 5 == 0):
            for token in tokens:
                records=kite.historical_data(token,from_date,to_date, interval)
                df = pd.DataFrame(records)
                df.drop(df.tail(1).index, inplace=True)

                open =df['open'].values     
                close =df['close'].values     
                high =df['high'].values     
                low =df['low'].values     
                volume =df['volume'].values

                sma5 =talib.SMA(close,5)
                sma20 =talib.SMA(close,20)

                icecream.ic(sma5[-1])
                icecream.ic(sma20[-1])

                price=kite.ltp('NSE'+tokens[token])
                icecream.ic(price)

                ltp =price['NSE:' + tokens[token]]['last_price']

                # BUY order
                if (sma5[-2]<sma20 and sma5[-1]>sma20[-1]):
                    buy_order_id=kite.place_order(variety=kite.VARIETY_REGULAR,
                                                exchange=kite.EXCHANGE_NSE,
                                                order_type=kite.ORDER_TYPE_MARKET,
                                                tradingsymbol=tokens[token],
                                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                                quantity=1,
                                                # price=ltp,
                                                # squareoff=10,
                                                # stoploss=2,
                                                # trailing_stoploss=1,
                                                validity=kite.VALIDITY_DAY,
                                                product=kite.PRODUCT_MIS)
                icecream.ic(kite.orders())

                # SELL order
                if (sma5[-2]>sma20 and sma5[-1]<sma20[-1]):
                    sell_order_id=kite.place_order(variety=kite.VARIETY_REGULAR,
                                                exchange=kite.EXCHANGE_NSE,
                                                order_type=kite.ORDER_TYPE_MARKET,
                                                tradingsymbol=tokens[token],
                                                transaction_type=kite.TRANSACTION_TYPE_SELL,
                                                quantity=1,
                                                # price=ltp,
                                                # squareoff=10,
                                                # stoploss=2,
                                                # trailing_stoploss=1,
                                                validity=kite.VALIDITY_DAY,
                                                product=kite.PRODUCT_MIS)
                icecream.ic(kite.orders())

