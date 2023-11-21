import pymysql.cursors
from typing import List, Tuple



class DB:
    """
    A class representing a database connection and operations.

    Attributes:
        connection: The database connection object.
        cursor: The database cursor object.

    Methods:
        __init__: Initializes the DB object and establishes a database connection.
        get_urls: Placeholder method for retrieving URLs from the database.
        insert: Inserts data into the specified table in the database.
        close_connection: Closes the database connection.
        __del__: Destructor method that closes the database connection.

    """

    def __init__(self, server: str, user: str, password: str, db: str) -> None:
        """
        Initializes the DB object and establishes a database connection.

        Args:
            server: The server address of the database.
            user: The username for the database connection.
            password: The password for the database connection.
            db: The name of the database.

        Returns:
            None

        """
        self.connection = pymysql.connect(
            host=server,
            user=user,
            password=password,
            database=db,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()


    def get_urls(self):
        """
        Placeholder method for retrieving URLs from the database.

        Returns:
            None

        """
        pass


    def insert(self, data: List[Tuple], table: str) -> None:
        """
        Inserts data into the specified table in the database.

        Args:
            data: A list of tuples containing the data to be inserted.
            table: The name of the table in the database.

        Returns:
            None

        """
        table_creation_sql = f"""CREATE TABLE IF NOT EXISTS {table} 
            (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            client_id INT, 
            title VARCHAR(255), 
            description TEXT, 
            token_cost VARCHAR(255), 
            scraping_start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            scraping_end_time TIMESTAMP,
            source VARCHAR(255)
            )
        """
        self.cursor.execute(table_creation_sql)
        self.connection.commit()
        insert_sql = f"""INSERT INTO {table} 
            (
            client_id, 
            title, 
            description, 
            token_cost,
            scraping_start_time,
            scraping_end_time,
            source
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.executemany(insert_sql, data)
        self.connection.commit()


    def close_connection(self):
        """
        Closes the database connection.

        Returns:
            None

        """
        self.connection.close()


    def __del__(self):
        """
        Destructor method that closes the database connection.

        Returns:
            None

        """
        self.close_connection()
