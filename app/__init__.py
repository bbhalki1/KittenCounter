#!/usr/bin/env python

import redis
import os
from celery import Celery
from flask import Flask
from flask import render_template

REDIS_HOST = 'redis'
REDIS_PORT = 6379
KITTEN_COUNTER_METRIC = 'kitten_counter'

#template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top-secret!'

# Celery configuration
app.config['broker_url'] = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)
app.config['result_backend'] = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)


# Initialize Celery
celery = Celery(app.name, broker=app.config['broker_url'])
celery.conf.update(app.config)

# Initialize Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
r.set(KITTEN_COUNTER_METRIC, 0)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls count_kittens() every 1 seconds.
    sender.add_periodic_task(1.0, count_kittens.s(), name='Count a new kitten every second')


@celery.task
def count_kittens():
    """Background task to count kittens."""
    with app.app_context():
        r.incr(KITTEN_COUNTER_METRIC, 1)
        return r.get(KITTEN_COUNTER_METRIC)


@app.route('/', methods=['GET'])
def index():
    """A very exciting landing page."""
    print 'Inside index'
    return render_template('index.html')


@app.route('/kittens', methods=['GET'])
@app.route('/kittens/', methods=['GET'])
def view_kitten_count():
    """View the kitten counter page."""
    return render_template('kittens.html', kitten_count=r.get(KITTEN_COUNTER_METRIC))


@app.route('/secrets', methods=['GET'])
@app.route('/secrets/', methods=['GET'])
def view_secrets():
    """View a super secret page that no one should see. Shhh."""
    return render_template('secrets.html')


# if __name__ == '__main__':
#     app.run(debug=True)