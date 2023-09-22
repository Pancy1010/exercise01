import sqlite3

# Create the database and tables
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Books table
cursor.execute("""CREATE TABLE IF NOT EXISTS Books (
                    BookID INTEGER PRIMARY KEY,
                    Title TEXT,
                    Author TEXT,
                    ISBN TEXT,
                    Status TEXT
                )""")

# Create Users table
cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                    UserID INTEGER PRIMARY KEY,
                    Name TEXT,
                    Email TEXT
                )""")

# Create Reservations table
cursor.execute("""CREATE TABLE IF NOT EXISTS Reservations (
                    ReservationID INTEGER PRIMARY KEY,
                    BookID INTEGER,
                    UserID INTEGER,
                    ReservationDate TEXT,
                    FOREIGN KEY(BookID) REFERENCES Books(BookID),
                    FOREIGN KEY(UserID) REFERENCES Users(UserID)
                )""")

# Commit the changes
conn.commit()


# Add a new book to the database
def add_book():
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    isbn = input("Enter the book ISBN: ")

    cursor.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, 'Available')",
                   (title, author, isbn))
    conn.commit()
    print("Book added successfully.")


# Find a book's detail based on BookID
def find_book_by_id():
    book_id = int(input("Enter the BookID: "))

    cursor.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN,
                      Books.Status, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID
                      WHERE Books.BookID = ?""", (book_id,))
    result = cursor.fetchone()

    if not result:
        print("Book not found.")
    else:
        book_id, title, author, isbn, status, user_name, user_email = result
        print("Book Details:")
        print(f"BookID: {book_id}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"ISBN: {isbn}")
        print(f"Status: {status}")

        if user_name:
            print("Reserved by:")
            print(f"Name: {user_name}")
            print(f"Email: {user_email}")


# Find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation_status():
    input_text = input("Enter BookID, Title, UserID, or ReservationID: ")

    if input_text.startswith("LB"):
        cursor.execute("SELECT Status FROM Books WHERE BookID = ?", (int(input_text[2:]),))
        result = cursor.fetchone()
        if result:
            print(f"Book reservation status: {result[0]}")
        else:
            print("Book not found.")
    elif input_text.startswith("LU"):
        cursor.execute("""SELECT Books.Status FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          INNER JOIN Users ON Reservations.UserID = Users.UserID
                          WHERE Users.UserID = ?""", (int(input_text[2:]),))
        result = cursor.fetchone()
        if result:
            print(f"User reservation status: {result[0]}")
        else:
            print("User not found.")
    elif input_text.startswith("LR"):
        cursor.execute("""SELECT Books.Status FROM Books
                          INNER JOIN Reservations ON Books.BookID = Reservations.BookID
                          WHERE Reservations.ReservationID = ?""", (int(input_text[2:]),))
        result = cursor.fetchone()
        if result:
            print(f"Reservation status for ReservationID {input_text}: {result[0]}")
        else:
            print("Reservation not found.")
    else:
        cursor.execute("SELECT Status FROM Books WHERE Title = ?", (input_text,))
        result = cursor.fetchone()
        if result:
            print(f"Book reservation status: {result[0]}")
        else:
            print("Book not found.")


# Find all the books in the database
def find_all_books():
    cursor.execute("""SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN,
                      Books.Status, Users.Name, Users.Email
                      FROM Books
                      LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                      LEFT JOIN Users ON Reservations.UserID = Users.UserID""")
    results = cursor.fetchall()

    if not results:
        print("No books found.")
    else:
        print("Books:")
        for result in results:
            book_id, title, author, isbn, status, user_name, user_email = result
            print(f"BookID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Status: {status}")

            if user_name:
                print(f"Reserved by: {user_name} ({user_email})")

            print()


# Modify/update book details based on its BookID
def modify_book_details():
    book_id = int(input("Enter the BookID: "))
    new_title = input("Enter the new title (leave blank to keep current title): ")
    new_author = input("Enter the new author (leave blank to keep current author): ")
    new_isbn = input("Enter the new ISBN (leave blank to keep current ISBN): ")
    new_status = input("Enter the new status (leave blank to keep current status): ")

    changes_made = False
    if new_title:
        cursor.execute("UPDATE Books SET Title = ? WHERE BookID = ?", (new_title, book_id))
        changes_made = True
    if new_author:
        cursor.execute("UPDATE Books SET Author = ? WHERE BookID = ?", (new_author, book_id))
        changes_made = True
    if new_isbn:
        cursor.execute("UPDATE Books SET ISBN = ? WHERE BookID = ?", (new_isbn, book_id))
        changes_made = True
    if new_status:
        cursor.execute("UPDATE Books SET Status = ? WHERE BookID = ?", (new_status, book_id))
        # Update reservation status as well
        cursor.execute("""UPDATE Reservations SET ReservationDate = NULL
                          WHERE BookID = ? AND ReservationDate IS NOT NULL""", (book_id,))
        changes_made = True

    if changes_made:
        conn.commit()
        print("Book details modified successfully.")
    else:
        print("No changes were made.")


# Delete a book based on its BookID
def delete_book():
    book_id = int(input("Enter the BookID: "))

    cursor.execute("SELECT COUNT(*) FROM Reservations WHERE BookID = ?", (book_id,))
    result = cursor.fetchone()

    if result[0] == 0:
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    else:
        cursor.execute("DELETE FROM Books WHERE BookID = ?", (book_id,))
        cursor.execute("DELETE FROM Reservations WHERE BookID = ?", (book_id,))
        conn.commit()
        print("Book and associated reservations deleted successfully.")


# Menu loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's details based on BookID")
    print("3. Find a book's reservation status")
    print("4. Find all the books in the database")
    print("5. Modify/update book details based on BookID")
    print("6. Delete a book based on BookID")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        find_book_by_id()
    elif choice == "3":
        find_reservation_status()
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        modify_book_details()
    elif choice == "6":
        delete_book()
    elif choice == "7":
        break
    else:
        print("Invalid choice. Please try again.")

# Close the connection
conn.close()
