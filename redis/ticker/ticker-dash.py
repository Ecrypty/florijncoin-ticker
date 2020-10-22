#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
import simplejson as json
import redis
from datetime import datetime
import time
from statistics import mean

#from ISStreamer.Streamer import Streamer
from twython import Twython, TwythonError

from config.role import *
from config.twitter import *
from config.rkeys import *

def shiptoredis(datatoship):
    rx.lpush(QUE_NAME, json.dumps(datatoship))

def get_espochtime():
    return time.time()

def get_tooktime(START):
    return (time.time() - START)

def make_request(URL, CHECK_STRRING):
    USERAGET = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'
    headers = {'user-agent': USERAGET}

    try:
        response = requests.get(URL, headers=headers, timeout=(2,5))
        try:
            if response.status_code == requests.codes.ok and len(response.text) > 2:
                if isinstance(response.json(), list):
                    if CHECK_STRRING in response.json()[0]:
                        return response.json()[0]

                else:
                    if CHECK_STRRING in response.json():
                        return response.json()

        except Exception as e:
            print(e.args[0])
            pass

    except requests.exceptions.RequestException:
        return None

def get_poloniex():
    START         = get_espochtime()
    URL           = 'https://poloniex.com/public?command=returnTicker'
    CHECK_STRRING = 'BTC_FLRN'
    SECON_STRRING = 'USDT_FLRN'
    exsymbol      = 'poloniex'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if SECON_STRRING in rawjson:
            valbtc = round(float(rawjson[CHECK_STRRING]['last']), 5)
            valusd = round(float(rawjson[SECON_STRRING]['last']), 2)
            if valbtc > 0 and valusd > 0:
                florijncoinbtc[exsymbol] = valbtc
                florijncoinusd[exsymbol] = valusd
                florijncoinbtc_ttook[exsymbol]  = florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
                florijncoinbtc_tstamp[exsymbol] = florijncoinusd_tstamp[exsymbol] = epoch00

def get_exmo():
    START         = get_espochtime()
    URL           = 'https://api.exmo.com/v1/ticker/'
    CHECK_STRRING = 'FLRN_BTC'
    SECON_STRRING = 'FLRN_USD'
    exsymbol      = 'exmo'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if SECON_STRRING in rawjson:
            valbtc = round(float(rawjson[CHECK_STRRING]['last_trade']), 5)
            valusd = round(float(rawjson[SECON_STRRING]['last_trade']), 2)
            if valbtc > 0 and valusd > 0:
                florijncoinbtc[exsymbol] = valbtc
                florijncoinusd[exsymbol] = valusd
                florijncoinbtc_ttook[exsymbol]  = florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
                florijncoinbtc_tstamp[exsymbol] = florijncoinusd_tstamp[exsymbol] = epoch00


def get_bittrex():
    START         = get_espochtime()
    URL           = 'https://bittrex.com/api/v1.1/public/getticker?market=btc-florijncoin'
    CHECK_STRRING = 'success'
    exsymbol      = 'bittrex'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == True:
            valbtc = round(float(rawjson['result']['Last']), 5)
            if valbtc > 0:
                florijncoinbtc[exsymbol] = valbtc
                florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
                florijncoinbtc_tstamp[exsymbol] = epoch00

def get_btcebtc():
    START         = get_espochtime()
    URL           = 'https://btc-e.com/api/3/ticker/dsh_btc'
    CHECK_STRRING = 'dsh_btc'
    exsymbol      = 'btce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valbtc = round(float(rawjson[CHECK_STRRING]['last']), 5)
        if valbtc > 0:
            florijncoinbtc[exsymbol] = valbtc
            florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
            florijncoinbtc_tstamp[exsymbol] = epoch00


def get_btceusd():
    START         = get_espochtime()
    URL           = 'https://btc-e.com/api/3/ticker/dsh_usd'
    CHECK_STRRING = 'dsh_usd'
    exsymbol      = 'btce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valusd = round(float(rawjson[CHECK_STRRING]['last']), 2)
        if valusd > 0:
            florijncoinusd[exsymbol] = valusd
            florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
            florijncoinusd_tstamp[exsymbol] = epoch00


def get_xbtcebtc():
    START         = get_espochtime()
    URL           = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHBTC'
    CHECK_STRRING = 'Symbol'
    exsymbol      = 'xbtce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == 'DSHBTC':
            valbtc = round(float(rawjson['BestBid']), 5)
            if valbtc > 0:
               florijncoinbtc[exsymbol] = valbtc 
               florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
               florijncoinbtc_tstamp[exsymbol] = epoch00

def get_xbtceusd():
    START         = get_espochtime()
    URL           = 'https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/DSHUSD'
    CHECK_STRRING = 'Symbol'
    exsymbol      = 'xbtce'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        if rawjson[CHECK_STRRING] == 'DSHUSD':
            valusd = round(float(rawjson['BestBid']), 2)
            if valusd > 0:
                florijncoinusd[exsymbol] = valusd
                florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
                florijncoinusd_tstamp[exsymbol] = epoch00

