
from .redis_client import redisConObj

# Lua: atomically decrement stock if enough quantity
# KEYS[1] = stock key
# ARGV[1] = desired quantity (number)
DECR_STOCK_LUA = """
local stock = tonumber(redis.call('GET', KEYS[1]) or '-1')
local qty = tonumber(ARGV[1])
if stock == -1 then
    -- key missing
    return -2
end
if stock < qty then
    -- insufficient
    return -1
end
redis.call('DECRBY', KEYS[1], qty)
return stock - qty
"""

# register script (returns a Script object)
decr_stock_script = redisConObj.register_script(DECR_STOCK_LUA)
