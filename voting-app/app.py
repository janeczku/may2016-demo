from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from utils import connect_to_redis
from statsd import statsd
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "In")
option_b = os.getenv('OPTION_B', "Out")
hostname = socket.gethostname()

redis = connect_to_redis("redis")
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def hello():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    vote = None

    if request.method == 'POST':
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)
        # statsd.increment('votes.submitted')
        statsd.increment('votes-submitted', tags=['vote:%s' % vote])
        statsd.set('votes-uniques', voter_id)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    statsd.increment('vote-page-views')
    return resp


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)
