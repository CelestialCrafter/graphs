import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime as dt
import numpy as np

lines = open('data.txt', encoding='utf-8').read().splitlines()
data = np.array(np.char.split(lines, '|').tolist())
users = np.column_stack((np.unique(data[:, 0]), np.unique(data[:, 1])))

def processException(user):
	name, uid = user

	# Portugla Exceptions
	if name == 'iloveyanna':
		name = '17xr'
	elif name == 'celestialexe_':
		name = 'celestialexe'
	elif uid == '456226577798135808':
		name = 'nikolus_'

	return name

dtify = np.frompyfunc(lambda timestamp: dt.datetime.fromisoformat(timestamp), 1, 1)

print('Processing Messages...')
indicies = {processException(user): dtify(data[data[:, 0] == processException(user)][:, 2]) for user in users}
counts = {user: np.arange(1, indicies[user].shape[0] + 1) for user in [processException(user) for user in users]}

colors = {
  'celestialexe': 'plum',
  'pdbaroni': 'royalblue',
  'normalcat_': 'red',
  'nikolus_': 'darkorange',
  '17xr': 'limegreen',
  'itscattybro': 'darkviolet',
  'morilis': 'sienna',
  'mcsaucynuggets': 'darkviolet'
}

ax = plt.gca()
xfmt = md.DateFormatter('%Y %m %d')
ax.xaxis.set_major_formatter(xfmt)

print('Plotting!')
for user, uindicies in indicies.items():
	ucounts = counts[user]

	plt.plot(uindicies, ucounts, color=colors[user] if user in colors else 'black')

	plt.text(uindicies[-1], ucounts[-1], user)

plt.show()
