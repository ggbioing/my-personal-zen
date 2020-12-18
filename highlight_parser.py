#!/usr/bin/env python
"""
A script to parse kindle highlights into markdown
files for my personal github repo. Because other
software was making me pay for it.
Use it, and abuse it.
"""
import re
from pathlib import Path


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
    total_highlights = 0

    def __init__(self, raw_string):
        self.title, self.author, self.content = parse_single_highlight(raw_string)

    def __repr__(self):
        return f"{self.content}"


class Book:

    def __init__(self, title, author):
        self.author = author
        self.title = title
        self.highlights = []

    def add_highlight(self, highlight):

        assert isinstance(highlight, Highlight)

        if highlight:
            self.highlights.append(highlight)

    def __str__(self):
        return self.title

    def write_book(self, library_dir):
        if self.title == None or len(self.highlights) == 0:
            print(f"Not writing because name is None.")
            return False
        clean_title = "".join(
            [c for c in self.title if c.isalpha() or c.isdigit() or c == " "]
        ).rstrip()
        with open(f"{library_dir}/{clean_title}.md", "w+") as file:
            file.write(f"# {clean_title}\n")
            file.write(f"## {self.author}\n")
            for h in self.highlights:
                clean_text = h.content.replace("\n", " ")
                file.write(f"- {clean_text}")
                file.write("\n")

            file.close()


class Library:

    book_list = set()

    def __init__(self):

        self.books = []

    def add(self, book):

        assert isinstance(book, Book)

        self.books.append(book)
        self.book_list.add(book.title)

    def __getitem__(self, i):
        return self.books[i]


if __name__ == "__main__":
    current_directory = Path.cwd()
    parsed_books = list(set(file.stem for file in current_directory.glob("**/*.md")))
    highlight_separator = "=========="
    highlight_json = dict()
    library = Library()
    
    library_dir = Path("books")
    library_dir.mkdir(parents=True, exist_ok=True) if not library_dir.exists() else None

    with open("My Clippings.txt", "r") as file:
        data = file.read()
    
    highlights = data.split(highlight_separator)
    
    for raw_string in highlights:
        h = Highlight(raw_string)
        if h.title not in library.book_list:
            b = Book(h.title, h.author)
            b.add_highlight(h)
            library.add(b)
        else:
            for b in library:
                if b.title == h.title:
                    b.add_highlight(h)
    
    for book in library:
        if book.title:
            if book.title.strip() not in parsed_books:
                book.write_book(library_dir=library_dir)
            else:
                print(f"{book.title} is already written.")
