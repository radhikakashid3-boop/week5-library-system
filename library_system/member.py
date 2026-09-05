class Member:
    """Represents a library member."""

    MAX_BOOKS = 5

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, isbn):
        """Add a book ISBN to the member's borrowed books."""

        if len(self.borrowed_books) >= self.MAX_BOOKS:
            return False, f"Borrowing limit reached. Maximum {self.MAX_BOOKS} books allowed."

        if isbn in self.borrowed_books:
            return False, "This book is already borrowed by the member."

        self.borrowed_books.append(isbn)

        return True, "Book added to member's borrowed books."

    def return_book(self, isbn):
        """Remove a book ISBN from borrowed books."""

        if isbn not in self.borrowed_books:
            return False, "This book is not borrowed by this member."

        self.borrowed_books.remove(isbn)

        return True, "Book returned successfully."

    def has_borrowed(self, isbn):
        """Check whether the member has borrowed a particular book."""

        return isbn in self.borrowed_books

    def to_dict(self):
        """Convert Member object into dictionary."""

        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member object from dictionary."""

        member = cls(
            name=data["name"],
            member_id=data["member_id"]
        )

        member.borrowed_books = data.get("borrowed_books", [])

        return member

    def __str__(self):
        return (
            f"Member ID: {self.member_id} | "
            f"Name: {self.name} | "
            f"Books Borrowed: {len(self.borrowed_books)}"
        )
        