import logging
from kiteconnect import KiteTicker, KiteConnect

logging.basicConfig(level=logging.DEBUG)

# Initialise
api_key = open('api_key.txt','r').read()
access_token = open('access_token.txt','r').read()


# kite = KiteConnect(api_key=api_key)
# print(kite.login_url())
# data = kite.generate_session("", api_secret=api_key)
# print(data['access_token'])
# kite.set_access_token(data['access_token'])

# with open('access_token.txt', 'w') as ak:
#     ak.write(data['access_token'])


kws = KiteTicker("api_key", "access_token")

def on_ticks(ws, ticks):
    # Callback to receive ticks.
    logging.debug("Ticks: {}".format(ticks))

def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [738561])

def on_close(ws, code, reason):
    # On connection close stop the main loop
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()

# Assign the callbacks.
kws.on_ticks = on_ticks
kws.on_connect = on_connect
kws.on_close = on_close

# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()