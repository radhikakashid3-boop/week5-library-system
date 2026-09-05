# 📚 Library Management System

A console-based Library Management System built using **Python Object-Oriented Programming (OOP)**.

The system allows librarians to manage books and members, handle book borrowing and returning, search books, track due dates, calculate overdue fines, and store library data using JSON files.

---

## 🎯 Project Objective

The main objective of this project is to understand and implement **Object-Oriented Programming concepts** using a real-world Library Management System.

The project demonstrates:

- Classes and Objects
- Encapsulation
- Class Methods
- Constructors
- Object Relationships
- File Handling
- JSON Data Persistence
- Exception Handling
- Unit Testing

---

## ✨ Features

- ➕ Add new books
- ❌ Remove books
- 🔎 Search books by title, author, or ISBN
- 👤 Register library members
- 📖 Borrow books
- ↩️ Return books
- 📅 Track book due dates
- ⚠️ Detect overdue books
- 💰 Calculate overdue fines
- 📊 Display library statistics
- 💾 Save data to JSON files
- 📂 Load data from JSON files
- 🔐 Create backup files
- 🧪 Unit testing for Book, Member, and Library classes
- 🖥️ User-friendly console menu

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OOP | Application architecture |
| JSON | Data persistence |
| unittest | Testing |
| Git | Version control |
| GitHub | Project hosting |

---

## 📁 Project Structure

```text
week5-library-system/
│
├── library_system/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   ├── library.py
│   └── main.py
│
├── data/
│   ├── books.json
│   ├── members.json
│   └── backup/
│
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
│
├── requirements.txt
├── README.md
└── .gitignore
