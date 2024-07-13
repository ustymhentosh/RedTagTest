import sqlite3


class DB:
    """
    Abstraction class over SQLite database
    """

    def __init__(self) -> None:
        self.db_connection = sqlite3.connect("db.sqlite", check_same_thread=False)

    def get_all_books(self) -> list:
        """Gets list of all books from database

        Returns:
            list: list of tuples representing rows in the 'books' table
        """
        cur = self.db_connection.cursor()
        query = "SELECT * FROM books"
        cur.execute(query)
        return cur.fetchall()

    def get_all_authors(self) -> list:
        """Gets list of all authors from databes

        Returns:
            list: list of tuples representing authors` names
        """
        cur = self.db_connection.cursor()
        query = "SELECT * FROM authors"
        cur.execute(query)
        return cur.fetchall()

    def add_author(self, name: str) -> bool:
        """Adds author to the database

        Args:
            name (str): name of an author

        Returns:
            bool: True when success
        """
        cur = self.db_connection.cursor()
        author_query = "SELECT * FROM authors WHERE name = ?;"
        cur.execute(author_query, (name,))

        if len(cur.fetchall()) == 0:
            insert_query = "INSERT INTO authors (name) VALUES (?);"
            cur.execute(insert_query, (name,))
            self.db_connection.commit()
            cur.close()
            return True

        cur.close()
        return True

    def export_books(self) -> str:
        """Creates string representing .csv file of the books table

        Returns:
            str: sting in csv format
        """
        cur = self.db_connection.cursor()
        query = "SELECT * FROM books"
        cur.execute(query)
        books = cur.fetchall()
        cur.close()

        output = "Title,Description,Author\n"
        for book in books:
            output += f"{book[1]},{book[2]},{book[3]}\n"
        return output[:-1]

    def add_book(self, title: str, desc: str, author: str) -> bool:
        """Adds single book into the database

        Args:
            title (str): Title of the book
            desc (str): Description of the book
            author (str): Book's author's name

        Returns:
            bool: True if success
        """
        cur = self.db_connection.cursor()
        author_query = "SELECT * FROM authors WHERE name = ?;"
        author_result = cur.execute(author_query, (author,))
        if len(author_result.fetchall()) == 0:
            author_query = "INSERT INTO authors (name) VALUES (?);"
            cur.execute(author_query, (author,))

        query = """
        INSERT INTO books (title, description, author_name) 
        VALUES (?, ?, ?);
        """
        cur.execute(query, (title, desc, author))
        self.db_connection.commit()
        cur.close()
        return True

    def delete_book(self, id: int) -> bool:
        """deletes book from db by index

        Args:
            id (int): index of the book

        Returns:
            bool: True if success
        """
        print(id)
        cur = self.db_connection.cursor()
        query = "DELETE FROM books WHERE id = ?;"
        cur.execute(query, (id,))
        self.db_connection.commit()
        cur.close()
        return True

    def delete_author_and_books(self, name: str) -> bool:
        """Given author's deletes him from db and all his books

        Args:
            name (str): name of the author

        Returns:
            bool: True if success
        """
        cur = self.db_connection.cursor()
        query1 = "DELETE FROM authors WHERE name = ?;"
        query2 = "DELETE FROM books WHERE author_name = ?;"
        cur.execute(query1, (name,))
        cur.execute(query2, (name,))
        self.db_connection.commit()
        cur.close()
        return True

    def edit_book_by_id(self, id: int, title: str, desc: str, author: str) -> bool:
        """Changes column values for one book given new data and index

        Args:
            id (int): index of the book
            title (str): Title of the book
            desc (str): Description of the book
            author (str): Book's author's name

        Returns:
            bool: True if success
        """
        cur = self.db_connection.cursor()

        author_query = "SELECT * FROM authors WHERE name = ?;"
        author_result = cur.execute(author_query, (author,))
        if len(author_result.fetchall()) == 0:
            author_query = "INSERT INTO authors (name) VALUES (?);"
            cur.execute(author_query, (author,))

        query = """
        UPDATE books
        SET title = ?, description = ?, author_name = ?
        WHERE id = ?;
        """
        cur.execute(query, (title, desc, author, id))
        self.db_connection.commit()
        cur.close()
        return True
