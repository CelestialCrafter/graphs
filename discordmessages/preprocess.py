import json

dataset_name = input('Dataset name: ')

try:
	with open(f'{dataset_name}.json', encoding='ascii', errors='ignore') as f:
		dataset = json.load(f)
		dataset = [
		  f'{message["author"]["name"]}|{message["author"]["id"]}|{message["timestamp"]}' for message in dataset['messages']
		]
except FileNotFoundError:
	print(f'Could not load {dataset_name}.json')

dataset = '\n'.join(dataset)

with open(f'{dataset_name}.txt', 'w', encoding='utf-8', newline='\n', errors='ignore') as f:
	f.write(dataset)
