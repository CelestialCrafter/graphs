import datetime as dt

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np

lines = open('data.txt', encoding='utf-8').read().splitlines()
data = np.array(np.char.split(lines, '|').tolist())
artists = np.unique(data[:, 0])

dtify = np.frompyfunc(lambda timestamp: dt.datetime.fromtimestamp(int(timestamp)), 1, 1)

def processTimes(times):
	hours = [dt.timedelta(seconds=0)]

	for time in times:
		hours.append(hours[-1] + dt.timedelta(milliseconds=int(time)))

	return hours[1:]

print('Processing Tracks...')
indicies = {artist: dtify(data[data[:, 0] == artist][:, 2]) for artist in artists}
counts = {artist: processTimes(data[data[:, 0] == artist][:, 1]) for artist in artists}

colors = {
  'NIKI': 'plum',
  'keshi': 'darkviolet',
  'beabadoobee': 'deepskyblue',
  'yorushika': 'crimson',
}

ax = plt.gca()
xfmt = md.DateFormatter('%Y %m %d')
ax.xaxis.set_major_formatter(xfmt)

print('Plotting!')
for artist, pindicies in indicies.items():
	#if artist != 'NIKI' and artist != 'keshi' and artist != 'yorushika':
	#	continue
	pcounts = counts[artist]

	ptime = [time_delta.total_seconds() / 60 / 60 for time_delta in pcounts]
	plt.plot(pindicies, ptime, color=colors[artist] if artist in colors else 'black')

	plt.text(pindicies[-1], ptime[-1], f'{artist}\n{str(pcounts[-1])}')

plt.show()
