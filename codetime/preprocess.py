import json

dataset_name = input('Dataset name: ')

try:
	with open(f'{dataset_name}.json', encoding='ascii', errors='ignore') as f:
		dataset = json.load(f)
		dataset = [
		  '\n'.join([f'{heartbeat["project"]}|{round(heartbeat["time"])}'
		             for heartbeat in day['heartbeats']])
		  for day in dataset['days']
		]
except FileNotFoundError:
	print(f'Could not load {dataset_name}.json')

dataset = '\n'.join(dataset).replace('\n\n', '\n')

with open(f'{dataset_name}.txt', 'w', encoding='utf-8', newline='\n', errors='ignore') as f:
	f.write(dataset)
