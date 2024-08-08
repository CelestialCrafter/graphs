import datetime as dt

import matplotlib.dates as md
import matplotlib.pyplot as plt
import numpy as np

lines = open('data.txt', encoding='utf-8').read().splitlines()
data = np.array(np.char.split(lines, '|').tolist())
artists = np.unique(data[:, 0])

dtify = np.frompyfunc(lambda timestamp: dt.datetime.fromtimestamp(int(timestamp)), 1, 1)

def processTimes(timestamps):
	previousTime = 0
	hours = [dt.timedelta(seconds=0)]

	for timestamp in timestamps:
		if timestamp == timestamps[0]:
			previousTime = timestamp
			continue

		difference = (timestamp - previousTime)
		if difference.total_seconds() > 6 * 60:
			hours.append(hours[-1])
		else:
			hours.append(hours[-1] + difference)

		previousTime = timestamp
	return hours

print('Processing Plays...')
indicies = {artist: dtify(data[data[:, 0] == artist][:, 1]) for artist in artists}
counts = {artist: np.arange(1, indicies[artist].shape[0] + 1) for artist in artists}

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
	pcounts = counts[artist]

	plt.plot(pindicies, pcounts, color=colors[artist] if artist in colors else 'black')

	plt.text(pindicies[-1], pcounts[-1], f'{artist}\n{str(pcounts[-1])}')

plt.show()
