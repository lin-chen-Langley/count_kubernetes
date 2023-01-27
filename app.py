import os
import time
import redis
from flask import Flask

def get_ip():
    return os.getenv('MYREDIS_HOST', 'localhost')

app = Flask(__name__)
print(get_ip())
cache = redis.Redis(host=get_ip(), port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello from Docker! I have been seen {} times.\n'.format(count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
