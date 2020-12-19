#!/usr/bin/env python
from ggkindle import *
from pathlib import Path
import json


jdir = Path('jsons')

library = Library()

for jfile in jdir.glob("*.json"):

	with open(jfile, 'r') as f:
		jbook = json.load(f)
		book = Book(json=jbook)
		library.add(book)

library.export_to(library_dir='books')

print("See you!")