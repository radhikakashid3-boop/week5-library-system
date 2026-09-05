import unittest
from library_system.book import Book


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = Book(
            "Python Basics",
            "John Smith",
            "1234567890",
            2024
        )

    def test_book_created(self):
        self.assertEqual(self.book.title, "Python Basics")
        self.assertEqual(self.book.author, "John Smith")
        self.assertEqual(self.book.isbn, "1234567890")
        self.assertTrue(self.book.available)

    def test_checkout_book(self):
        success, message = self.book.check_out("MEM001")

        self.assertTrue(success)
        self.assertFalse(self.book.available)
        self.assertEqual(self.book.borrowed_by, "MEM001")
        self.assertIsNotNone(self.book.due_date)

    def test_checkout_unavailable_book(self):
        self.book.check_out("MEM001")

        success, message = self.book.check_out("MEM002")

        self.assertFalse(success)

    def test_return_book(self):
        self.book.check_out("MEM001")

        success, message = self.book.return_book()

        self.assertTrue(success)
        self.assertTrue(self.book.available)
        self.assertIsNone(self.book.borrowed_by)
        self.assertIsNone(self.book.due_date)

    def test_return_available_book(self):
        success, message = self.book.return_book()

        self.assertFalse(success)

    def test_not_overdue(self):
        self.book.check_out("MEM001")

        self.assertFalse(self.book.is_overdue())
        self.assertEqual(self.book.days_overdue(), 0)

    def test_to_dict(self):
        data = self.book.to_dict()

        self.assertEqual(data["title"], "Python Basics")
        self.assertEqual(data["author"], "John Smith")
        self.assertEqual(data["isbn"], "1234567890")

    def test_from_dict(self):
        data = {
            "title": "Clean Code",
            "author": "Robert Martin",
            "isbn": "9876543210",
            "year": 2008,
            "available": True,
            "borrowed_by": None,
            "due_date": None
        }

        book = Book.from_dict(data)

        self.assertEqual(book.title, "Clean Code")
        self.assertEqual(book.isbn, "9876543210")
        self.assertTrue(book.available)


if __name__ == "__main__":
    unittest.main()
