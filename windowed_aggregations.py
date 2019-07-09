#!/usr/bin/env python

# In this exapmple we have a function `publish_every_2secs` publishing a
# message every 2 senconds to topic `hopping_topic`
# We have created an agent `print_windowed_events` consuming events from
# `hopping_topic` that mutates the windowed table `values_table`

# `values_table` is a table with hopping (overlaping) windows. Each of
# its windows is 10 seconds of duration, and we create a new window every 5
# seconds.
# |----------|
#       |-----------|
#             |-----------|
#                   |-----------|

from random import random
from datetime import timedelta
import faust
import statistics

app = faust.App('windowing', broker='kafka://localhost:9092')


class Model(faust.Record, serializer='json'):
    random: float


TOPIC = 'hopping_topic'
WINDOW_SIZE = 10
WINDOW_STEP = 5

hopping_topic = app.topic(TOPIC, value_type=Model)
values_table = app.Table(
    'values_table',
    default=list
).hopping(WINDOW_SIZE, WINDOW_STEP, expires=timedelta(minutes=10))


@app.agent(hopping_topic)
async def print_windowed_events(stream):
    async for event in stream:  # noqa
        values_table['values'] += [event.random]
        values = values_table['values'].delta(WINDOW_SIZE)
        print(f'-- New Event (every 2 secs) written to hopping(10, 5) --')
        print(f'COUNT should start at 0 and after 10 secs be 5: '
              f'{len(values)}')
        print(f'SUM   should have values between 0-5: '
              f'{sum(values) if values else 0}')
        print(f'AVG   should have values between 0-1: '
              f'{statistics.mean(values) if values else 0}')
        print(f'LAST  should have values between 0-1: '
              f'{event.random}')
        print(f'MAX   should have values between 0-1: '
              f'{max(values) if values else 0}')
        print(f'MIN   should have values between 0-1: '
              f'{min(values) if values else 0}')


@app.timer(2.0, on_leader=True)
async def publish_every_2secs():
    msg = Model(random=round(random(), 2))
    await hopping_topic.send(value=msg)


if __name__ == '__main__':
    app.main()
