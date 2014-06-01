import math
from time import sleep
from random import random

import databench


signals = databench.Signals('dummypi')

@signals.on('connect')
def onconnect():
	inside = 0
	for i in range(10000):
		sleep(0.001)
		r1, r2 = (random(), random())
		if r1*r1 + r2*r2 < 1.0: 
			inside += 1

		if (i+1)%100 == 0:
			draws = i+1
			signals.emit('log', {
				'draws':draws, 
				'inside':inside, 
				'r1':r1, 
				'r2':r2
			})

			p = float(inside)/draws
			uncertainty = 4.0*math.sqrt(draws*p*(1.0 - p)) / draws
			signals.emit('status', {
				'pi-estimate': 4.0*inside/draws,
				'pi-uncertainty': uncertainty
			})

	signals.emit('log', {'action': 'done'})


dummypi = databench.Analysis('dummypi', __name__, signals)
dummypi.thumbnail = 'dummypi.png'
dummypi.description = """Calculating \(\pi\) the simple way, but this is called 
dummypi to avoid conflict with simplepi in the databench_examples repo."""