def get_yobit():
    START         = get_espochtime()
    URL           = 'https://yobit.net/api/2/florijncoin_btc/ticker'
    CHECK_STRRING = 'ticker'
    exsymbol      = 'yobit'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valbtc = round(float(rawjson['ticker']['last']), 5)
        if valbtc > 0:
            florijncoinbtc[exsymbol] = valbtc    
            florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
            florijncoinbtc_tstamp[exsymbol] = epoch00


def get_livecoinbtc():
    START         = get_espochtime()
    URL           = 'https://api.livecoin.net/exchange/ticker?currencyPair=FLRN/BTC'
    CHECK_STRRING = 'last'
    exsymbol      = 'livecoin'
    rawjson       = make_request(URL, CHECK_STRRING)

    if rawjson:
        valbtc = round(float(rawjson[CHECK_STRRING]), 5)
        if valbtc > 0:
            florijncoinbtc[exsymbol] = valbtc
            florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
            florijncoinbtc_tstamp[exsymbol] = epoch00

def get_livecoinusd():
    START         = get_espochtime()
    URL           = 'https://api.livecoin.net/exchange/ticker?currencyPair=FLRN/USD'
    CHECK_STRRING = 'last'
    exsymbol      = 'livecoin'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valusd = round(float(rawjson[CHECK_STRRING]), 2)
        if valusd > 0:
            florijncoinusd[exsymbol] = valusd
            florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
            florijncoinusd_tstamp[exsymbol] = epoch00

#
def get_bitfinex_florijncoinbtc():
    START         = get_espochtime()
    URL           = 'https://api.bitfinex.com/v1/pubticker/DSHBTC'
    CHECK_STRRING = 'last_price'
    exsymbol      = 'bitfinex'
    rawjson       = make_request(URL, CHECK_STRRING)

    if rawjson:
        valbtc = round(float(rawjson[CHECK_STRRING]), 5)
        if valbtc > 0:
            florijncoinbtc[exsymbol] = valbtc
            florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
            florijncoinbtc_tstamp[exsymbol] = epoch00

def get_bitfinex_florijncoinusd():
    START         = get_espochtime()
    URL           = 'https://api.bitfinex.com/v1/pubticker/DSHUSD'
    CHECK_STRRING = 'last_price'
    exsymbol      = 'bitfinex'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valusd = round(float(rawjson[CHECK_STRRING]), 2)
        if valusd > 0:
            florijncoinusd[exsymbol] = valusd
            florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
            florijncoinusd_tstamp[exsymbol] = epoch00

#
def get_kraken_florijncoinbtc():
    START         = get_espochtime()
    URL           = 'https://api.kraken.com/0/public/Ticker?pair=FLRNXBT'
    CHECK_STRRING = 'result'
    exsymbol      = 'kraken'
    rawjson       = make_request(URL, CHECK_STRRING)

    if rawjson:
        valbtc = round(float(rawjson.get('result').get('FLRNXBT').get('b')[0]), 5)
        if valbtc > 0:
            florijncoinbtc[exsymbol] = valbtc
            florijncoinbtc_ttook[exsymbol] =  get_tooktime(START)
            florijncoinbtc_tstamp[exsymbol] = epoch00


def get_kraken_florijncoinusd():
    START         = get_espochtime()
    URL           = 'https://api.kraken.com/0/public/Ticker?pair=FLRNUSD'
    CHECK_STRRING = 'result'
    exsymbol      = 'kraken'
    rawjson       = make_request(URL, CHECK_STRRING)
    if rawjson:
        valusd = round(float(rawjson.get('result').get('FLRNUSD').get('b')[0]), 2)
        if valusd > 0:
            florijncoinusd[exsymbol] = valusd
            florijncoinusd_ttook[exsymbol] =  get_tooktime(START)
            florijncoinusd_tstamp[exsymbol] = epoch00

#

#-----------
def check_redis():
    if HOST_ROLE == 'MASTER':
        SETINEL_HOST = MASTER_SETINEL_HOST
        REDIS_MASTER = MASTER_REDIS_MASTER

    else:
        SETINEL_HOST = SLAVE_SETINEL_HOST
        REDIS_MASTER = SLAVE_REDIS_MASTER        

    s = redis.StrictRedis(host=SETINEL_HOST, port=26379, socket_timeout=0.1)
    try:
        h = s.execute_command("SENTINEL get-master-addr-by-name mymaster")[0].decode("utf-8")
        print(h)
        if h == REDIS_MASTER:
            print('Other host is redis master')
            sys.exit()

        else:
            pass

    except Exception as e:
        print(e.args[0])
        sys.exit()

#--------------
def check_update():
    cur_time = time.time()
    lasttstamp = json.loads(r.get(r_KEY_FLRN_BTC_PRICE))
    if 'tstamp' in lasttstamp:
        lastupdate = lasttstamp['tstamp']

        if cur_time - lastupdate > 270 and cur_time - lastupdate < 330:
            twitter.update_status(status='ticker florijncoin has prob -1')

        if cur_time - lastupdate > 570 and cur_time - lastupdate < 630:
            twitter.update_status(status='ticker florijncoin has prob -2')


