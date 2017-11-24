import redis

ip = 'localhost'
r1 = redis.Redis(host=ip, port=6379, db=1)

print r1.get(1500)