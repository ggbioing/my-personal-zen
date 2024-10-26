#!/usr/bin/env python
"""
A script to parse kindle highlights into markdown
files for my personal github repo. Because other
software was making me pay for it.
Use it, and abuse it.
"""
from ggkindle import *
from pathlib import Path

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
