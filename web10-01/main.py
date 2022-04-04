import redis
from redis_lru import RedisLRU
import timeit
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


@cache
def fib_cache(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_cache(n - 1) + fib_cache(n - 2)


starttime = timeit.default_timer()
print(f'The start: {starttime}')
fibonacci(8)
print(f'The end: {timeit.default_timer() - starttime}')

starttime = timeit.default_timer()
print(f'The start: {starttime}')
fib_cache(138)
print(f'The end: {timeit.default_timer() - starttime}')

client.set('foo', 'bar')
client.set('baz', 100)
print(client.get('foo').decode())
print(int(client.get('baz').decode()))