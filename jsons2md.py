#!/usr/bin/env python
from sys import exec_prefix

from ggkindle import *
from pathlib import Path
import json


jdir = Path('jsons')
jdir = Path(r'C:\Users\luigi.antelmi\Dropbox\LIBRI\kindle\jsons')

library = Library()

for jfile in jdir.glob("*.json"):
	try:
		with open(jfile, 'r', encoding='utf-8') as f:
			print(jfile)
			jbook = json.load(f)
			book = Book(json=jbook)
			library.add(book)
	except Exception as e:
		print(jfile)
		print(e)
		raise

library.export_to(library_dir='books')

print("See you!")