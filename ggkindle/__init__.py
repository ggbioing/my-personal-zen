import re


def parse_single_highlight(highlight_string):
	splitted_string = highlight_string.split("\n")
	author_line = splitted_string[1]
	content = splitted_string[-2]
	regex = "\((.*)\)"
	match = re.search(regex, author_line)

	if match:
		author = match.group(0)
		title = author_line[: match.start()]
		return title, author, content

	return None, None, None


class Highlight:

	def __init__(self, raw_string):
		self.title, self.author, self.content = parse_single_highlight(raw_string)

	def __repr__(self):
		return f"{self.content}"


class Book:

	def __init__(self, title=None, author=None, json=None):

		self.json = json

		if self.json is None:
			self.author = author
			self.title = title
			self.highlights = []
		else:
			self.asin = self.json['asin']  # BOOK ID
			self.author = self.json['authors']
			self.title = self.json['title']
			self.highlights = self.json['highlights']

	def add_highlight(self, highlight):

		assert isinstance(highlight, Highlight)

		if highlight:
			self.highlights.append(highlight)

	def __repr__(self):
		return f"{self.title}\n\tHighlights: {len(self.highlights)}"

	def write_book(self, library_dir):
		if self.title == None or len(self.highlights) == 0:
			print(f"Not writing because name is None.")
			return False
		clean_title = "".join(
			[c for c in self.title if c.isalpha() or c.isdigit() or c == " "]
		).rstrip()
		with open(f"{library_dir}/{clean_title}.md", "w+", encoding='utf-8') as file:
			file.write(f"# {clean_title}\n")
			file.write(f"## {self.author}\n")
			for h in self.highlights:
				try:
					if isinstance(h, Highlight):
						clean_text = h.content.replace("\n", " ")
					elif isinstance(h, dict):
						clean_text = h['text']
					else:
						raise NotImplementedError
					file.write(f"- {clean_text}")
					file.write("\n")
				except Exception as e:
					print(clean_title)
					print(h)
					print(e)

			file.close()


class Library:
	book_list = set()

	def __init__(self):
		self.books = []

	def add(self, book):
		assert isinstance(book, Book)

		self.books.append(book)
		self.book_list.add(book.title)

	def export_to(self, library_dir):
		for b in self:
			b.write_book(library_dir=library_dir)

	def __len__(self):
		return len(self.book_list)

	def __getitem__(self, i):
		return self.books[i]


__all__ = [
	'Highlight',
	'Book',
	'Library',
]