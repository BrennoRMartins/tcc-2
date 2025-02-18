from flask import request
import psycopg2 as ps
from psycopg2 import OperationalError
import psycopg2

def connect_to_database():
    """Connects to the PostgreSQL database.

    Returns:
        psycopg2.connection: A connection object if successful, None otherwise.
    """
    try:
        connection = ps.connect(host="localhost", database="tcc", user="postgres", password="123", port="5432")
        return connection
    except OperationalError as e:
        print(f"Error connecting to database: {e}")
        return None

def insert_feedback(connection, rating, comment, email):
    """Inserts feedback data into the database.

    Args:
        connection (psycopg2.connection): The database connection object.
        rating (int): The user's rating (1-5).
        comment (str): The user's feedback comment.
        email (str): The user's email address (optional).
    """
    cursor = connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO feedback (rating, comment, email)
            VALUES (%s, %s, %s)
        """, (rating, comment, email))
        connection.commit()
        print("Feedback inserted successfully!")
    except (Exception, psycopg2.Error) as error:
        print(f"Error inserting feedback: {error}")
        connection.rollback()  # Rollback on error
    finally:
        if cursor:
            cursor.close()

if __name__ == "__main__":
    # Connect to the database
    connection = connect_to_database()
    if connection:
        # If connection successful, retrieve data from the form
        try:
            # Assuming data is accessible via form data or request object
            rating = int(request.form["rating"])
            comment = request.form["comment"]
            email = request.form.get("email", "")  # Handle optional email

            # Insert data into the database
            insert_feedback(connection, rating, comment, email)
        except (ValueError, KeyError) as e:
            print(f"Error retrieving data from form: {e}")
        finally:
            connection.close()  # Close connection after processing
    else:
        print("Database connection failed!")
