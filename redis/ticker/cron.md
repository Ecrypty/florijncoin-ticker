```
* * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-btc.py && ~/florijncoin-ticker/redis/ticker/ticker-btc.py >> ~/florijncoin-ticker/logs/ticker-btc.log
* * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-florijncoin.py && ~/florijncoin-ticker/redis/ticker/ticker-florijncoin.py >> ~/florijncoin-ticker/logs/ticker-florijncoin.log
* * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-graph.py && ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-graph.py  >> ~/florijncoin-ticker/logs/ticker-update-florijncoin-btc-graph.log
* * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-usd-graph.py && ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-usd-graph.py  >> ~/florijncoin-ticker/logs/ticker-update-florijncoin-usd-graph.log
*/5 * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-5min.py && ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-5min.py >> ~/florijncoin-ticker/logs/ticker-update-florijncoin-btc-5min.log
01 * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-explorer.py && ~/florijncoin-ticker/redis/ticker/ticker-explorer.py >> ~/florijncoin-ticker/logs/ticker-explorer.log
01 * * * * test -x ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-1h.py && ~/florijncoin-ticker/redis/ticker/ticker-update-florijncoin-btc-1h.py >> ~/florijncoin-ticker/logs/ticker-update-florijncoin-btc-1h.log
```
