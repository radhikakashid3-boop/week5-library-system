import unittest
from library_system.member import Member


class TestMember(unittest.TestCase):

    def setUp(self):
        self.member = Member("Radhika", "MEM001")

    def test_member_creation(self):
        self.assertEqual(self.member.name, "Radhika")
        self.assertEqual(self.member.member_id, "MEM001")
        self.assertEqual(self.member.borrowed_books, [])

    def test_borrow_book(self):
        success, message = self.member.borrow_book("ISBN001")

        self.assertTrue(success)
        self.assertIn("ISBN001", self.member.borrowed_books)

    def test_return_book(self):
        self.member.borrow_book("ISBN001")

        success, message = self.member.return_book("ISBN001")

        self.assertTrue(success)
        self.assertNotIn("ISBN001", self.member.borrowed_books)

    def test_return_not_borrowed_book(self):
        success, message = self.member.return_book("ISBN999")

        self.assertFalse(success)

    def test_duplicate_book(self):
        self.member.borrow_book("ISBN001")

        success, message = self.member.borrow_book("ISBN001")

        self.assertFalse(success)

    def test_maximum_books(self):
        for number in range(1, 6):
            self.member.borrow_book(f"ISBN00{number}")

        success, message = self.member.borrow_book("ISBN006")

        self.assertFalse(success)
        self.assertEqual(len(self.member.borrowed_books), 5)

    def test_has_borrowed(self):
        self.member.borrow_book("ISBN001")

        self.assertTrue(
            self.member.has_borrowed("ISBN001")
        )

        self.assertFalse(
            self.member.has_borrowed("ISBN002")
        )

    def test_to_dict(self):
        self.member.borrow_book("ISBN001")

        data = self.member.to_dict()

        self.assertEqual(data["name"], "Radhika")
        self.assertEqual(data["member_id"], "MEM001")
        self.assertIn("ISBN001", data["borrowed_books"])


if __name__ == "__main__":
    unittest.main()
    