from datadog import initialize, statsd

import os

statsd_host = os.environ['STATSD_HOST']

options = {
    'statsd_host': statsd_host,
    'statsd_port': 8125
}

initialize(**options)