#-----------------#
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# redis
POOL = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=POOL)

#
# redis2
POOLX = redis.ConnectionPool(host='192.168.10.2', port=16379, db=0)
rx = redis.StrictRedis(connection_pool=POOLX)

#
florijncoinbtc = {}
florijncoinbtc_ttook = {}
florijncoinbtc_tstamp = {}

florijncoinusd = {}
florijncoinusd_ttook = {}
florijncoinusd_tstamp = {}


now = datetime.now()
epoch00 = int(time.mktime(now.timetuple())) - now.second

#
try:
    check_redis()

except Exception as e:
    print(e.args[0])

try:
    check_update()
    get_poloniex()
    get_exmo()
    get_bittrex()
    get_btcebtc()
    get_btceusd()
    get_xbtcebtc()
    get_xbtceusd()
    get_yobit()
    get_livecoinbtc()
    get_livecoinusd()
    get_bitfinex_florijncoinbtc()
    get_bitfinex_florijncoinusd()
    get_kraken_florijncoinbtc()
    get_kraken_florijncoinusd()


    #
    l_florijncoinbtc = []
    for key in florijncoinbtc:
        l_florijncoinbtc.append(florijncoinbtc[key])

    l_florijncoinusd = []
    for key in florijncoinusd:
        l_florijncoinusd.append(florijncoinusd[key])

    if len(l_florijncoinbtc) < 3:
        florijncoinbtc['avg'] = round(mean(sorted(l_florijncoinbtc)), 5)        
    else:
        florijncoinbtc['avg'] = round(mean(sorted(l_florijncoinbtc)[1:-1]), 5)
       
    if len(l_florijncoinusd) < 3:
        florijncoinusd['avg'] = round(mean(sorted(l_florijncoinusd)), 2)
    else: 
        florijncoinusd['avg'] = round(mean(sorted(l_florijncoinusd)[1:-1]), 2)
    
    florijncoinbtc['tstamp'] = florijncoinusd['tstamp'] = int(time.time())

    # redis
    try:
        pipe = r.pipeline()
        pipe.set(r_KEY_FLRN_BTC_PRICE, json.dumps(florijncoinbtc, sort_keys=True))
        pipe.set(r_KEY_FLRN_USD_PRICE, json.dumps(florijncoinusd, sort_keys=True))
        pipe.set(r_KEY_FLRN_BTC_PRICE_TSTAMP, json.dumps(florijncoinbtc_tstamp, sort_keys=True))
        pipe.set(r_KEY_FLRN_USD_PRICE_TSTAMP, json.dumps(florijncoinusd_tstamp, sort_keys=True))
        pipe.zadd(r_SS_FLRN_BTC_PRICE, epoch00, str(epoch00) + ':' + str(florijncoinbtc['avg']))
        pipe.zadd(r_SS_FLRN_USD_PRICE, epoch00, str(epoch00) + ':' + str(florijncoinusd['avg']))
        response = pipe.execute()

    except Exception as e:
        print(e.args[0])
        pass

    # ISS
    try:
#        streamer = Streamer(bucket_name=ISS_BUCKET_NAME, bucket_key=ISS_BUCKET_KEY, access_key=ISS_BUCKET_AKEY, buffer_size=50)
#        streamer.log_object(florijncoinbtc, key_prefix=ISS_PREFIX_FLRNBTC, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNBTC,
            "epoch": epoch00,
            "bucket": florijncoinbtc
        }
        shiptoredis(datatoship)
#        streamer.log_object(florijncoinusd, key_prefix=ISS_PREFIX_FLRNUSD, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNUSD,
            "epoch": epoch00,
            "bucket": florijncoinusd
        }
        shiptoredis(datatoship)
#        streamer.log_object(florijncoinbtc_ttook, key_prefix=ISS_PREFIX_FLRNBTC_TT, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNBTC_TT,
            "epoch": epoch00,
            "bucket": florijncoinbtc_ttook
        }
        shiptoredis(datatoship)
#        streamer.log_object(florijncoinbtc_tstamp, key_prefix=ISS_PREFIX_FLRNBTC_TS, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNBTC_TS,
            "epoch": epoch00,
            "bucket": florijncoinbtc_tstamp
        }
        shiptoredis(datatoship)
#        streamer.log_object(florijncoinusd_ttook, key_prefix=ISS_PREFIX_FLRNUSD_TT, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNUSD_TT,
            "epoch": epoch00,
            "bucket": florijncoinusd_ttook
        }
        shiptoredis(datatoship)
#        streamer.log_object(florijncoinusd_tstamp, key_prefix=ISS_PREFIX_FLRNUSD_TS, epoch=epoch00)
        datatoship = {
            "bucket_name": ISS_BUCKET_NAME,
            "key_prefix": ISS_PREFIX_FLRNUSD_TS,
            "epoch": epoch00,
            "bucket": florijncoinusd_tstamp
        }
        shiptoredis(datatoship)
#        streamer.flush()
#        streamer.close()

    except Exception as e:
        print(e.args[0])
        pass

except Exception as e:
    print(e.args[0])

except KeyboardInterrupt:
    sys.exit()
