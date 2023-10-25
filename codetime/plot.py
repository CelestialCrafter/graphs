import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import numpy as np

lines = open('data.txt', encoding='utf-8').read().splitlines()
data = np.array(np.char.split(lines, '|').tolist())
projects = np.unique(data[:, 0])

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

print('Processing Heartbeats...')
indicies = {project: dtify(data[data[:, 0] == project][:, 1]) for project in projects}
counts = {project: processTimes(indicies[project]) for project in projects}

colors = {
  'main-server': 'plum',
  'algorithm-server': 'darkviolet',
}

ax = plt.gca()
xfmt = md.DateFormatter('%Y %m %d')
ax.xaxis.set_major_formatter(xfmt)

print('Plotting!')
for project, pindicies in indicies.items():
	pcounts = counts[project]

	ptime = [time_delta.total_seconds() / 60 / 60 for time_delta in pcounts]
	plt.plot(pindicies, ptime, color=colors[project] if project in colors else 'black')

	plt.text(pindicies[-1], ptime[-1], f'{project}\n{str(pcounts[-1])}')

plt.show()
