import json
import os
import shutil
from datetime import datetime

from .book import Book
from .member import Member


class Library:
    """Manages books, members, borrowing and library operations."""

    def __init__(self):
        self.books = {}
        self.members = {}

    # ---------------- BOOK MANAGEMENT ----------------

    def add_book(self, book):
        """Add a new book to the library."""

        if book.isbn in self.books:
            return False, "A book with this ISBN already exists."

        self.books[book.isbn] = book
        return True, "Book added successfully."

    def remove_book(self, isbn):
        """Remove a book from the library."""

        if isbn not in self.books:
            return False, "Book not found."

        book = self.books[isbn]

        if not book.available:
            return False, "Cannot remove a borrowed book."

        del self.books[isbn]
        return True, "Book removed successfully."

    def find_book(self, isbn):
        """Find a book using ISBN."""

        return self.books.get(isbn)

    # ---------------- MEMBER MANAGEMENT ----------------

    def register_member(self, member):
        """Register a new library member."""

        if member.member_id in self.members:
            return False, "Member ID already exists."

        self.members[member.member_id] = member
        return True, "Member registered successfully."

    def find_member(self, member_id):
        """Find a member using member ID."""

        return self.members.get(member_id)

    # ---------------- BORROW / RETURN ----------------

    def borrow_book(self, isbn, member_id):
        """Borrow a book for a member."""

        book = self.find_book(isbn)

        if book is None:
            return False, "Book not found."

        member = self.find_member(member_id)

        if member is None:
            return False, "Member not found."

        if not book.available:
            return False, "Book is already borrowed."

        success, message = member.borrow_book(isbn)

        if not success:
            return False, message

        success, message = book.check_out(member_id)

        if not success:
            member.return_book(isbn)
            return False, message

        return True, message

    def return_book(self, isbn, member_id):
        """Return a borrowed book."""

        book = self.find_book(isbn)

        if book is None:
            return False, "Book not found."

        member = self.find_member(member_id)

        if member is None:
            return False, "Member not found."

        if book.available:
            return False, "Book is already available."

        if book.borrowed_by != member_id:
            return False, "This book was not borrowed by this member."

        overdue_days = book.days_overdue()

        success, message = member.return_book(isbn)

        if not success:
            return False, message

        success, book_message = book.return_book()

        if not success:
            member.borrow_book(isbn)
            return False, book_message

        if overdue_days > 0:
            fine = overdue_days * 2
            return True, (
                f"Book returned successfully. "
                f"Overdue by {overdue_days} day(s). "
                f"Fine: ₹{fine}"
            )

        return True, "Book returned successfully."

    # ---------------- SEARCH ----------------

    def search_books(self, keyword, search_by="title"):
        """Search books by title, author or ISBN."""

        keyword = keyword.lower()
        results = []

        for book in self.books.values():

            if search_by == "title":
                value = book.title.lower()

            elif search_by == "author":
                value = book.author.lower()

            elif search_by == "isbn":
                value = book.isbn.lower()

            else:
                return []

            if keyword in value:
                results.append(book)

        return results

    def available_books(self):
        """Return all available books."""

        return [
            book for book in self.books.values()
            if book.available
        ]

    def overdue_books(self):
        """Return all overdue books."""

        return [
            book for book in self.books.values()
            if book.is_overdue()
        ]

    # ---------------- STATISTICS ----------------

    def get_statistics(self):
        """Return library statistics."""

        total_books = len(self.books)

        available_books = sum(
            1 for book in self.books.values()
            if book.available
        )

        borrowed_books = total_books - available_books

        total_members = len(self.members)

        overdue_books = len(self.overdue_books())

        return {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "total_members": total_members,
            "overdue_books": overdue_books
        }

    # ---------------- FILE OPERATIONS ----------------

    def save_data(self, books_file="data/books.json",
                  members_file="data/members.json"):

        """Save books and members to JSON files."""

        os.makedirs(os.path.dirname(books_file), exist_ok=True)

        books_data = {
            isbn: book.to_dict()
            for isbn, book in self.books.items()
        }

        members_data = {
            member_id: member.to_dict()
            for member_id, member in self.members.items()
        }

        with open(books_file, "w", encoding="utf-8") as file:
            json.dump(books_data, file, indent=4)

        with open(members_file, "w", encoding="utf-8") as file:
            json.dump(members_data, file, indent=4)

        return True, "Library data saved successfully."

    def load_data(self, books_file="data/books.json",
                  members_file="data/members.json"):

        """Load books and members from JSON files."""

        try:
            if os.path.exists(books_file):
                with open(books_file, "r", encoding="utf-8") as file:
                    books_data = json.load(file)

                self.books = {
                    isbn: Book.from_dict(data)
                    for isbn, data in books_data.items()
                }

            if os.path.exists(members_file):
                with open(members_file, "r", encoding="utf-8") as file:
                    members_data = json.load(file)

                self.members = {
                    member_id: Member.from_dict(data)
                    for member_id, data in members_data.items()
                }

            return True, "Library data loaded successfully."

        except (json.JSONDecodeError, OSError, KeyError) as error:
            return False, f"Error loading data: {error}"

    # ---------------- BACKUP ----------------

    def create_backup(self,
                      books_file="data/books.json",
                      members_file="data/members.json",
                      backup_folder="data/backup"):

        """Create backup copies of library data."""

        try:
            os.makedirs(backup_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            if os.path.exists(books_file):
                backup_books = os.path.join(
                    backup_folder,
                    f"books_{timestamp}.json"
                )
                shutil.copy2(books_file, backup_books)

            if os.path.exists(members_file):
                backup_members = os.path.join(
                    backup_folder,
                    f"members_{timestamp}.json"
                )
                shutil.copy2(members_file, backup_members)

            return True, "Backup created successfully."

        except OSError as error:
            return False, f"Backup failed: {error}"
            