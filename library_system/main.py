from .book import Book
from .member import Member
from .library import Library


def display_books(books):
    """Display books in a formatted way."""

    if not books:
        print("\nNo books found.")
        return

    print("\n" + "-" * 70)

    for index, book in enumerate(books, start=1):
        print(f"{index}. {book.title}")
        print(f"   Author : {book.author}")
        print(f"   ISBN   : {book.isbn}")
        print(f"   Year   : {book.year}")

        if book.available:
            print("   Status : Available")
        else:
            print(
                f"   Status : Borrowed by {book.borrowed_by}"
                f" (Due: {book.due_date})"
            )

        print("-" * 70)


def add_book(library):
    """Add a new book."""

    print("\n--- Add New Book ---")

    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    isbn = input("Enter ISBN: ").strip()

    year_input = input("Enter publication year (optional): ").strip()

    if year_input:
        try:
            year = int(year_input)
        except ValueError:
            print("Invalid year.")
            return
    else:
        year = None

    if not title or not author or not isbn:
        print("Title, author and ISBN are required.")
        return

    book = Book(title, author, isbn, year)

    success, message = library.add_book(book)
    print(message)


def register_member(library):
    """Register a new member."""

    print("\n--- Register New Member ---")

    name = input("Enter member name: ").strip()
    member_id = input("Enter member ID: ").strip()

    if not name or not member_id:
        print("Name and Member ID are required.")
        return

    member = Member(name, member_id)

    success, message = library.register_member(member)
    print(message)


def borrow_book(library):
    """Borrow a book."""

    print("\n--- Borrow Book ---")

    isbn = input("Enter book ISBN: ").strip()
    member_id = input("Enter member ID: ").strip()

    success, message = library.borrow_book(isbn, member_id)

    print(message)


def return_book(library):
    """Return a book."""

    print("\n--- Return Book ---")

    isbn = input("Enter book ISBN: ").strip()
    member_id = input("Enter member ID: ").strip()

    success, message = library.return_book(isbn, member_id)

    print(message)


def search_books(library):
    """Search books."""

    print("\n--- Search Books ---")
    print("1. Search by Title")
    print("2. Search by Author")
    print("3. Search by ISBN")
    print("4. Show All Available Books")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        keyword = input("Enter title to search: ").strip()
        results = library.search_books(keyword, "title")

    elif choice == "2":
        keyword = input("Enter author to search: ").strip()
        results = library.search_books(keyword, "author")

    elif choice == "3":
        keyword = input("Enter ISBN to search: ").strip()
        results = library.search_books(keyword, "isbn")

    elif choice == "4":
        results = library.available_books()

    else:
        print("Invalid choice.")
        return

    display_books(results)

    print(f"\nFound {len(results)} book(s).")


def view_all_books(library):
    """Display all books."""

    print("\n--- All Books ---")

    books = list(library.books.values())

    display_books(books)

    print(f"\nTotal Books: {len(books)}")


def view_all_members(library):
    """Display all members."""

    print("\n--- All Members ---")

    if not library.members:
        print("No members registered.")
        return

    print("-" * 70)

    for index, member in enumerate(
        library.members.values(), start=1
    ):
        print(f"{index}. Name      : {member.name}")
        print(f"   Member ID  : {member.member_id}")
        print(
            f"   Books      : "
            f"{len(member.borrowed_books)}"
        )
        print("-" * 70)


def view_overdue_books(library):
    """Display overdue books."""

    print("\n--- Overdue Books ---")

    books = library.overdue_books()

    if not books:
        print("No overdue books.")
        return

    display_books(books)

    for book in books:
        print(
            f"{book.title} → "
            f"{book.days_overdue()} day(s) overdue"
        )


def show_statistics(library):
    """Display library statistics."""

    stats = library.get_statistics()

    print("\n" + "=" * 40)
    print("       LIBRARY STATISTICS")
    print("=" * 40)

    print(f"Total Books     : {stats['total_books']}")
    print(f"Available Books : {stats['available_books']}")
    print(f"Borrowed Books  : {stats['borrowed_books']}")
    print(f"Total Members   : {stats['total_members']}")
    print(f"Overdue Books   : {stats['overdue_books']}")

    print("=" * 40)


def show_menu():
    """Display main menu."""

    print("\n" + "=" * 40)
    print("     LIBRARY MANAGEMENT SYSTEM")
    print("=" * 40)

    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. Library Statistics")
    print("10. Save & Exit")
    print("0. Exit Without Saving")

    print("=" * 40)


def main():
    """Main application function."""

    library = Library()

    success, message = library.load_data()

    if success:
        print(message)
    else:
        print(message)

    while True:

        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(library)

        elif choice == "2":
            register_member(library)

        elif choice == "3":
            borrow_book(library)

        elif choice == "4":
            return_book(library)

        elif choice == "5":
            search_books(library)

        elif choice == "6":
            view_all_books(library)

        elif choice == "7":
            view_all_members(library)

        elif choice == "8":
            view_overdue_books(library)

        elif choice == "9":
            show_statistics(library)

        elif choice == "10":
            success, message = library.save_data()
            print(message)

            if success:
                backup_success, backup_message = (
                    library.create_backup()
                )
                print(backup_message)

            print("Thank you for using Library Management System!")
            break

        elif choice == "0":
            print("Exited without saving changes.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
    