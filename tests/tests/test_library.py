import unittest

from library_system.book import Book
from library_system.member import Member
from library_system.library import Library


class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()

        self.book = Book(
            "Python Basics",
            "John Smith",
            "ISBN001",
            2025
        )

        self.member = Member(
            "Radhika",
            "MEM001"
        )

    def test_add_book(self):
        success, message = self.library.add_book(self.book)

        self.assertTrue(success)
        self.assertIn("ISBN001", self.library.books)

    def test_duplicate_book(self):
        self.library.add_book(self.book)

        duplicate = Book(
            "Another Book",
            "Another Author",
            "ISBN001",
            2025
        )

        success, message = self.library.add_book(duplicate)

        self.assertFalse(success)

    def test_find_book(self):
        self.library.add_book(self.book)

        result = self.library.find_book("ISBN001")

        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Python Basics")

    def test_remove_book(self):
        self.library.add_book(self.book)

        success, message = self.library.remove_book("ISBN001")

        self.assertTrue(success)
        self.assertNotIn("ISBN001", self.library.books)

    def test_register_member(self):
        success, message = self.library.register_member(
            self.member
        )

        self.assertTrue(success)
        self.assertIn("MEM001", self.library.members)

    def test_find_member(self):
        self.library.register_member(self.member)

        result = self.library.find_member("MEM001")

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "Radhika")

    def test_borrow_book(self):
        self.library.add_book(self.book)
        self.library.register_member(self.member)

        success, message = self.library.borrow_book(
            "ISBN001",
            "MEM001"
        )

        self.assertTrue(success)
        self.assertFalse(self.book.available)
        self.assertIn(
            "ISBN001",
            self.member.borrowed_books
        )

    def test_return_book(self):
        self.library.add_book(self.book)
        self.library.register_member(self.member)

        self.library.borrow_book(
            "ISBN001",
            "MEM001"
        )

        success, message = self.library.return_book(
            "ISBN001",
            "MEM001"
        )

        self.assertTrue(success)
        self.assertTrue(self.book.available)
        self.assertNotIn(
            "ISBN001",
            self.member.borrowed_books
        )

    def test_search_by_title(self):
        self.library.add_book(self.book)

        results = self.library.search_books(
            "python",
            "title"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0].title,
            "Python Basics"
        )

    def test_search_by_author(self):
        self.library.add_book(self.book)

        results = self.library.search_books(
            "john",
            "author"
        )

        self.assertEqual(len(results), 1)

    def test_search_by_isbn(self):
        self.library.add_book(self.book)

        results = self.library.search_books(
            "ISBN001",
            "isbn"
        )

        self.assertEqual(len(results), 1)

    def test_available_books(self):
        self.library.add_book(self.book)

        results = self.library.available_books()

        self.assertEqual(len(results), 1)

    def test_statistics(self):
        self.library.add_book(self.book)
        self.library.register_member(self.member)

        stats = self.library.get_statistics()

        self.assertEqual(stats["total_books"], 1)
        self.assertEqual(stats["available_books"], 1)
        self.assertEqual(stats["borrowed_books"], 0)
        self.assertEqual(stats["total_members"], 1)
        self.assertEqual(stats["overdue_books"], 0)


if __name__ == "__main__":
    unittest.main()
    